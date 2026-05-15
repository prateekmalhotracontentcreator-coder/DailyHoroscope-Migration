# Library Amendment Contract -- [Book Title]
> Amendment to: Commission I -- Jyotish Knowledge Engine
> Amendment No: LA-00X
> Date: YYYY-MM-DD
> Book File: [filename.txt / filename.pdf on client workstation]
> Estimated Effort: ~Xh

---

## Book Details

| Field | Value |
|---|---|
| Title | |
| Author | |
| Tradition | Vedic / KP / Nadi / Numerology / Palmistry / Tarot / Western |
| Language | English / Sanskrit+English / Hindi+English |
| OCR Quality | High / Medium (note any known OCR issues) |
| File Location | `/Users/apple/Documents/[folder]/[filename]` |

---

## Extraction Scope

**Modules this book covers:**
- [ ] Kundali / Birth Chart
- [ ] Longevity & Health (Ayur Jyotish)
- [ ] Numerology
- [ ] Palmistry
- [ ] Tarot
- [ ] Daily / Weekly / Monthly Horoscope
- [ ] Cross-Science Combinations

**Categories to extract:**
- [ ] general
- [ ] career
- [ ] wealth
- [ ] relationships / marriage
- [ ] health
- [ ] education
- [ ] spirituality
- [ ] longevity

**Chapters / Sections in scope:**
> List specific chapters or sections to extract from. If the entire book is in scope, write "All chapters."

---

## Special Instructions

> Client's editorial notes -- how they want the content handled. Examples:
> - "Extract only the house-placement sections (Chapters 3-7). Skip the introductory theory."
> - "This book uses Western house numbering -- convert to Vedic (subtract 1)."
> - "Preserve all Sanskrit shlokas as secondary text alongside the English translation."
> - "Flag any rule that contradicts BPHS -- tag as `conflicts_with: BPHS` in the rule."
> - "Author's voice is modern_analytical -- assign that voice tone to all passages."

---

## Deliverables

1. `backend/data/LA-00X_[book_slug]_rules.json` -- extracted rules in standard schema
2. Import log: rules extracted, duplicates found, rules imported, rules flagged for review
3. Brief note on any anomalies encountered during extraction

---

## Process

1. Codex runs `backend/scripts/extract_book.py` locally against the OCR file
2. Output JSON reviewed by Codex before import (quality check)
3. JSON imported via `POST /api/knowledge/rules/import` with source metadata
4. Client reviews new rules in Library Console → Rules Browser + Test Console
5. Client approves or raises corrections
6. Amendment closed -- update `MEMORY.md` with book added and rule count

---

## Acceptance

- [ ] All in-scope chapters extracted
- [ ] Rules tagged to correct source, chapter, verse where available
- [ ] Author voice assigned correctly
- [ ] No blank or near-empty passages (< 100 words flagged for manual review)
- [ ] Duplicate detection run -- overlaps documented
- [ ] Test Console narrative verified with at least one sample chart
- [ ] Import history log shows correct batch entry in Library Console
