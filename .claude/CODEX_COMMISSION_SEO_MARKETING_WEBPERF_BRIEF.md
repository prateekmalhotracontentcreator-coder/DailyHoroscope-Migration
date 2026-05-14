# SEO & MARKETING + WEBSITE PERFORMANCE OPTIMIZATION BRIEF

**Status:** New parallel session (non-cleanup track)  
**Date:** 30 April 2026  
**For:** Parallel delegation while main cleanup continues  
**Duration:** 3-5 days  
**Model:** Haiku or Sonnet (performance analysis needs detail)

---

## CONTEXT: EverydayHoroscope Project

**Product:** Premium Vedic astrology platform (https://www.everydayhoroscope.in)  
**Backend:** FastAPI on Render (https://everydayhoroscope-api.onrender.com)  
**Frontend:** React on Vercel  
**Database:** MongoDB (horoscope_db)  
**Go-Live Target:** Play Store + Web (payments live) -- 60 days

**Current state:**
- ✅ Core features live (Panchang, Horoscope, Tarot, Numerology, Kundali)
- ✅ 7 premium reports in testing (Arc Angel, Career Blueprint, Love Weather, etc.)
- 🔜 Premium subscription (Razorpay test keys live; waiting for live keys)
- 🔜 Android app (React Native build, not yet on Play Store)
- ✅ Google Search Console + Bing Webmaster verified
- ⚠️ No automated social media posting yet (manual only)

---

## TASK 1: SEO & MARKETING 30-DAY PLAN

### Deliverable: `docs/SEO_MARKETING_30DAY_PLAN.md`

Create a **week-by-week roadmap** to take the platform live and reach 500 signups in 30 days.

**Scope includes:**

#### Week 1: Technical SEO Foundation
- [ ] Audit current SEO metrics: Core Web Vitals (LCP, FID, CLS)
  - Use PageSpeed Insights, Lighthouse
  - Document baseline
  
- [ ] Implement structured data optimization
  - JSON-LD schema for:
    - Horoscope cards (article + ratingValue)
    - Birth chart (schema.org/Person + astrological properties)
    - Panchang calendar (Event schema for festivals)
  - Verify with Google Rich Results Test
  
- [ ] Create XML sitemap variations
  - `/sitemap-pages.xml` (main pages)
  - `/sitemap-horoscopes.xml` (daily horoscopes by sign)
  - `/sitemap-reports.xml` (premium reports)
  - Submit to GSC + Bing
  
- [ ] Set up analytics funnels
  - Free horoscope signup → premium upsell → payment
  - Track via GA4 events
  - Identify drop-off points

#### Week 2: Content & Keyword Strategy
- [ ] Keyword research
  - Primary: "Vedic astrology", "birth chart", "daily horoscope"
  - Long-tail: "career horoscope 2026", "love compatibility", "panchang today"
  - Local: "astrology for [city name]" (318 cities indexed)
  - Tools: Google Keyword Planner, Ahrefs (if available)
  
- [ ] On-page SEO optimization
  - Update meta descriptions (all pages)
  - Optimize OG tags for social sharing
  - Add alt text to all images (share cards, zodiac icons)
  
- [ ] Blog content plan
  - 3 SEO-optimized posts (500-1000 words each):
    1. "What is Vedic Astrology? Complete Beginner's Guide"
    2. "How to Read Your Kundali / Birth Chart"
    3. "Daily Panchang: Auspicious Timing Explained"
  - Internal linking strategy (blog → horoscope → premium reports)
  - Publication dates: stagger over 2 weeks
  
- [ ] Metadata refresh for cards
  - Horoscope share cards: add sign symbol + "2026 forecast"
  - Panchang cards: add date + location + auspicious/inauspicious badges

#### Week 3: Social Media & Influencer Outreach
- [ ] Facebook Page automation setup
  - Platform: Already connected (System User token on Render)
  - Schedule 6 AM daily posts:
    - Daily horoscope (all 12 signs)
    - Daily Panchang (location: New Delhi)
    - Weekly tips ("Mercury retrograde survival guide", etc.)
  - Tools: Use `/api/admin/facebook/schedule-post` endpoint (build if missing)
  
- [ ] YouTube Shorts automation
  - Setup: Already done (OAuth token stored)
  - Content: Share cards → MP4 (ffmpeg, 30s videos)
  - Schedule: 3× weekly (Mon/Wed/Fri at 6 AM)
  - Captions: Auto-generate (YouTube API)
  
- [ ] WhatsApp Business setup (blocked -- phone pending OTP)
  - Action: Complete phone verification on Meta
  - Template: `everydayhoroscope_update` (already approved)
  - Subscriber list: Import from MongoDB (subscribers collection)
  
- [ ] Email drip campaign (Resend API live)
  - Sequence 1 (Day 0-1): Welcome + free horoscope
  - Sequence 2 (Day 3): "See your premium reports"
  - Sequence 3 (Day 7): "Complete your birth chart"
  - Sequence 4 (Day 14): "Limited offer: 30% off premium"
  - Tracking: GA4 email campaign source
  
- [ ] Influencer outreach
  - Identify 10 astrology creators (YouTube, Instagram, TikTok)
  - Pitch: "Free premium access in exchange for 60-second review"
  - Target: 100K+ followers, India-focused
  - Tracking: UTM codes for each influencer

#### Week 4: App Launch & Conversion Optimization
- [ ] Android app finalization
  - Ensure app links to web (deep linking)
  - Configure in-app payments (Razorpay test)
  - Test end-to-end: signup → free report → upgrade
  - Play Store listing optimization:
    - Title: "EverydayHoroscope: Vedic Astrology & Birth Chart"
    - Description: Include keywords + unique selling points
    - Screenshots: Show horoscope + premium reports
    - Icon: Professional astrology symbol
  
- [ ] Landing page A/B tests
  - Variant A: "Free Daily Horoscope" CTA
  - Variant B: "Get Your Personalized Birth Chart" CTA
  - Run 1 week, measure conversion
  
- [ ] Payment funnel optimization
  - Test pricing tiers: $4.99/month vs. $9.99/month vs. $19.99/month
  - Highlight benefits: "Unlock all 27 reports"
  - Add trust badges: "10,000+ satisfied customers"
  - Track Razorpay conversion rate
  
- [ ] Analytics dashboard setup
  - Key metrics:
    - Free signups/day (target: 17/day → 500 in 30 days)
    - Premium conversions (target: 50 → 10% conversion rate)
    - App installs (target: 100)
    - Organic search traffic (target: 200 visitors/day by day 30)
  - Dashboard: Google Sheets + GA4 integration
  - Weekly reporting to Prateek

**Output format:**
```markdown
# SEO & MARKETING 30-DAY PLAN

## Week 1: Technical SEO Foundation
- [ ] Task 1.1 -- Detailed subtasks
  - Estimated effort: X hours
  - Tools needed: X
  - Success metric: X

...

## Launch Metrics (Target)
| Metric | Target | Current |
|---|---|---|
| Free signups | 500 | -- |
| Premium conversions | 50 | -- |
| App installs | 100 | -- |
| Organic daily visitors | 200 | -- |
```

---

## TASK 2: WEBSITE PERFORMANCE OPTIMIZATION

### Deliverable: `docs/WEBSITE_PERFORMANCE_OPTIMIZATION.md`

Audit the frontend and provide **concrete optimization recommendations with before/after metrics**.

**Scope includes:**

### Section 1: Core Web Vitals Analysis

**Run audits (use tools below):**
- [ ] Google PageSpeed Insights (mobile + desktop)
- [ ] WebPageTest (www.webpagetest.org)
- [ ] Chrome DevTools Lighthouse
- [ ] Record baseline metrics:

| Metric | Target | Current | Tool |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 0.5s | ? | Lighthouse |
| **FID** (First Input Delay) | < 100ms | ? | Lighthouse |
| **CLS** (Cumulative Layout Shift) | < 0.05 | ? | Lighthouse |
| **TTFB** (Time to First Byte) | < 0.6s | ? | WebPageTest |
| **JS size** | < 100KB | ? | Webpack Bundle Analyzer |
| **CSS size** | < 20KB | ? | PurgeCSS report |

### Section 2: Image Optimization

**Current issue:** Share cards exported as PNG (large files)

**Recommendations:**

1. **Convert all PNG → WebP**
   ```bash
   # Tool: cwebp or sharp (Node.js)
   # Impact: 50-70% size reduction
   # Target: All PanchangShareCard + HoroscopeShareCard outputs
   ```
   
2. **Lazy-load zodiac card images**
   ```jsx
   // Current: <img src="..."> (loads all 12 on page load)
   // Better: <img loading="lazy" src="...">
   // Impact: LCP improves by 0.3-0.5s
   ```
   
3. **Optimize horoscope card images**
   - Replace full PNG (900px wide) with responsive images
   - Use `<picture>` tag for WebP + PNG fallback
   - Impact: 40% bandwidth savings on mobile

**Action:** Audit `frontend/src/components/ShareCard.jsx` and image generation pipeline

### Section 3: Code Splitting & Lazy Loading

**Current issue:** React app loads all pages + components upfront

**Audit:**

1. **Identify non-critical pages**
   ```
   ✅ Critical (load immediately):
   - Home.jsx
   - Login.jsx
   - DailyHoroscope.jsx
   
   🔜 Can lazy-load:
   - admin/* (not needed on home)
   - LovePage.jsx (premium feature)
   - LuminaPage.jsx (new feature)
   - PalmistryPage.jsx (niche feature)
   ```

2. **Measure current JS bundle**
   ```bash
   # Tool: webpack-bundle-analyzer
   npm install --save-dev webpack-bundle-analyzer
   # Output: identify duplicate/unused packages
   ```

3. **Implement code splitting**
   ```jsx
   // Current: import AllPages from './pages'
   
   // Better: const AdminDashboard = React.lazy(() => import('./pages/admin/AdminDashboard'))
   // Wrap with Suspense fallback
   ```
   
   **Expected impact:** JS size: 400KB → 200KB (50% reduction)
   **LCP improvement:** 1.2s → 0.6s

### Section 4: CSS Optimization

**Current issue:** Tailwind full build (50KB+)

**Audit:**

1. **Check Tailwind config**
   ```bash
   # Look at: frontend/tailwind.config.js
   # Verify: purge/content is configured correctly
   ```

2. **Measure CSS size**
   ```bash
   # Build prod: npm run build
   # Check: frontend/build/static/css/main.*.css size
   # Expected: 8-15KB for Tailwind + custom
   # If >30KB: purge is not working
   ```

3. **Optimize unused styles**
   - Add PurgeCSS plugin if missing
   - Remove unused color variables from Tailwind
   - Consolidate custom CSS into `index.css`
   
   **Expected impact:** CSS: 50KB → 8KB (84% reduction)

### Section 5: API Response Optimization

**Current issue:** Rules library browser loads all 6000+ rules

**Audit:**

1. **Check `/api/interpretation_rules` endpoint**
   - Current: Returns entire collection (6000+ docs)
   - Issue: 3-5s load time, kills browser rendering
   
2. **Implement pagination**
   ```python
   # backend/routers/astrology_reports/library_router.py
   @router.get("/api/interpretation_rules")
   def get_rules(
       limit: int = 50,        # Default page size
       offset: int = 0,        # Pagination offset
       batch_id: str = None,   # Filter by source
       approval_status: str = None  # Filter by status
   ):
       # Return: { rules: [...], total: 6000, has_more: true }
   ```
   
   **Expected impact:** Load time: 3s → 0.3s

3. **Add caching headers**
   ```python
   # Cache rules for 1 hour (they don't change often)
   response.headers["Cache-Control"] = "public, max-age=3600"
   ```

### Section 6: Database Indexing

**Current issue:** MongoDB queries slow (no indexes optimized for queries)

**Audit:**

1. **Check existing indexes**
   ```bash
   # MongoDB command:
   db.interpretation_rules.getIndexes()
   ```

2. **Add missing indexes**
   ```javascript
   // Most-queried fields:
   db.interpretation_rules.createIndex({ "approval_status": 1 })
   db.interpretation_rules.createIndex({ "source.batch_id": 1 })
   db.interpretation_rules.createIndex({ "condition.dasha_lord": 1, "condition.antardasha_planet": 1 })
   
   // Composite index for Knowledge Engine queries:
   db.interpretation_rules.createIndex({ 
     "approval_status": 1,
     "source.book_id": 1,
     "condition.dasha_lord": 1
   })
   ```
   
   **Expected impact:** Query time: 500ms → 50ms

3. **Monitor query performance**
   - Enable MongoDB profiling
   - Identify slow queries (>100ms)
   - Create indexes for each

### Section 7: Render Backend Optimization

**Current issue:** Single container, no load balancing

**Audit:**

1. **Check current Render deployment**
   - Memory: 512MB? 1GB?
   - CPU: Shared or dedicated?
   - Concurrent requests: Limit unknown
   
2. **Load test**
   ```bash
   # Tool: Apache Bench or wrk
   ab -n 100 -c 10 https://everydayhoroscope-api.onrender.com/api/panchang/locations
   # Measure: Response time under concurrent load
   ```

3. **Scale if needed**
   - Add 2-3 containers behind load balancer (Render's native load balancing)
   - Cost: $15-20/month additional
   - Benefit: Handle 5× traffic, prevent downtime during spikes

### Section 8: Vercel Frontend Optimization

**Recommendations:**

1. **Enable incremental static generation (ISG)**
   - Pre-render critical pages (Home, PanchangPage)
   - Revalidate every 24 hours
   - Impact: Instant page loads from CDN

2. **Optimize build cache**
   - Vercel caches dependencies; ensure `.npmrc` includes cache headers
   - Impact: 30% faster builds on subsequent deploys

**Output format:**

```markdown
# WEBSITE PERFORMANCE OPTIMIZATION REPORT

## Current Baseline (Before)
| Metric | Value | Target | Gap |
|---|---|---|---|
| LCP | 1.2s | 0.5s | -0.7s ❌ |
| FID | 45ms | 100ms | +55ms ✅ |
| CLS | 0.08 | 0.05 | -0.03 ❌ |
| JS Size | 400KB | 150KB | -250KB ❌ |
| CSS Size | 50KB | 15KB | -35KB ❌ |

## Optimization Roadmap

### Priority 1: Image Optimization (Effort: 2 days | Impact: 0.3s LCP improvement)
- [ ] Convert PNG share cards → WebP
- [ ] Lazy-load zodiac icons
- Implementation: See [detailed steps]
- Expected result: LCP 1.2s → 0.9s

### Priority 2: Code Splitting (Effort: 1 day | Impact: 0.4s LCP improvement)
- [ ] Lazy-load admin pages
- [ ] Lazy-load love bundle
- Implementation: See [detailed steps]
- Expected result: JS size 400KB → 200KB; LCP 0.9s → 0.5s

### Priority 3: CSS Purging (Effort: 0.5 days | Impact: 0.05s improvement)
- [ ] Audit Tailwind config
- [ ] Run PurgeCSS
- Expected result: CSS 50KB → 8KB

### Priority 4: API Pagination (Effort: 1 day | Impact: 3s improvement on rules page)
- [ ] Add limit/offset to `/api/interpretation_rules`
- [ ] Implement client-side pagination
- Expected result: Rules page load 3s → 0.3s

### Priority 5: Database Indexing (Effort: 2 hours | Impact: 10× query speedup)
- [ ] Audit MongoDB indexes
- [ ] Create missing indexes
- Expected result: KE queries 500ms → 50ms

### Priority 6: Infrastructure (Effort: 4 hours | Cost: $20/mo | Impact: 5× traffic capacity)
- [ ] Scale Render to 3 containers
- [ ] Enable load balancing
- Expected result: Can handle 500-1000 concurrent users

## Post-Optimization Target (After)
| Metric | Value | Target | Status |
|---|---|---|---|
| LCP | 0.4s | 0.5s | ✅ |
| FID | 40ms | 100ms | ✅ |
| CLS | 0.04 | 0.05 | ✅ |
| JS Size | 150KB | 150KB | ✅ |
| CSS Size | 8KB | 15KB | ✅ |

## ROI
- **Effort:** ~1 week
- **Cost:** $20/mo infrastructure (optional)
- **Benefit:** 50% faster page loads → estimated 15-20% increase in conversions
```

---

## DELIVERABLES CHECKLIST

**For new session, produce:**

```
A) docs/SEO_MARKETING_30DAY_PLAN.md
   ├─ Week 1: Technical SEO (with GSC + schema setup steps)
   ├─ Week 2: Content & keywords (blog plan + keyword list)
   ├─ Week 3: Social + influencer (automation setup instructions)
   ├─ Week 4: App + conversion (Play Store + payment setup)
   └─ Target metrics dashboard (Google Sheets template)

B) docs/WEBSITE_PERFORMANCE_OPTIMIZATION.md
   ├─ Baseline metrics (from Lighthouse audit)
   ├─ 6 optimization strategies (with before/after impact)
   ├─ Priority roadmap (effort + ROI per task)
   ├─ Implementation checklists
   └─ Post-optimization target metrics
```

---

## RESOURCES & REFERENCE LINKS

**Project:**
- Live URL: https://www.everydayhoroscope.in
- Backend API: https://everydayhoroscope-api.onrender.com
- GitHub: https://github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration
- CLAUDE.md: `/CLAUDE.md` (product guide)
- Current status: `PROJECT_STATUS.md`

**Tools needed:**
- PageSpeed Insights: https://pagespeed.web.dev
- Lighthouse: Chrome DevTools (built-in)
- GA4: https://analytics.google.com (already set up)
- Google Search Console: https://search.google.com/search-console
- Razorpay dashboard: https://dashboard.razorpay.com (test mode)

**Key environment variables:**
- `REACT_APP_BACKEND_URL` (Vercel) -- points to Render API
- `MONGO_URL`, `DB_NAME` (Render) -- horoscope_db
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` (test keys active)
- `RESEND_API_KEY` (email service)
- `FACEBOOK_PAGE_ACCESS_TOKEN`, `YOUTUBE_CLIENT_ID` (social integrations)

**Data:**
- 318 locations catalogue: `/backend/panchang_router.py` (LOCATIONS dict)
- 12 zodiac signs: Standard (Aries-Pisces)
- 27 modules/features: Live (see PROJECT_STATUS.md)

**Key contacts for coordination:**
- Prateek (founder): Approval on pricing, messaging, Play Store launch timeline
- Codex: If new Codex briefs needed (currently paused for this track)

---

## COORDINATION WITH MAIN CLEANUP SESSION

**This session runs PARALLEL to:**
- Step 1: Repo code + structure review
- Step 2: Session chat extraction
- Step 3: Reconciliation

**Sync points:**
- Share final SEO/Marketing plan with main session (for Go-Live roadmap)
- Share perf optimization report with main session (for tech debt section)
- Both feed into final "PROGRESS_TRACKER.md" (deliverable A from main plan)

**Expected handoff:** By day 5-6 of this session, pass outputs to main session for integration into progress tracker.

---

## QUESTIONS BEFORE STARTING

1. Should the 30-day plan include A/B testing budget, or assume organic reach only?
2. For the Android app -- do you have React Native build already set up, or is that a separate task?
3. For Razorpay live keys -- is there a date you're targeting, or waiting for certain signups first?
4. Should I include "Android app testing" as part of the SEO/Marketing plan, or is that a separate session?

---

**Ready to hand off to new session?**
