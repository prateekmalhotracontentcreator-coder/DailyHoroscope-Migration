# Codex Commission Brief — Live TV: Sai Baba Arti
> Version 1.0 | 25 April 2026 | EverydayHoroscope
> YouTube Channel: https://www.youtube.com/@SkyHoundStudios

---

## 1. Overview

Build a **Live Sai Baba Arti** experience comprising three parts:

1. **Video Generation Pipeline** — ffmpeg generates a 60-minute looping Sai Baba Arti video and uploads it to the @SkyHoundStudios YouTube channel via the existing YouTube Data API integration
2. **Live TV Side Panel** — a floating, always-playing embedded video panel on the EverydayHoroscope home page
3. **SEO Landing Page** — a standalone `/live-sai-baba-arti` page optimised for organic search traffic on the keyword "Live Sai Baba Arti"

Future videos (other deities, other artis) will slot into the same infrastructure via Admin Console — this commission builds the foundation.

---

## 2. Video Generation Pipeline

### Source Material
The commission assumes the following source files will be provided before the pipeline runs:
- `sai_baba_arti.jpg` or `sai_baba_arti.png` — a high-resolution image of Sai Baba (min 1920×1080)
- `sai_baba_arti.mp3` — the Sai Baba Arti audio track

These files are placed in `backend/assets/live_tv/` before running the generation script.

### Video Spec
| Parameter | Value |
|---|---|
| Resolution | 1920×1080 (Full HD) |
| Duration | 60 minutes (audio looped to fill) |
| Format | MP4, H.264, AAC audio |
| ffmpeg preset | `-preset veryfast -crf 18 -threads 1` (matches existing YouTube pipeline) |
| Frame rate | 25fps (still image — minimal CPU) |
| Aspect ratio | 16:9 |

### ffmpeg Command (backend generates this)
```bash
ffmpeg -loop 1 -i sai_baba_arti.jpg \
  -stream_loop -1 -i sai_baba_arti.mp3 \
  -t 3600 \
  -c:v libx264 -preset veryfast -crf 18 -threads 1 \
  -c:a aac -b:a 192k \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" \
  -tune stillimage \
  -shortest \
  output_sai_baba_arti_60min.mp4
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

## 3. Live TV Side Panel (Home Page)

### Component: `frontend/src/components/LiveTVPanel.jsx`

A floating panel fixed to the **bottom-right corner** of every page (not just home — bottom-right is unobtrusive and always accessible).

### Visual Design
```
┌─────────────────────────────────┐
│ 🔴 LIVE  Sai Baba Arti    [─][✕]│
│ ┌───────────────────────────┐   │
│ │                           │   │
│ │   [YouTube embed player]  │   │
│ │                           │   │
│ └───────────────────────────┘   │
│ 🔇 Tap to unmute  ·  Full page → │
└─────────────────────────────────┘
```

- **Width**: 280px (collapsed) | 480px (expanded via toggle)
- **Position**: `fixed bottom-4 right-4 z-50`
- **Header bar**: Gold gradient, `🔴 LIVE` pulsing red dot, title, minimise `—` and close `✕` buttons
- **Player**: YouTube iframe embed, 16:9 ratio
- **Autoplay**: `autoplay=1&mute=1` (browser-compliant — starts muted)
- **Unmute prompt**: Visible button "🔇 Tap to unmute" — clicking sets `mute=0` via YouTube iframe API
- **Full page link**: "Full page →" navigates to `/live-sai-baba-arti`
- **Persistence**: Panel state (minimised/closed) saved to `localStorage`; closed state resets after 24 hours so it reappears daily

### Embed URL Format
```
https://www.youtube.com/embed/{youtube_video_id}?autoplay=1&mute=1&loop=1&playlist={youtube_video_id}&rel=0&modestbranding=1
```

`loop=1&playlist={id}` causes YouTube to loop the video indefinitely without showing related videos at the end.

### Panel States
| State | Behaviour |
|---|---|
| Open (default) | Full panel visible, video autoplaying muted |
| Minimised | Only header bar visible (40px tall), video pauses |
| Closed | Panel hidden, reappears after 24 hours |
| Expanded | Wider panel (480px), better viewing |

### Integration in `frontend/src/App.js`
```jsx
// Add globally so panel appears on all pages
import LiveTVPanel from './components/LiveTVPanel';

// Inside App return:
<LiveTVPanel />
```

The panel fetches the active video from `GET /api/live-tv/active` on mount. If no active video, panel does not render.

---

## 4. SEO Landing Page

### Route: `/live-sai-baba-arti`
### File: `frontend/src/pages/LiveSaiBabaArtiPage.jsx`

### Page Purpose
A standalone, SEO-optimised page that ranks for searches like:
- "Live Sai Baba Arti"
- "Sai Baba Arti online"
- "Om Sai Ram live"
- "Sai Baba daily arti"

### Page Layout
```
[Header: EverydayHoroscope nav]

H1: 🙏 Live Sai Baba Arti — Om Sai Ram
Subtitle: Experience the divine blessings of Sai Baba with our continuous live arti

[Large YouTube embed — 16:9, full-width on mobile, 70% width on desktop]
[🔴 LIVE badge] [🔊 Unmute] [📱 Share]

[Arti Lyrics section — full Sai Baba Arti text in Hindi + English transliteration]

[About Sai Baba section — 200 words, SEO content]

[More Divine Content section — links to Panchang, Daily Horoscope, other artis when added]

[Footer]
```

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
