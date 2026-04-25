# Codex Commission Brief — Live TV: Sai Baba Arti
> Version 1.1 | 25 April 2026 | EverydayHoroscope
> YouTube Channel: https://www.youtube.com/@SkyHoundStudios

---

## 1. Overview

Build a **Live Sai Baba Arti** experience comprising three parts:

1. **Video Generation Pipeline** — ffmpeg assembles a 60-minute looping Sai Baba Arti video from multiple source clips/images with crossfade transitions, then uploads to the @SkyHoundStudios YouTube channel via the existing YouTube Data API integration
2. **Live TV Panel** — a viewport-fixed, always-playing embedded video panel in the **top-right corner of the Home page only**
3. **SEO Full-Screen Page** — a standalone `/live-sai-baba-arti` page with a full-screen immersive player, optimised for organic search on "Live Sai Baba Arti"

Future videos (other deities, other artis) slot into the same infrastructure via Admin Console — this commission builds the foundation.

---

## 2. Video Generation Pipeline

### Source Material
The commission assumes the following source files will be provided before the pipeline runs.
All files placed in `backend/assets/live_tv/sai_baba/` before running the generation script.

**Visual sources (provide any combination — more = richer video):**
- 5–8 images or short AI-generated clips of Shirdi Sai Baba, temple arti flame, diya, Shirdi temple exterior, devotees in prayer
- Recommended: generate 10–15 sec clips using Pika Labs / Kling AI with prompt *"Sai Baba temple arti, flickering diya flame, devotional atmosphere, warm golden light, cinematic slow motion"*
- Accepted formats: `.jpg`, `.png`, `.mp4` — the script handles both

**Audio source:**
- `sai_baba_arti.mp3` — the Sai Baba Arti audio track

### Video Spec
| Parameter | Value |
|---|---|
| Resolution | 1920×1080 (Full HD) |
| Duration | 60 minutes (audio looped to fill) |
| Format | MP4, H.264, AAC audio |
| ffmpeg preset | `-preset veryfast -crf 18 -threads 1` (matches existing YouTube pipeline) |
| Frame rate | 25fps |
| Aspect ratio | 16:9 |
| Transitions | Crossfade (xfade filter) between visual sources, 2-second blend |

### ffmpeg Command — Slideshow with Crossfades (backend generates this)
```bash
# Step 1: Build input list — each image shown for 8 seconds, crossfade 2s between
# Script auto-detects whether each source is image or video clip and constructs
# the correct ffmpeg filter_complex chain

# Example for 5 images:
ffmpeg \
  -loop 1 -t 10 -i img1.jpg \
  -loop 1 -t 10 -i img2.jpg \
  -loop 1 -t 10 -i img3.jpg \
  -loop 1 -t 10 -i img4.jpg \
  -loop 1 -t 10 -i img5.jpg \
  -stream_loop -1 -i sai_baba_arti.mp3 \
  -filter_complex "
    [0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v0];
    [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v1];
    [2:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v2];
    [3:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v3];
    [4:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[v4];
    [v0][v1]xfade=transition=fade:duration=2:offset=8[x1];
    [x1][v2]xfade=transition=fade:duration=2:offset=16[x2];
    [x2][v3]xfade=transition=fade:duration=2:offset=24[x3];
    [x3][v4]xfade=transition=fade:duration=2:offset=32[out]
  " \
  -map "[out]" -map 5:a \
  -t 3600 \
  -c:v libx264 -preset veryfast -crf 18 -threads 1 \
  -c:a aac -b:a 192k \
  -shortest \
  output_sai_baba_arti_60min.mp4

# The generation script loops the slideshow segment to fill 60 minutes automatically
```

### Backend Script: `backend/scripts/generate_live_tv_video.py`
```
Args:
  --image-path   Path to source image
  --audio-path   Path to source audio
  --duration     Duration in seconds (default: 3600)
  --title        YouTube video title
  --description  YouTube video description
  --upload       Flag: if set, upload to YouTube after generation
  --dry-run      Generate but do not upload

Output:
  Generates MP4 in backend/assets/live_tv/output/
  If --upload: calls existing YouTube Data API v3 upload pipeline
```

### YouTube Upload Metadata
```
Title:        "🙏 LIVE Sai Baba Arti | Om Sai Ram | EverydayHoroscope"
Description:  "Live Sai Baba Arti playing 24/7 on EverydayHoroscope — India's premium Vedic astrology platform.
               🙏 Om Sai Ram | Sai Baba Aarti | Daily Blessings
               Visit us at https://www.everydayhoroscope.in/live-sai-baba-arti
               #SaiBaba #ArtiLive #OmSaiRam #EverydayHoroscope #VedicAstrology"
Tags:         ["Sai Baba", "Arti", "Live", "Om Sai Ram", "Sai Baba Aarti", "EverydayHoroscope"]
Category:     22 (People & Blogs) or 24 (Entertainment)
Privacy:      Public
```

### MongoDB: `live_tv_videos` collection
```json
{
  "video_id": "uuid",
  "youtube_video_id": "xxxxxxxxxxx",
  "youtube_url": "https://www.youtube.com/watch?v=xxxxxxxxxxx",
  "youtube_embed_url": "https://www.youtube.com/embed/xxxxxxxxxxx",
  "title": "LIVE Sai Baba Arti",
  "deity": "Sai Baba",
  "arti_type": "morning | evening | general",
  "is_active": true,
  "display_order": 1,
  "duration_seconds": 3600,
  "generated_at": "ISO timestamp",
  "uploaded_at": "ISO timestamp",
  "thumbnail_url": "string"
}
```

---

## 3. Live TV Panel (Home Page Only)

### Component: `frontend/src/components/LiveTVPanel.jsx`

A viewport-fixed panel anchored to the **top-right corner**, visible only on the **Home page** (`/`). It stays in place as the user scrolls.

### Visual Design
```
                              ┌─────────────────────────────┐
                              │ 🔴 LIVE  Sai Baba Arti  [─][⛶]│
                              │ ┌─────────────────────────┐  │
                              │ │                         │  │
                              │ │  [YouTube embed player] │  │
                              │ │                         │  │
                              │ └─────────────────────────┘  │
                              │ 🔇 Unmute  ·  ⛶ Full Screen  │
                              └─────────────────────────────┘
```

- **Width**: 300px
- **Position**: `fixed top-20 right-4 z-50` (top-20 = 80px — clears the navbar)
- **Header bar**: Gold gradient, `🔴 LIVE` pulsing red dot, "Sai Baba Arti" title, minimise `—` and fullscreen `⛶` buttons
- **Player**: YouTube iframe embed, 16:9 ratio (300×169px)
- **Autoplay**: `autoplay=1&mute=1` — browser-compliant, starts muted automatically
- **Unmute button**: "🔇 Unmute" — user clicks to enable audio via YouTube iframe API postMessage
- **Full Screen button**: navigates to `/live-sai-baba-arti` (the dedicated SEO page)
- **Persistence**: minimised/closed state saved to `localStorage`; closed resets after 24 hours

### Embed URL Format
```
https://www.youtube.com/embed/{youtube_video_id}?autoplay=1&mute=1&loop=1&playlist={youtube_video_id}&rel=0&modestbranding=1&enablejsapi=1
```

`loop=1&playlist={id}` — loops indefinitely, no related videos at end.
`enablejsapi=1` — required for iframe API unmute control.

### Panel States
| State | Behaviour |
|---|---|
| Open (default on Home) | Full panel visible, autoplaying muted |
| Minimised | Header bar only (48px), video pauses |
| Closed | Hidden, reappears after 24 hours |

### Integration — Home Page Only
```jsx
// In frontend/src/pages/HomePage.jsx (or equivalent home route component):
import LiveTVPanel from '../components/LiveTVPanel';

// Inside return:
<LiveTVPanel />

// Do NOT add to App.js — panel renders only within the Home page component
```

The panel fetches the active video from `GET /api/live-tv/active` on mount. If no active video is configured, the panel does not render.

---

## 4. SEO Full-Screen Page

### Route: `/live-sai-baba-arti`
### File: `frontend/src/pages/LiveSaiBabaArtiPage.jsx`

### Page Purpose
A standalone, immersive, full-screen SEO page that:
- Ranks organically for "Live Sai Baba Arti", "Sai Baba Arti online", "Om Sai Ram live"
- Provides a premium devotional experience — the video is the centrepiece, not a sidebar
- Drives return traffic (bookmarkable, shareable)

### Page Layout
```
┌────────────────────────────────────────────────────────────────┐
│  [EverydayHoroscope nav — minimal, dark overlay style]         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ╔══════════════════════════════════════════════════════════╗  │
│  ║                                                          ║  │
│  ║                                                          ║  │
│  ║         YOUTUBE PLAYER — full viewport width            ║  │
│  ║              16:9, ~75vh height                         ║  │
│  ║                                                          ║  │
│  ║  🔴 LIVE SAI BABA ARTI          🔇 Unmute  📱 Share  ║  │
│  ╚══════════════════════════════════════════════════════════╝  │
│                                                                │
│  H1: 🙏 Live Sai Baba Arti — Om Sai Ram                      │
│  Subheading: Continuous arti, 24/7 blessings                  │
│                                                                │
│  ┌──────────────────────┐  ┌───────────────────────────────┐  │
│  │  Arti Lyrics         │  │  About Shirdi Sai Baba        │  │
│  │  (Hindi + English)   │  │  (200 words SEO content)      │  │
│  └──────────────────────┘  └───────────────────────────────┘  │
│                                                                │
│  [More Divine Content — Panchang, Daily Horoscope, other artis]│
│  [Footer]                                                      │
└────────────────────────────────────────────────────────────────┘
```

**Player specifics:**
- `width: 100vw` — edge to edge
- `height: 75vh` — dominates the viewport
- Autoplay muted on load, unmute button prominent
- On mobile: `height: 56vw` (maintains 16:9)
- Custom overlay: gold "🔴 LIVE SAI BABA ARTI" badge bottom-left of player

### SEO Implementation (use existing `SEO.jsx` component)
```jsx
<SEO
  title="Live Sai Baba Arti | Om Sai Ram | EverydayHoroscope"
  description="Watch Sai Baba Arti live 24/7 on EverydayHoroscope. Experience divine blessings with continuous Sai Baba Aarti. Om Sai Ram. Free spiritual content."
  keywords="Sai Baba Arti live, Om Sai Ram, Sai Baba Aarti online, live arti, daily arti"
  canonical="https://www.everydayhoroscope.in/live-sai-baba-arti"
/>
```

### JSON-LD Schema (add to page)
```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Live Sai Baba Arti | Om Sai Ram",
  "description": "Continuous live Sai Baba Arti playing 24/7. Experience divine blessings.",
  "thumbnailUrl": "{thumbnail_url_from_youtube}",
  "uploadDate": "{generated_at}",
  "contentUrl": "https://www.youtube.com/watch?v={youtube_video_id}",
  "embedUrl": "https://www.youtube.com/embed/{youtube_video_id}",
  "publisher": {
    "@type": "Organization",
    "name": "EverydayHoroscope",
    "url": "https://www.everydayhoroscope.in"
  }
}
```

### Arti Lyrics Content (hardcoded on page — SEO value)
Include full Sai Baba Arti text:
- Hindi: "Arti Sai Baba, Soham Devanand..."
- English transliteration below each line
- English translation as a collapsible section
This is original textual content that helps page rank for "Sai Baba Arti lyrics" queries.

---

## 5. Backend API Endpoints

### File: `backend/live_tv_router.py`
Register in `server.py`: `app.include_router(live_tv_router, prefix="/api/live-tv")`

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/live-tv/active` | Returns the currently active video (for side panel) |
| GET | `/api/live-tv/videos` | Returns all uploaded videos |
| POST | `/api/admin/live-tv/generate` | Trigger video generation + upload (background task) |
| GET | `/api/admin/live-tv/status` | Check generation/upload status |
| PATCH | `/api/admin/live-tv/videos/{id}/activate` | Set a video as the active one |

### `GET /api/live-tv/active` response:
```json
{
  "youtube_video_id": "xxxxxxxxxxx",
  "youtube_embed_url": "https://www.youtube.com/embed/xxxxxxxxxxx?autoplay=1&mute=1&loop=1&playlist=xxxxxxxxxxx&rel=0&modestbranding=1",
  "title": "Live Sai Baba Arti",
  "deity": "Sai Baba",
  "is_live": true
}
```

---

## 6. Admin Console Integration

Add a **"Live TV"** tab to the Admin Console (`/admin/dashboard`):

**Sub-tabs:**
- **Generate** — upload image + audio → trigger generation → progress indicator → auto-upload to YouTube
- **Videos** — list of all uploaded videos, set active, view YouTube analytics link
- **Settings** — panel auto-show delay (currently 24h), panel default state

**Generate form fields:**
- Deity name (text)
- Arti type (Morning / Evening / General)
- Image upload
- Audio upload
- Video duration (30 min / 60 min / 120 min)
- YouTube title + description (pre-filled, editable)
- [Generate & Upload] button → triggers `POST /api/admin/live-tv/generate` as background task
- Progress: "Generating..." → "Uploading..." → "Live ✅"

---

## 7. Sitemap & Discoverability

Add to `frontend/public/sitemap.xml`:
```xml
<url>
  <loc>https://www.everydayhoroscope.in/live-sai-baba-arti</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>
```

Add to React Router in `App.js`:
```jsx
<Route path="/live-sai-baba-arti" element={<LiveSaiBabaArtiPage />} />
```

---

## 8. Tech Stack & Constraints

- **Video generation**: ffmpeg (already in Dockerfile) — same `-preset veryfast -threads 1` settings as YouTube share card pipeline
- **YouTube upload**: Existing `youtube_upload` pipeline in `server.py` — reuse the refresh token flow, do NOT create new OAuth flow
- **Frontend**: React 18, Tailwind CSS, Temple App theme tokens (`bg-card`, `text-gold`, `border-gold/20`)
- **Autoplay policy**: Always use `mute=1` in embed URL — unmute is user-initiated only (browser requirement)
- **YouTube embed loop**: Use `loop=1&playlist={video_id}` — this is the correct YouTube embed loop syntax
- **Background task**: Video generation uses FastAPI `BackgroundTasks` — same pattern as existing YouTube upload (returns immediately, client polls status)
- **No ffmpeg blocking**: Generation must run as background task — never block the request thread
- **Render health check**: ffmpeg with `-threads 1 -preset veryfast` keeps encode under 60s for 60min still-image video — safe for Render's 30s health check window

---

## 9. Future Expansion (Do Not Build Now — Design Must Accommodate)

The `live_tv_videos` collection and admin panel should be designed so that adding a second deity (e.g., Ganesh Vandana, Hanuman Chalisa) requires only:
1. Admin uploads image + audio → generates new video → uploads to YouTube
2. Admin sets new video as active OR adds to rotation playlist
3. No code changes required

A future "playlist rotation" feature will cycle through all active videos in `display_order` sequence. Design the data model to support `is_active` as a list of active video IDs, not a single ID, for when rotation is needed.
