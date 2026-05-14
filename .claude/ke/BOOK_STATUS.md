# Knowledge Engine — Book Status
> Single-source progress tracker. Update when a book/chapter completes. Last updated: 2026-05-13

## Ingested Books

| Book | Chapters Covered | Total Rules | Auto-Approved | PHR + Flagged | Co-founder Review | Status |
|---|---|---|---|---|---|---|
| **BPHS Vol 1** | Ch 12–24, 27, 34, 35–40, 43, 44 | ~1,069 | ~628 | ~447 (352 PHR + 95 flagged) | — | Ingested + Validated; PHR triage next |
| **BPHS Vol 2** | Ch 47, 48, 52–60 | ~2,227 | 1,092 | ~772 (582 PHR + 190 flagged) | — | Ingested + Split-Upgrade + Validated; PHR triage pending |
| **A Text-Book of Astrology** | Ch 15, 16 | 1,659 | 589 | ~941 (639 PHR + 302 flagged) | — | Ingested + Validated; PHR triage pending |
| **Lal Kitab** | Ch 19–28 | ~445 | ~275 | ~159 (149 PHR + 10 flagged) | — | Ingested + Validated; PHR triage pending |
| **Mundane Astrology** (Gaur, Mehta, Rao, Gopalakrishnan, Raphael) | Gaur Ch 1,2,6,8,9,10,11 · Mehta Ch 2,7,8,18,22 · Rao · Gopal Ch 3,4,11,14 · Raphael Ch 8,14,22,26,27,28 | 328 rules + 102 specs | **326 approved** | 2 intentional holds | **7 rules tagged** | ✅ COMPLETE |
| **Jyotish Remedies & Mantras** | 100 Remedies (Book E) | 100 | 45 | 50 PHR | — | Ingested + Validated; PHR triage pending |
| **Strategist Rules** | 22-record patch | 22 | **22 approved** | 0 | — | ✅ Approved 2026-05-12; live in `knowledge_rules` |

## Books / Chapters Not Yet Ingested

| Book | Chapters Pending |
|---|---|
| **BPHS Vol 1** | Ch 1–11, 25–26, 28–33, 41–42, 45–46, 61+ |
| **BPHS Vol 2** | Ch 49–51 (**excluded** by co-founder decision); other remaining chapters |
| **A Text-Book of Astrology** | Ch 1–14, 17+ (no ingest script; RTF source needed) |
| **Lal Kitab** | Ch 29+ (confirm if remaining chapters exist) |

## Co-Founder Review Queue

### Mundane (7 rules — approved & live, tagged for review)
Query: `col.find({"science_id":"mundane_jyotish","validation.cofounders_review_required":True})`

| Rule ID | Review Topic |
|---|---|
| `mundane-gaur-ch6-ownership-rain-confirm` | 24–48h timing window analyst-added |
| `gaur-ch8-gold-reserve-banking-crisis-veto` | "Sanghatta grid" = Mehta Ch8 term; triple condition = analyst synthesis |
| `gaur-ch10-jupiter-cancer-sun-aspect-supremacy` | "trine" = Western term; confirm Digvijay Yoga label |
| `mundane-mehta-ch22-saturn-dhanesh-treasury-depletion` | Dhanesh at Virgo ingress = Gaur Ch2 (not Mehta Ch22) |
| `mundane-gopal-ch3-widow-pm-multiplier` | +0.2 weight multiplier analyst-derived |
| `mundane-gopal-ch4-volatile-nomination-chart` | "2 or more planets" threshold analyst-derived |
| `mundane-gopal-ch11-rains-rahu-capricorn-moderate` | NE monsoon/Himalayan/J&K specifics analyst-added |

### Intentional PHR Holds (2 rules — do not touch)
- `mundane-gopal-ch3-trikona-trikona-billionaire` — natal rule misclassified as mundane
- `mundane-mehta-ch22-raja-mantri-enemy-deadlock` — interpretive synthesis, not explicit Mehta text

## Validation Pipeline State
- `horoscope_db` — all rules validated (zero `pending_review`) ✅
- `EverydayHoroscope` DB — fully retired; all 3,796 rules deprecated ✅ Do not use.

## NLM Triage Priority
1. BPHS Ch 12-23 — 13 contradiction pairs (highest priority)
2. BPHS Ch 12-23 — worst PHR rules (Ch 15 low auto-approve 25%; Ch 19 at 33%)
3. BPHS Ch 35-40 yoga chapters — Phase 2 yoga_check promotability audit
