# EverydayHoroscope — Knowledge Engine Strategy
**Co-Founder Working Document**
Last updated: 14 April 2026

---

## 1. Objectives

### A. Build a Knowledge Base from Authentic Vedic Resources
Extract, structure, and store astrological logic from classical Vedic texts in a machine-readable format. The source books are the ground truth — every rule must be traceable to an authoritative text, not synthesised from a generic AI model.

### B. Cross-Book + Cross-Science Logic
Build a reconciled knowledge layer where rules from multiple books (e.g. BPHS + Lal Kitab + Phaladeepika) can be cross-referenced for the same condition (e.g. "Saturn in 7th house"). Where books agree → HIGH confidence. Where they contradict → surface for expert review. This enables zeroed-in predictions rather than generic outputs.

### C. Precise Sectional Inventory
Know exactly what each Vedic book covers — every Yoga, every planet × house combination, every Lagna characteristic, every Dasha rule. This is institutional knowledge that is otherwise scattered across Google, forums, and individual practitioners — impossible to query at scale.

### D. Narrative Templates for Premium Reports
Build reusable, structured narrative blocks (not just raw rules) that power consistent, fast Premium Report responses — Brihat Kundli, Ankjyotish, Career, Relationship, Karmic Debt reports. Goal: sub-second retrieval with minimal live API calls.

### E. Validate Logic via Classical Case Studies
The Vedic books include horoscopes of real, historically verifiable people (JFK, Swami Vivekananda, Mahatma Gandhi, Sanjay Gandhi, Nelson Mandela, etc.). Use these as a test bench — if our extracted rules correctly predict known outcomes for these charts, the logic is validated. This is our accuracy benchmark.

---

## 2. Phase 1 Books

| # | Book | Rules Extracted | Notes |
|---|---|---|---|
| 1 | A Text Book of Astrology | 167 | General principles, Yogas, transits |
| 2 | Lal Kitab | ~198 | Planet × House, remedies |
| 3 | Longevity & Astro System | 56 | Lagna-wise longevity, 30+ case studies |
| 4 | Brihat Parashara Hora Shastra (BPHS) | 313 | The foundational Vedic text — full coverage |
| 5 | Phaladeepika | 15 | Classical text, single-file extraction |
| 6 | 300 Important Horoscopes Vol-I | 22 | Case studies of famous charts |
| 7 | Longevity & Un-Natural Death | 4 | Badhaka, Maraca, case studies |
| 8 | 300 Important Combinations (BV Raman) | 171 | Named yogas, planetary combinations |
| | **Total** | **946** | All with approval_status = pending_review |

---

## 3. Issues Found in Phase 1 — OCR Pipeline

### 3a. Infrastructure & Environment Issues
| Issue | Impact | Status |
|---|---|---|
| Python 3.9 on macOS — `X \| None` syntax unsupported | Blocked ingest entirely | Fixed (eval_type_backport) |
| `OPENAI_API_KEY` not persisted across terminal sessions | All 948 rules stored as error placeholders | Fixed (re-ingest with key set) |
| `ANTHROPIC_API_KEY` missing for validation | All rules marked spot_check | Fixed |
| MongoDB URI with leading space | InvalidURI crash | Fixed |
| iCloud Drive — PDFs not downloaded locally | `[Errno 1] Operation not permitted` | Fixed (Download Now in Finder) |
| `python` vs `python3` on macOS | Command not found | Fixed |
| `pymongo`, `pydantic`, `eval_type_backport` missing | Import errors | Fixed |

### 3b. Extraction Quality Issues
| Issue | Impact | Root Cause |
|---|---|---|
| Truncated paraphrases | Incomplete rules (e.g. "achievements in fiel") | GPT-4o-mini hit token limit mid-sentence |
| Vague / empty conditions | 58% of rules flagged | `infer_condition()` falls back to composite `{}` when no planet/house/sign pattern detected |
| Duplicate rule IDs | Same ID, different content (e.g. 3× `R-ATEXTB-GEN-002`) | `build_rule_id()` resets sequence counter per chapter, not per book |
| Non-standard transliterations | "Molovyo" yoga, "Muthun" Lagna | OCR artefacts from scanned PDFs |
| Factual errors in paraphrase | "Libra ruled by Moon" (should be Venus) | GPT-4o-mini hallucination on OCR-garbled input |
| Low rule yield from case study chapters | 0–2 rules per chapter | Case study chapters contain chart data, not interpretive rules |
| `life_domain` always set to "relationships" | Incorrect metadata | `infer_categories()` defaulting without specific pattern detection |

### 3c. Validation Pipeline Issues
| Issue | Impact | Status |
|---|---|---|
| 100% flagged on first validation run | Claude saw "Extraction failed" text | Fixed — OpenAI key + re-ingest |
| Duplicate entries in validation report | Same rule validated multiple times | Cosmetic — does not affect counts |
| Silent `except Exception: return None` in OpenAI call | Failures invisible, placeholder rules stored | Fixed — now prints error message |

---

## 4. Validation Results — Phase 1 Dry Run

| Status | Count | % | Meaning |
|---|---|---|---|
| ✅ auto_approved | 190 | 20% | Clean, production-ready rules |
| 🔶 pending_human_review | 202 | 21% | Borderline — quick expert check needed |
| ⛔ flagged | 553 | 58% | Genuine issues — incomplete, vague, contradictory |
| ❌ rejected | 3 | 0% | Too short to evaluate |

**Key insight:** The 58% flag rate is not a failure of the validation engine — it accurately reflects the quality ceiling of OCR-extracted + AI-paraphrased content from scanned PDFs.

---

## 5. Strategic Decision — OCR Pipeline vs. Codex-Direct

### OCR Pipeline (current approach)
**Strengths:**
- Source fidelity — every rule traced to specific chapter/page/edition
- Captures nuanced or obscure rules that may not be in GPT's training data
- Automated at scale once working

**Weaknesses:**
- 58% flag rate — most output needs human review or rejection
- Multiple failure points (API keys, file permissions, Python versions, OCR artefacts)
- Expensive in time and compute for marginal quality output
- Paraphrase hallucinations introduced by GPT-4o-mini on garbled OCR text

### Codex-Direct (proposed new approach)
**Strengths:**
- GPT knows BPHS, Phaladeepika, Lal Kitab, and BV Raman's works deeply
- Zero OCR artefacts — clean, complete, structured output
- Section-wise organisation from the start (Planet × House matrix, Yoga catalogue, Lagna guide)
- Near-zero validation failures expected
- Free via Codex, fast turnaround

**Weaknesses:**
- Not tied to a specific edition/translation
- Risk of GPT synthesising rules not explicitly in the book
- Requires careful prompt engineering to stay within each book's scope

---

## 6. Agreed Next Steps

### Phase 1 — Complete Documentation (No Production Ingest Yet)

**Step i — Complete the book-by-book review**
- Run `review_approved.py` for each Phase 1 book
- Document what each book covers, its strengths, and extraction limitations
- Identify which books are suitable for Codex-direct vs. OCR pipeline

**Step ii — Build Codex Prompts for Sectional Inputs**
- Once we understand each book's coverage, commission Codex section-by-section:
  - *"Write all 108 Planet × House effects in Lal Kitab tradition (schema: JSON)"*
  - *"Write all Panch Mahapurusha Yogas from BPHS with formation rules and results"*
  - *"Write all 12 Lagna characteristics from Phaladeepika"*
  - *"Write all named Yogas from 300 Important Combinations by BV Raman"*
- Outputs drop directly into our MongoDB schema with correct IDs, conditions, and domains

**Step iii — Validate via Classical Case Studies**
- Use the real chart case studies in our books (JFK, Gandhi, Vivekananda, Mandela, etc.)
- Run each case study chart through our extracted rules
- Check: do the matched rules correctly describe the known life outcomes?
- Rules that pass case study validation → promote to HIGH confidence
- This is our accuracy proof before production

**Step iv — Build Cross-Reference Knowledge Base**
- After per-book validation, build the cross-book layer:
  - Index rules by condition (planet × house, Yoga, Lagna)
  - Flag where books agree (HIGH confidence) vs. disagree (REVIEW)
  - This becomes the reconciled, production-ready knowledge base

**Step v — Ingest into Live Production**
- Only after Steps i–iv complete for a book
- Deploy incrementally: BPHS first (most authoritative), then Lal Kitab, then others
- Each batch has a science_id and version — easy to roll back

**Step vi — Expand Continuously**
- Add Phase 2 books as new modules
- Each new book goes through the same review → Codex-direct → case study validation → cross-reference → ingest pipeline

---

## 7. Immediate Technical Fixes (Before Next Book Review)

| Fix | File | Description |
|---|---|---|
| Duplicate rule IDs | `extract_book.py` → `build_rule_id()` | Use book-wide sequence counter, not per-chapter |
| Silent OpenAI failures | `extract_book.py` → `paraphrase_with_openai()` | Already fixed — prints error message |
| `life_domain` always "relationships" | `extract_book.py` → `infer_categories()` | Improve domain detection patterns |

---

## 8. Knowledge Engine Architecture — Target State

```
Phase 1 Books (8)
      ↓
 [OCR Extract]         [Codex-Direct]
      ↓                      ↓
  Raw Rules              Structured Rules
      ↓                      ↓
  ┌─────────────────────────────┐
  │   Validation Pipeline       │
  │   Structural → Claude Haiku │
  │   → Contradiction Detection │
  └─────────────────────────────┘
              ↓
      Case Study Bench
   (JFK, Gandhi, Vivekananda...)
              ↓
    Cross-Reference Layer
  (Planet × House × Book matrix)
              ↓
   MongoDB: interpretation_rules
   approval_status = approved
              ↓
    Arc Angel API → Premium Reports
    Narrative Templates → Fast Response
```

---

## 9. Success Metrics

| Metric | Target |
|---|---|
| Rules in production (Phase 1) | ≥ 2,000 approved rules |
| Validation approval rate (Codex-direct) | ≥ 85% auto-approved |
| Case study accuracy | ≥ 80% correct prediction match |
| Premium report response time | < 500ms (template retrieval) |
| Cross-book coverage (Planet × House) | 100% of 108 combinations covered |

---

*Document owner: Prateek Malhotra + EverydayHoroscope AI Co-Founder*
*Next review: After Phase 1 book-by-book review complete*
