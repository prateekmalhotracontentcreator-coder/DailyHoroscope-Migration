# Daily Horoscope Prediction App - Product Requirements Document

## Original Problem Statement
Build a fully functional Daily Horoscope Prediction app with:
- AI-generated horoscopes refreshed daily
- Western astrology principles
- All 12 zodiac signs support
- Light/dark themes with Mustard, Yellow, Brown, Gold color palette
- Premium features: Kundali Milan and Birth Chart reports
- PDF download and sharing for reports
- Tiered access: Basic free, detailed premium
- Payment system (Razorpay) for per-report purchases and subscriptions
- Google OAuth authentication
- User account section with profile and plan details

## User Flow (Updated)
**🔓 Public Access (No Login Required):**
- Home page with all feature cards
- Daily Horoscope
- Weekly Horoscope  
- Monthly Horoscope

**🔐 Login Required (Premium Only):**
- Birth Chart Analysis
- Kundali Milan

## Tech Stack
- **Frontend:** React, react-router-dom, Tailwind CSS, Shadcn/UI, lucide-react
- **Backend:** FastAPI, Pydantic, Python-Jose (JWT)
- **Database:** MongoDB
- **AI:** OpenAI GPT-5.2 via Emergent LLM Key
- **Payments:** Razorpay (Test Mode)
- **Auth:** Google OAuth 2.0 (Emergent-managed) + JWT sessions
- **PDF:** fpdf2

## What's Been Implemented

### Core Features (Completed)
- [x] Daily/Weekly/Monthly AI-generated horoscopes for all 12 zodiac signs
- [x] Birth Chart Analysis - AI-powered Vedic astrology reports
- [x] Kundali Milan - Marriage compatibility analysis
- [x] PDF download functionality for premium reports
- [x] Share reports feature
- [x] Light/Dark theme toggle with gold color palette
- [x] Multi-page application structure with protected routes
- [x] **Public/Premium user flow** - Horoscopes free, premium features require login

### Authentication (Completed)
- [x] Google OAuth 2.0 login flow
- [x] Email/password registration and login
- [x] JWT-based session management
- [x] Protected routes for premium features only

### Payments (Completed)
- [x] Razorpay integration with test credentials
- [x] Per-report purchase flow (Birth Chart: ₹799, Kundali Milan: ₹1199)
- [x] Monthly subscription pricing defined (₹1599/month)
- [x] Payment order creation endpoint
- [x] Payment verification endpoint
- [x] Premium access check endpoint

### SEO Implementation (Completed)
- [x] Meta tags (title, description, keywords)
- [x] Open Graph tags for social sharing
- [x] Twitter Card meta tags
- [x] Structured data (JSON-LD) for WebSite and Service
- [x] robots.txt with crawl rules
- [x] sitemap.xml for all public pages
- [x] Canonical URLs

### Blog System (Completed)
- [x] Admin blog management (create, edit, delete posts)
- [x] Blog post editor with title, slug, excerpt, content, category, tags
- [x] Publish/unpublish toggle for draft management
- [x] Public blog listing page with category filtering
- [x] Individual blog post pages with share functionality
- [x] View counter for blog posts
- [x] Blog link added to home page

### UI/UX Enhancements (Completed)
- [x] Home page with feature cards (public)
- [x] Shared Header component with conditional Sign In / User Menu
- [x] User account dropdown menu showing plan details
- [x] Zodiac sign selection interface
- [x] **Enhanced Daily Horoscope UI:**
  - Today's date display header
  - Colored section boxes (General, Love, Career, Health, Lucky Elements)
  - Visual icons for each section
- [x] Report display components
- [x] Payment modal with Razorpay checkout
- [x] Loading states for AI generation

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - User logout
- `GET /api/auth/google/login` - Initiate Google OAuth
- `GET /api/auth/google/callback` - Google OAuth callback

### Horoscopes
- `GET /api/zodiac-signs` - List all zodiac signs
- `POST /api/horoscope/{sign}` - Generate horoscope (type: daily/weekly/monthly)

### Premium Reports
- `POST /api/profile/birth` - Create birth profile
- `GET /api/profile/birth/{id}` - Get birth profile
- `POST /api/birthchart/generate` - Generate birth chart report
- `GET /api/birthchart/{profile_id}` - Get existing birth chart
- `POST /api/kundali-milan/generate` - Generate compatibility report

### Payments
- `POST /api/payment/create-order` - Create Razorpay order
- `POST /api/payment/verify` - Verify payment
- `GET /api/premium/check` - Check premium access

### Sharing
- `POST /api/share/create` - Create share link
- `GET /api/share/{token}` - Get shared report
- `GET /api/download-pdf/{report_type}/{report_id}` - Download PDF

## Database Schema
- **users:** {email, name, google_id, password_hash, created_at}
- **birth_profiles:** {id, name, date_of_birth, time_of_birth, location, created_at}
- **birth_chart_reports:** {id, profile_id, report_content, generated_at}
- **kundali_milans:** {id, person1_id, person2_id, compatibility_score, detailed_analysis, generated_at}
- **payments:** {id, user_email, report_type, report_id, amount, razorpay_order_id, razorpay_payment_id, status, created_at}
- **subscriptions:** {id, user_email, subscription_type, status, expires_at, created_at}
- **share_links:** {id, token, report_type, report_id, views, created_at}

## Testing Status (Last: iteration_5.json)
- **Backend:** 95.6% pass rate
- **Frontend:** 100% pass rate
- **Overall:** 97.8%

## Backlog (Prioritized)

### P1 - High Priority (Next)
1. **Switch Razorpay to Live Mode** - Update from test to production keys for real payments
2. **Custom Domain Setup** - Connect a custom domain for branding

### P2 - Medium Priority
1. **Implement Subscription Flow UI** - Frontend for monthly premium subscription
2. **Email notifications** - Send welcome emails, payment confirmations

### P3 - Future Enhancements
1. Improve PDF sharing with direct cloud links
2. Account Settings & Payment History pages for users
3. Social media sharing buttons on blog posts
4. Newsletter subscription feature

## Last Updated
February 2026
