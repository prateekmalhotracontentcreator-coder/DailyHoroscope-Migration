# Codex Commission: SOCIAL-1 -- Instagram + X (Twitter) Social Posting
> **Module:** Growth -- Social Media
> **Issued:** 2026-06-08 | **Priority:** Medium
> **Depends on:** Facebook posting (already live). Extends the same Social Media sub-tab.
> **Env vars needed by TT before issuing:**
>   - Instagram: `INSTAGRAM_BUSINESS_ACCOUNT_ID` (pending -- TT to confirm in Meta Business Manager)
>   - X/Twitter: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` (TT to create Twitter Developer App)

---

## 1. What This Builds

Extends the existing Social Media sub-tab in Admin Console Notifications to support posting to:
- **Instagram** (Business account, image + caption via Meta Graph API)
- **X / Twitter** (text + optional image via Twitter API v2)

Facebook ✅ and YouTube ✅ are already live. This commission adds the two remaining channels.

---

## 2. Files to Create / Modify

```
backend/server.py                             ← 4 new endpoints (Instagram post + status, X post + status)
frontend/src/pages/admin/AdminDashboard.jsx   ← Enable Instagram + X buttons in Social Media sub-tab
```

No new service files needed -- keep all logic in `server.py` like the existing Facebook implementation.

---

## 3. Instagram -- Meta Graph API

### 3a -- How Instagram Business posting works (2-step)

Step 1: Create a media container
```
POST https://graph.facebook.com/v19.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media
  ?image_url={url}
  &caption={caption}
  &access_token={FACEBOOK_PAGE_ACCESS_TOKEN}
```
Returns: `{ "id": "container_id" }`

Step 2: Publish the container
```
POST https://graph.facebook.com/v19.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish
  ?creation_id={container_id}
  &access_token={FACEBOOK_PAGE_ACCESS_TOKEN}
```
Returns: `{ "id": "post_id" }`

**Uses the existing `FACEBOOK_PAGE_ACCESS_TOKEN`** (System User token -- never expires). No new OAuth flow needed. The `INSTAGRAM_BUSINESS_ACCOUNT_ID` is the only new env var.

**Image requirement:** URL must be publicly accessible. The existing `POST /api/admin/social/post-image` endpoint already uploads an image to a public URL -- reuse it.

### 3b -- Text-only Instagram posts

Instagram Business API does not support text-only posts (requires image). If no image is provided and `instagram` is in channels: return an error: `"Instagram requires an image. Please upload one."` -- do not silently skip.

### 3c -- New endpoints

```python
GET  /api/admin/instagram/status
# Returns: { "configured": bool, "account_id": str|null }
# "configured" = True if INSTAGRAM_BUSINESS_ACCOUNT_ID env var is set

POST /api/admin/social/post
# Already exists. Extend the `channels` list handler to include "instagram":
# if "instagram" in channels: call _post_to_instagram(message, image_url)
```

**Do NOT create a separate Instagram post endpoint.** The existing `POST /api/admin/social/post` already handles multi-channel posting. Add Instagram as a new branch in that handler.

---

## 4. X (Twitter) -- API v2

### 4a -- Credentials

```python
TWITTER_API_KEY             = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET          = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN        = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")
```

These are app-level credentials for a single dedicated account (not user OAuth). TT creates the Twitter Developer App and pastes the 4 keys into Render.

### 4b -- Text post

```python
POST https://api.twitter.com/2/tweets
Headers: OAuth 1.0a (TWITTER_API_KEY + TWITTER_API_SECRET + TWITTER_ACCESS_TOKEN + TWITTER_ACCESS_TOKEN_SECRET)
Body: { "text": message }
```

Use `requests-oauthlib` library (add to requirements.txt if not present).

### 4c -- Image post (optional)

Step 1: Upload media via v1.1 (media v2 upload not yet GA):
```
POST https://upload.twitter.com/1.1/media/upload.json
  (multipart, binary image)
Returns: { "media_id_string": "..." }
```

Step 2: Post with media:
```
POST https://api.twitter.com/2/tweets
Body: { "text": message, "media": { "media_ids": ["media_id_string"] } }
```

**Character limit:** X truncates at 280 chars. If `message` > 280 chars: truncate to 277 chars + "..." before posting. Log the truncation in the response.

### 4e -- New endpoints

```python
GET  /api/admin/x/status
# Returns: { "configured": bool }
# "configured" = True if all 4 TWITTER_* env vars are set

POST /api/admin/social/post
# Extend existing handler -- add "x" as a channel option alongside "facebook", "instagram", "youtube"
```

---

## 5. Admin UI Changes -- Social Media Sub-Tab

The Social Media sub-tab already shows channel checkboxes. Currently:
```
[✓ Facebook]  [○ Instagram (pending)]  [○ X (coming soon)]  [○ YouTube]
```

**Changes:**

1. **Instagram checkbox:** Change from disabled to enabled when `GET /api/admin/instagram/status` returns `configured: true`. Show tooltip: "Requires image upload" when hovered.

2. **X checkbox:** Change from disabled to enabled when `GET /api/admin/x/status` returns `configured: true`. Show character counter below message field (live count, turns amber at 260 chars, red at 280+).

3. **Validation:** If Instagram is checked but no image is attached, show inline error before sending: "Instagram requires an image."

4. **Channel status indicators:** Below each checkbox, show a small status indicator:
   - Instagram: "Account ID: configured ✅" or "Not configured ⚠️"
   - X: "API keys: configured ✅" or "Not configured ⚠️"

5. **Post results:** The existing `socialResults` state already shows per-channel success/failure. No change needed -- just ensure the backend returns `instagram` and `x` keys in the results object.

---

## 6. `POST /api/admin/social/post` -- updated response shape

```python
{
  "success": True,
  "results": {
    "facebook":  { "success": bool, "post_id": str|None, "error": str|None },
    "instagram": { "success": bool, "post_id": str|None, "error": str|None },
    "x":         { "success": bool, "tweet_id": str|None, "error": str|None, "truncated": bool },
    "youtube":   { "success": bool, "video_id": str|None, "error": str|None }
  }
}
```

Each channel's result is independent -- failure on one does not prevent posting to others.

---

## 7. Logging

All posts (success and failure) must be logged to `db.social_logs` -- the same collection the existing Facebook/YouTube posts write to. Add `"channel": "instagram"` or `"channel": "x"` in the log document.

---

## 8. Acceptance Gates (8)

| Gate | Test |
|---|---|
| G-01 | `GET /api/admin/instagram/status` returns `{ configured: true }` when `INSTAGRAM_BUSINESS_ACCOUNT_ID` env var is set |
| G-02 | Instagram post (text + image) succeeds: returns `post_id` and creates a `social_logs` entry |
| G-03 | Instagram post without image returns 400 error: "Instagram requires an image" |
| G-04 | `GET /api/admin/x/status` returns `{ configured: true }` when all 4 Twitter vars are set |
| G-05 | X post (text only) succeeds: returns `tweet_id` and creates `social_logs` entry |
| G-06 | X post with message > 280 chars: truncated to 277 + "..." in tweet, `truncated: true` in response |
| G-07 | Multi-channel post (Facebook + Instagram + X): all three post, results object has all 3 keys |
| G-08 | Instagram checkbox enabled only when `configured: true`; X checkbox enabled only when `configured: true` |

---

## 9. Constraints

- Build with full env var guard states -- both channels must display "not configured ⚠️" cleanly when their env vars are absent. The app must never crash due to missing credentials.
- Acceptance gates G-01 and G-04 (status endpoints) can be verified locally with placeholder env vars. All other gates (actual posting) are validated by TT on the live Render deployment after credentials are added.
- Do NOT create new OAuth flows for either platform -- both use static credentials set in Render.
- Do NOT modify the Facebook or YouTube posting code.
- Commit: `feat(social): SOCIAL-1 Instagram + X posting`
