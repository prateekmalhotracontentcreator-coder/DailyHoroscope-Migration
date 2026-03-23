# Bucket 10 — Play Store Setup Guide

## Overview
We use **TWA (Trusted Web Activity)** — wraps `everydayhoroscope.in` directly as a Play Store app.
No native code. No Android Studio. No SDK.

## Status
- [x] `manifest.json` — complete
- [x] PWA icons — `icon-192.png`, `icon-512.png` in `public/`
- [x] `assetlinks.json` — placeholder, needs real SHA-256
- [ ] Play Console account — needs creation
- [ ] SHA-256 fingerprint — needs copying from Play Console
- [ ] `bubblewrap` build — needs running on Mac
- [ ] AAB upload to Play Console — final step

---

## Step 1 — Create Play Console Account
1. Go to https://play.google.com/console
2. Sign in with your Google account
3. Pay ₹2,500 one-time developer fee
4. Accept developer agreement

---

## Step 2 — Create the App & Get SHA-256
1. Click **Create app**
2. App name: `Everyday Horoscope`
3. Default language: `English (India) - en-IN`
4. App or game: `App`
5. Free or paid: `Free`
6. Accept policies → **Create app**
7. In the left sidebar go to: **Release → Setup → App signing**
8. Copy the **SHA-256 certificate fingerprint** (looks like `AB:CD:EF:...`)
9. Paste it here in Claude — I'll update `assetlinks.json` immediately

---

## Step 3 — Update assetlinks.json
Once you paste the SHA-256, I update:
```
frontend/public/.well-known/assetlinks.json
```
Replace `REPLACE_WITH_SHA256_FROM_PLAY_CONSOLE` with your actual fingerprint.

Verify it's live at:
```
https://everydayhoroscope.in/.well-known/assetlinks.json
```

---

## Step 4 — Build TWA on Your Mac

### Prerequisites
```bash
# Install Node.js if not installed
brew install node

# Install bubblewrap CLI
npm install -g @bubblewrap/cli

# Install JDK 11 (required by bubblewrap)
brew install --cask temurin@11
```

### Initialise project
```bash
mkdir ~/everydayhoroscope-twa
cd ~/everydayhoroscope-twa
bubblewrap init --manifest https://everydayhoroscope.in/manifest.json
```

When prompted, use these values:
| Field | Value |
|---|---|
| Package ID | `in.everydayhoroscope.app` |
| App name | `Everyday Horoscope` |
| Launcher name | `EH Horoscope` |
| Display mode | `standalone` |
| Start URL | `/` |
| Theme colour | `#B8860B` |
| Background colour | `#fdf8ee` |
| Signing key path | (press Enter for default) |
| Signing key alias | `everydayhoroscope` |
| Min Android version | `19` |

### Build
```bash
bubblewrap build
```
This generates `app-release-signed.aab` in the project folder.

---

## Step 5 — Upload to Play Console
1. In Play Console → **Release → Production**
2. Click **Create new release**
3. Upload `app-release-signed.aab`
4. Release name: `1.0.0`
5. Release notes: `Everyday Horoscope — Free Vedic astrology, Panchang, birth chart and kundali milan`
6. Click **Save → Review release → Start rollout to Production**

---

## Step 6 — Store Listing

### Required assets
| Asset | Size | Notes |
|---|---|---|
| App icon | 512×512 PNG | Use `icon-512.png` from public/ |
| Feature graphic | 1024×500 PNG | Create in Canva — gold star on cream background |
| Phone screenshots | Min 2, max 8 | Take from live site at 390px viewport |
| Short description | Max 80 chars | `Free Vedic horoscope, Panchang & birth chart` |
| Full description | Max 4000 chars | See below |

### Full description (copy-paste ready)
```
Everyday Horoscope is your trusted daily companion for Vedic astrology — 
rooted in 5,000 years of ancient wisdom and interpreted for the modern world.

✦ DAILY, WEEKLY & MONTHLY HOROSCOPES
Personalised predictions for all 12 zodiac signs. Save your sign and get 
immediate results every time you open the app.

✦ VEDIC PANCHANG
Complete daily almanac — Tithi, Nakshatra, Yoga, Karana, Sunrise, Sunset, 
Rahu Kaal, Abhijit Muhurta and all timing windows. Monthly calendar view 
with observances. Full festival and vrat listing.

✦ BIRTH CHART (JANMA KUNDALI)
AI-powered Vedic birth chart with planetary positions, house analysis, 
dasha periods, yogas, and remedies — all from your date, time and place of birth.

✦ KUNDALI MILAN
Compatibility report for marriage — Ashtakoot Guna Milan with all 8 Kootas, 
Mangal Dosha assessment, and personalised guidance.

✦ BRIHAT KUNDLI PRO
Our most comprehensive report — 15+ sections covering career, marriage, health, 
wealth, dasha timeline, gemstone remedies and mantras.

✦ VEDIC NUMEROLOGY
Moolank (Life Path) and Bhagyank (Destiny) number calculator based on 
ancient Indian Ankjyotish.

All predictions are powered by real Jyotish calculations — not generic content.
```

### Category
`Lifestyle`

### Content rating
Run the content rating questionnaire — select `Everyone`.

---

## Notes
- TWA app will show no browser UI — full-screen like a native app
- Updates deploy automatically when Vercel deploys (no Play Store update needed for content changes)
- Only architecture/package changes need a new AAB upload
- App signing is managed by Google Play — keep your keystore file safe
