# Knowledge Engine -- Book Status
> Single-source progress tracker. Update when a book/chapter completes. Last updated: 2026-05-20

## Ingested Books

| Book | Chapters Covered | Total Rules | Auto-Approved | PHR + Flagged | Co-founder Review | Status |
|---|---|---|---|---|---|---|
| **BPHS Vol 1** | Ch 12-24, 27, 34, 35-40, 43, 44 | ~1,069 | ~628 | ~447 (352 PHR + 95 flagged) | -- | Ingested + Validated; PHR triage next |
| **BPHS Vol 2** | Ch 47, 48, 52-60 | ~2,227 | 1,092 | ~772 (582 PHR + 190 flagged) | -- | Ingested + Split-Upgrade + Validated; PHR triage pending |
| **A Text-Book of Astrology** | Ch 15, 16 | 1,659 | 589 | ~941 (639 PHR + 302 flagged) | -- | Ingested + Validated; PHR triage pending |
| **Lal Kitab** | Ch 19-28 | ~445 | ~275 | ~159 (149 PHR + 10 flagged) | -- | Ingested + Validated; PHR triage pending |
| **Mundane Astrology** (Gaur, Mehta, Rao, Gopalakrishnan, Raphael) | Gaur Ch 1,2,6,8,9,10,11 · Mehta Ch 2,7,8,18,22 · Rao · Gopal Ch 3,4,11,14 · Raphael Ch 8,14,22,26,27,28 | 328 rules + 102 specs | **326 approved** | 2 intentional holds | **7 rules tagged** | ✅ COMPLETE |
| **Jyotish Remedies & Mantras** | 100 Remedies (Book E) | 100 | 45 | 50 PHR | -- | Ingested + Validated; PHR triage pending |
| **Strategist Rules** | 22-record patch | 22 | **22 approved** | 0 | -- | ✅ Approved 2026-05-12; live in `knowledge_rules` |

## Decoded -- Awaiting Ingest (KE Freeze Blocking)

> These books are fully decoded and files are on disk. Ingest is blocked until KE Sprint 2 arbitration runtime delivers and the freeze lifts.

| Book | Chapters | Rules Extracted | Decode Status | Ingest Status | Open TT Decisions | Files |
|---|---|---|---|---|---|---|
| **Sarvato Bhadra Chakra V2** | Ch 2-18 (Ch 15/19/20 scoped out) | 181 rules | ✅ COMPLETE 2026-05-18 | ⛔ Blocked -- KE freeze | **7 blocking priority conflicts + 6 architecture/collection decisions** -- resolve before arbitration runtime built | `/New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/` -- 16 JSON + 16 Diagnostic + Master Summary + Testing Plan |
| **Longevity & Astro System** (KP) | Ch 4-58 (all chapters) | Ch6-19: full rules extracted; Ch20-58: benchmark log only | ✅ COMPLETE 2026-05-19 | ⛔ Blocked -- KE freeze | **Ch36-58 case study rules extraction** = separate Codex commission needed post-freeze. First ingest target = Ch5 aayu bucket rules. | `/Longevity_CC_Decode/` -- 14 decoded files + 2 benchmark files + Handover Summary |

### SBC Open Decisions (7 blocking + 6 architecture)

**Blocking priority conflicts (TT must resolve before arbitration runtime):**
| OQ | Conflict |
|---|---|
| OQ-08-01 | Drug Bala 100% override vs Combustion zero Kala -- which takes precedence? |
| OQ-08-02 | Santha Bala 100% override vs Combustion -- which takes precedence? |
| OQ-10-01 | Lagna Lord Exception 50% softening -- can it cancel a lethal signal from Timed Mortality Windows? |
| OQ-10-02 | 2-malefic pada convergence (death) vs strong benefic Panchaka aggregate -- which surfaces? |
| OQ-11-01 | Quad-Benefic Lock 100% success vs Lethal Star Index simultaneously firing -- which wins? |
| OQ-13-01 | Both countries combust simultaneously -- does defensive Varga veto still apply? |
| OQ-18-01 | Auxiliary chakra output conflicts main SBC grid -- resolution protocol not defined |

**Architecture/collection decisions (6 lookup datasets to be ingested separately):**
`vedha_coordinates` · `latta_coordinates` · `upgraha_coordinates` · `planet_significations` · `sbc_geopolitical_coordinates` · `sapt_salaka_coordinates`

### Longevity Open Items
- Ch36-58 benchmark case studies: rules extraction is a SEPARATE Codex commission (not yet briefed). Post-freeze.
- Ch4 + Ch5 decoded by Notebook LM -- separate folder, already in JSON-ready format.
- Ingest priority order: Ch5 aayu buckets → Ch6 general house traits → Ch7-18 lagna chapters → Ch19 method → Ch20-24 Balarishta → Ch25-35 case studies → Ch36-58 (pending commission).

## Books / Chapters Not Yet Ingested

| Book | Chapters Pending |
|---|---|
| **BPHS Vol 1** | Ch 1-11, 25-26, 28-33, 41-42, 45-46, 61+ |
| **BPHS Vol 2** | Ch 49-51 (**excluded** by co-founder decision); other remaining chapters |
| **A Text-Book of Astrology** | Ch 1-14, 17+ (no ingest script; RTF source needed) |
| **Lal Kitab** | Ch 29+ (confirm if remaining chapters exist) |

## Co-Founder Review Queue

### Mundane (7 rules -- approved & live, tagged for review)
Query: `col.find({"science_id":"mundane_jyotish","validation.cofounders_review_required":True})`

| Rule ID | Review Topic |
|---|---|
| `mundane-gaur-ch6-ownership-rain-confirm` | 24-48h timing window analyst-added |
| `gaur-ch8-gold-reserve-banking-crisis-veto` | "Sanghatta grid" = Mehta Ch8 term; triple condition = analyst synthesis |
| `gaur-ch10-jupiter-cancer-sun-aspect-supremacy` | "trine" = Western term; confirm Digvijay Yoga label |
| `mundane-mehta-ch22-saturn-dhanesh-treasury-depletion` | Dhanesh at Virgo ingress = Gaur Ch2 (not Mehta Ch22) |
| `mundane-gopal-ch3-widow-pm-multiplier` | +0.2 weight multiplier analyst-derived |
| `mundane-gopal-ch4-volatile-nomination-chart` | "2 or more planets" threshold analyst-derived |
| `mundane-gopal-ch11-rains-rahu-capricorn-moderate` | NE monsoon/Himalayan/J&K specifics analyst-added |

### Intentional PHR Holds (2 rules -- do not touch)
- `mundane-gopal-ch3-trikona-trikona-billionaire` -- natal rule misclassified as mundane
- `mundane-mehta-ch22-raja-mantri-enemy-deadlock` -- interpretive synthesis, not explicit Mehta text

## Validation Pipeline State
- `horoscope_db` -- all rules validated (zero `pending_review`) ✅
- `EverydayHoroscope` DB -- fully retired; all 3,796 rules deprecated ✅ Do not use.

## NLM Triage Priority
1. BPHS Ch 12-23 -- 13 contradiction pairs (highest priority)
2. BPHS Ch 12-23 -- worst PHR rules (Ch 15 low auto-approve 25%; Ch 19 at 33%)
3. BPHS Ch 35-40 yoga chapters -- Phase 2 yoga_check promotability audit
