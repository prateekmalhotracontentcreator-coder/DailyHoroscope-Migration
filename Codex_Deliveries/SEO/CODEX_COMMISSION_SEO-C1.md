# Commission Brief: SEO-C1 -- Legal Pages Content

**Commission ID:** SEO-C1  
**Track:** C -- Feature Builds  
**Priority:** HIGHEST in Tier 2 -- Revenue Gate (Razorpay live key prerequisite)  
**Date:** 2026-05-20  
**Status:** ⚠️ PARTIALLY BUILT -- see note below  

---

## Status Note -- Read Before Starting

**The frontend and backend infrastructure for legal pages already exists:**

| Component | Status | Detail |
|---|---|---|
| Frontend routes | ✅ Live | `/terms`, `/privacy`, `/subscription-terms`, `/refund-policy`, `/cookie-policy` wired in App.js |
| Frontend component | ✅ Live | `frontend/src/pages/system/PolicyPage.jsx` -- fetches from API |
| Backend API (read) | ✅ Live | `GET /api/policies/{type}` -- reads from MongoDB `policies` collection |
| Backend API (write) | ✅ Live | `PUT /api/admin/policies/{type}` -- admin can update content |
| MongoDB collection | ⚠️ Unknown | `policies` collection -- may be empty; documents need to be populated |

**This commission is therefore a CONTENT task, not a build task.** Codex must populate the MongoDB `policies` collection with proper legal content via the admin API.

If the policies collection is empty, pages currently show a loading state or error. This must be fixed before Razorpay live keys can be activated (Razorpay requires visible, accessible legal pages).

---

## What Codex Must Do

### Step 1 -- Verify current state
Check whether policies are populated:
```
GET https://everydayhoroscope-api.onrender.com/api/policies/terms
GET https://everydayhoroscope-api.onrender.com/api/policies/privacy
GET https://everydayhoroscope-api.onrender.com/api/policies/refund-policy
```

If any returns 404 or "Policy not found" → that document needs to be created.

### Step 2 -- Populate content via PUT calls
Use the admin endpoint:
```
PUT /api/admin/policies/{type}
Body: { "type": "{type}", "title": "...", "content": "..." }
```

### Step 3 -- Verify pages are live and readable
Check that all 5 policy URLs return visible content.

---

## Required Policies

### 1. Terms of Service (`type: "terms"`)
**Title:** Terms of Service  
**Key sections required by Razorpay:**
- Company identity (EverydayHoroscope, operated by [your company name])
- Service description (astrology platform, digital content, premium subscription)
- User eligibility (18+)
- Account registration
- Subscription plans and billing
- Premium features description
- Prohibited conduct
- Intellectual property
- Disclaimer (astrology is for entertainment/guidance, not professional advice)
- Limitation of liability
- Governing law (India, jurisdiction: [your city])
- Contact information

### 2. Privacy Policy (`type: "privacy"`)
**Title:** Privacy Policy  
**Key sections required by Razorpay + Google Play:**
- Data collected (name, email, DOB for chart, payment data via Razorpay)
- How data is used (personalization, account management)
- Data sharing (Razorpay for payments, no sale of personal data)
- Data retention
- User rights (access, deletion)
- Cookies
- Children's privacy (no users under 13)
- Contact for privacy queries

### 3. Refund & Cancellation Policy (`type: "refund-policy"`)
**Title:** Refund & Cancellation Policy  
**Key sections required by Razorpay (MANDATORY for live keys):**
- Subscription cancellation: user can cancel anytime; access continues until period end
- Refund eligibility: refunds within 7 days of purchase if service not accessed
- Non-refundable items: individual reports once generated/downloaded
- Process: email support@everydayhoroscope.in with order ID
- Processing time: 5-7 business days
- Contact details

### 4. Subscription Terms (`type: "subscription-terms"`)
**Title:** Subscription Terms  
**Key sections:**
- Plans available (monthly/annual)
- Auto-renewal disclosure (MANDATORY)
- Cancellation before renewal
- Price changes notice
- Free trial terms (if applicable)

### 5. Cookie Policy (`type: "cookie-policy"`)
**Title:** Cookie Policy  
**Key sections:**
- Types of cookies used (essential, analytics/GA4, preferences)
- How to opt out
- Third-party cookies (Google Analytics)

---

## Content Format

The `PolicyPage.jsx` component renders content from the API response. Check what fields the component expects:

Looking at `frontend/src/pages/system/PolicyPage.jsx` -- it fetches:
```javascript
const res = await axios.get(`${API}/policies/${type}`);
setPolicy(res.data);
```

The component then renders `policy.content` (HTML string or markdown). Confirm the exact field name by reading the full PolicyPage component.

Supply content as clean HTML or structured JSON -- whichever the component renders. Use clear headings (`<h2>`, `<h3>`), paragraphs (`<p>`), and lists (`<ul>`).

---

## SEO Requirements (for PolicyPage.jsx -- Claude Code handles these post-integration)

Each policy page should have:
- `<title>`: e.g. `Terms of Service | EverydayHoroscope`
- `<meta name="description">`: one-line summary of the policy
- `<meta name="robots" content="noindex">` -- legal pages should NOT be indexed by Google (they are not SEO pages; indexing thin legal content hurts quality score)

**Claude Code will add these meta tags to PolicyPage.jsx after Codex delivers the content.**

---

## Razorpay Compliance Checklist

Before requesting Razorpay live keys, these must all be true:
- [ ] `/terms` -- loads with Terms of Service content
- [ ] `/privacy` -- loads with Privacy Policy content
- [ ] `/refund-policy` -- loads with Refund & Cancellation Policy (explicit 7-day refund policy)
- [ ] Refund policy is **publicly accessible** (no login required) -- currently this is satisfied
- [ ] Company name and contact email visible on at least one policy page
- [ ] Pages are not behind a paywall

---

## What Claude Code Handles After Codex Delivers

1. Add `<meta name="robots" content="noindex, nofollow">` to PolicyPage.jsx
2. Add unique `<title>` and `<meta description>` per policy type to PolicyPage.jsx
3. Verify all 5 policy URLs load correctly on production
4. Confirm Razorpay live key requirements are met

---

## Acceptance Criteria

- [ ] All 5 policy URLs return content (not error/loading state)
- [ ] Refund Policy clearly states cancellation and refund eligibility
- [ ] Privacy Policy names Google Analytics and Razorpay as data processors
- [ ] Terms of Service includes subscription billing terms
- [ ] All content is readable (not broken HTML)
- [ ] No login required to view any policy page
