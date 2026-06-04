# ContentClear -- AI Content Compliance SaaS
> Idea captured: 2026-06-04
> Origin: ECHO/PACE system built for EverydayHoroscope Angel Numbers module
> Status: PARKED -- revisit after EverydayHoroscope commission queue clears
> IP Note: Architecture, methodology, and all five test layers are authored and
> timestamped in this private repo. Do not share scripts publicly before filing.

---

## The Idea in One Sentence

A SaaS tool that scans AI-generated content corpora through five compliance
layers -- internal similarity, verbatim phrase repetition, heading duplication,
copyright proximity, and live Google indexation -- before the content goes live.

---

## Origin Story

Built organically while developing EverydayHoroscope's Angel Numbers module
(10,001 pages). The ECHO/PACE system was created to validate AI-generated SEO
content at scale. After running it successfully across multiple modules
(Angel Numbers, Lo Shu Grid, Tarot, Rudraksha, Crystal Healing, Faith Hubs),
the system proved capable of catching real failures before they reached
production -- including copyright proximity, Google duplicate signals, and
internal template repetition.

No commercial tool on the market covers all five layers in a single pipeline.
That is the gap.

---

## The Five-Layer System (already built and production-validated)

| Layer | Test | What It Catches |
|---|---|---|
| L1 | TF-IDF Cosine Similarity | Pages too similar to each other internally -- Google near-duplicate penalty risk |
| L2 | N-gram Phrase Match | Verbatim 4+ word phrases repeated across records -- mechanical template leakage |
| L3 | Jaccard Heading Overlap | Category labels and headings that repeat across pages -- thin content signal |
| Copyright | PDF Similarity (Test A/B/C) | Verbatim copying, structural paraphrasing, and sentence-level proximity vs reference PDFs used as AI source material |
| Layer G | Exact-match Serper / Google | Whether content already exists anywhere on the indexed web -- catches scraping, prior publication, and source leakage |

### Production Validation Record

| Module | Pages | L1 Result | Copyright | Layer G |
|---|---|---|---|---|
| Angel Numbers | 10,001 | PASS (39.9% worst) | PASS -- 0 breaches vs 2 PDFs | PASS -- 0/10 hits |
| Lo Shu Grid | 57 | PASS | Not run | PASS |
| Tarot SEO | 199 | PASS (strict) | Not run | PASS -- 15/15 queries |
| Rudraksha | 62 | PASS (25.2%) | Not run | PASS -- 0/8 hits |
| Crystal Healing | TBC | FAIL -- L2 100% | Not run | Blocked |
| Faith Hubs | TBC | FAIL -- L1 100% | Not run | Blocked |

The system has caught real failures in production conditions, not toy examples.

---

## Market Opportunity

### The Problem Every AI Content Business Has Right Now

Any business using AI to generate content at scale faces three risks they
currently cannot measure:

1. **SEO risk** -- Google penalises near-duplicate content. If pages are too
   similar to each other, they cannibalise each other and may be de-indexed.
2. **Legal risk** -- If the AI reproduced text from source PDFs or training
   data, the business has copyright exposure. Post-NYT vs. OpenAI, this is
   now a board-level conversation.
3. **Reputation risk** -- If a scraper has already published similar content,
   or if the content exists in the AI's training data, the business looks like
   the plagiarist even if they are the original author.

No single commercial tool (Copyscape, Grammarly, Semrush, Originality.ai)
answers all three risks in a unified pipeline.

### Target Customers

**Tier 1 -- Direct fit:**
- EdTech platforms (course descriptions, quiz explanations, lesson summaries)
- Legal-tech / finance-tech (regulatory explainers, product disclosures)
- Travel platforms (destination guides, hotel descriptions)
- Health and wellness apps (condition summaries, supplement guides)
- Astrology, tarot, numerology apps -- the exact vertical this was built for;
  dozens of competitors in this space, none with compliance tooling

**Tier 2 -- Adjacent:**
- Digital agencies running AI content pipelines for multiple clients
- SEO agencies validating AI output before client delivery
- Publishers migrating legacy print content to web via AI summarisation

---

## Competitive Differentiators

**1. Layer G is novel.**
The exact-match Serper phrase extraction approach does not exist in any
commercial tool. Copyscape checks against known databases. Layer G checks
whether the content exists *anywhere* on the live indexed web -- including
scrapers, prior publications, and sources the customer didn't know existed.

**2. Copyright test fills a real legal gap.**
Test A (verbatim 4-gram), Test B (TF-IDF cosine), Test C (Jaccard sentence)
against uploaded reference PDFs. Legal departments will pay for this directly,
especially companies that have fed proprietary documents to AI models.

**3. Unified pipeline.**
Every other tool is single-purpose. ContentClear is the only tool that covers
internal duplication AND external duplication AND copyright proximity in one run.

**4. Production-validated, not demo-ware.**
Tested on a live 10,001-page module. Caught real failures across multiple
content verticals. Not a proof of concept.

---

## Product Architecture (Proposed)

### Three Pricing Tiers

**Free**
- Up to 50 pages (plain text upload)
- L1, L2, L3 internal compliance only
- Pass/fail report with worst-pair scores
- No Serper, no copyright upload
- Goal: developer and small-team acquisition

**Pro -- $99/month**
- Up to 10,000 pages per scan
- All 5 layers including Layer G Serper (credit allowance included)
- Copyright PDF upload (up to 3 reference documents)
- Configurable thresholds
- JSON + PDF report export
- Goal: serious content businesses (apps, agencies, publishers)

**Enterprise -- Custom pricing**
- Unlimited pages
- CI/CD pipeline integration (scan on every content deploy; fail the build
  if thresholds breach -- this is the sticky, infrastructure-grade feature)
- White-label reports for agency resale
- Custom domain threshold presets (legal-tech needs tighter gates than travel)
- Dedicated Serper credit pool
- Legal-grade compliance certificate output
- Goal: enterprise content teams, regulated industries

### Core Engineering Work to Productise

The current implementation is corpus-specific (each script is written for a
specific data shape). A productised version needs:

1. **Generalised corpus ingestion** -- accept plain text, JSON, CSV, or URL
   list; extract body content automatically; identify natural clusters.
2. **Configurable threshold presets** -- per-domain defaults (legal, travel,
   wellness, astrology) with ability to override.
3. **REST API** -- `POST /scan` with corpus payload; async job with webhook
   on completion; `GET /report/{job_id}` for results.
4. **Privacy architecture for copyright uploads** -- PDFs processed in-memory,
   not stored; SOC2 posture needed for enterprise.
5. **Smart sampling for Layer G** -- at 50,000 pages, sampling strategy
   (diversity across clusters, worst-L1-pair prioritisation) becomes a core
   product decision to manage Serper costs.

---

## Key Risks to Solve Before Building

| Risk | Detail | Mitigation |
|---|---|---|
| Serper cost pass-through | Layer G costs ~$0.001 per query; at scale this adds up | Bundle Serper credits into Pro/Enterprise tier pricing; expose cost estimate before scan runs |
| Threshold calibration | 40% L1 gate works for astrology; legal-tech may need 20% | Build domain preset library; price domain pack additions |
| PDF privacy | Enterprise customers won't upload confidential docs without privacy guarantees | In-memory processing only; no logging of document content; SOC2 target |
| Corpus ingestion diversity | Current scripts assume structured Python generators; real customers have CSV/JSON/CMS exports | Generalised ingestion is the first engineering milestone |

---

## IP Protection Note

All five test layer methodologies, the sampling logic, the phrase extraction
window approach (tokens 5-13 from stop-filtered mid-body), the dual-axis
copyright test (PDF similarity + Google indexation), and the production
validation framework are documented and timestamped in this private repository.

**Action before any public launch:** File a provisional patent application or
at minimum a dated IP disclosure document with a lawyer before open-sourcing
or publishing any description of the system architecture.

---

## When to Revisit

Pick this up when:
- EverydayHoroscope active commission queue is clear (Crystal Healing, Faith
  Hubs, M3 fixes, KE ingest all resolved)
- EverydayHoroscope is generating consistent revenue (validation that the
  content compliance system works as a revenue driver before selling it)
- A potential co-founder or technical lead is identified to own the product
  build independently of EverydayHoroscope operations

**Estimated time to MVP (Free + Pro tiers):** 6-8 weeks of focused engineering.
**Estimated time to Enterprise (CI/CD integration):** Additional 4-6 weeks.

---

*Captured from session discussion 2026-06-04. Great times ahead.*
