# Codex Commission: GRW-1 -- Transit-Based User Segmentation & Campaign Engine
> **Module:** Growth -- Marketing Automation
> **Issued:** 2026-06-08
> **Priority:** High -- first commissioned Growth module
> **Type:** New feature -- backend service + admin UI + privacy consent

---

## 1. What This Commission Builds

A **transit-based user segmentation engine** that:

1. Reads user birth profiles from MongoDB
2. Computes each user's current astrological transit condition using the live pyswisseph engine
3. Groups users into named **Transit Segments** (e.g. Sade Sati, Ashtama Shani, Rahu over Moon)
4. Exposes segment counts to the Admin Console
5. Lets the admin trigger a targeted Email + WhatsApp campaign to any segment in one click
6. Respects an opt-in consent flag stored on each user's birth profile

**This is an internal marketing tool. No data is sold or shared externally. All computations are server-side. Users who have not opted in are excluded from all campaign sends.**

---

## 2. Architecture -- Files to Create / Modify

### New files
```
backend/transit_segmentation_service.py     ← All transit segment logic
```

### Modified files
```
backend/server.py                           ← 2 new admin endpoints + consent field on birth profile save
frontend/src/pages/admin/AdminDashboard.jsx ← New "Transit Campaigns" sub-tab inside Notifications
```

### Do NOT modify
```
backend/vedic_calculator.py    ← Read-only. Call its functions. Never edit.
backend/panchang_router.py     ← Bump ENGINE_VERSION on any backend change.
```

---

## 3. Transit Segmentation Service -- `backend/transit_segmentation_service.py`

### 3a -- The Six Transit Segments

Classify every user with a birth profile against these six named segments. A user can be in **multiple segments simultaneously**.

| Segment ID | Name | Trigger Condition | Significance |
|---|---|---|---|
| `sade_sati` | Sade Sati | Saturn transiting 12th, 1st, or 2nd house from natal Moon sign | 7.5-year major life pressure |
| `kantaka_shani` | Kantaka Shani | Saturn transiting 4th house from natal Moon sign | 2.5-year domestic/career tension |
| `ashtama_shani` | Ashtama Shani | Saturn transiting 8th house from natal Moon sign | 2.5-year transformative challenge |
| `rahu_moon` | Rahu-Ketu Transit Over Moon | Rahu or Ketu within same sign as natal Moon | 1.5-year karmic shift |
| `saturn_mahadasha` | Saturn / Rahu / Ketu Mahadasha | Current Vimshottari Mahadasha lord is Saturn, Rahu, or Ketu | Intense dasha period |
| `jupiter_transit_new` | Jupiter Ingress Month | Jupiter changed signs within the last 30 days | Annual auspicious renewal window |

### 3b -- `get_today_transit_planets() -> dict`

```python
"""
Returns today's sidereal longitudes for segmentation-relevant planets.
Uses the same pyswisseph setup as vedic_calculator.py.
NEVER replicate the swe setup -- import from vedic_calculator:
  from vedic_calculator import _calc_planet, SWE_FLAGS, get_nakshatra
"""
# Returns:
{
  "saturn_sign": 0-11,      # sidereal sign index (0=Aries ... 11=Pisces)
  "saturn_longitude": float,
  "rahu_sign": 0-11,
  "ketu_sign": 0-11,
  "jupiter_sign": 0-11,
  "jupiter_longitude": float,
  "computation_date": "YYYY-MM-DD"
}
```

**Important:** Cache this result for 24 hours using a module-level dict with a date key. Do not call pyswisseph per-user -- call it once per day and reuse.

### 3c -- `classify_user_segments(birth_profile: dict, today_transits: dict) -> list[str]`

```python
"""
Returns list of segment IDs that apply to this user today.
birth_profile is a document from db.birth_profiles.
Calls calculate_vimshottari_dasha + get_current_dasha from vedic_calculator.
"""
```

**Logic for each segment:**

**sade_sati:**
```python
natal_moon_sign = int(birth_profile["moon_longitude"] / 30) % 12
sade_sati_signs = [
    (natal_moon_sign - 1) % 12,   # 12th from Moon
    natal_moon_sign,               # 1st (Moon's sign)
    (natal_moon_sign + 1) % 12    # 2nd from Moon
]
return today_transits["saturn_sign"] in sade_sati_signs
```

**kantaka_shani:**
```python
fourth_from_moon = (natal_moon_sign + 3) % 12
return today_transits["saturn_sign"] == fourth_from_moon
```

**ashtama_shani:**
```python
eighth_from_moon = (natal_moon_sign + 7) % 12
return today_transits["saturn_sign"] == eighth_from_moon
```

**rahu_moon:**
```python
return (today_transits["rahu_sign"] == natal_moon_sign or
        today_transits["ketu_sign"] == natal_moon_sign)
```

**saturn_mahadasha:**
```python
dashas = calculate_vimshottari_dasha(birth_profile["date_of_birth"], birth_profile["moon_longitude"])
current = get_current_dasha(dashas)
return current.get("maha_lord") in ["Saturn", "Rahu", "Ketu"]
```

**jupiter_transit_new:**
```python
# Jupiter changed signs within last 30 days
# Store previous jupiter_sign in the cache dict alongside today's value
# Return True if jupiter_sign changed since 30 days ago
```

### 3d -- `get_segment_summary(db) -> dict` (async)

```python
"""
Iterates all birth profiles that have transit_alerts_consent=True.
Computes segments for each. Returns counts per segment.
Caps at 5000 profiles per run to avoid timeout.
"""
# Returns:
{
  "computed_at": "ISO timestamp",
  "total_profiles_scanned": int,
  "segments": {
    "sade_sati":           {"count": int, "label": "Sade Sati",            "description": "Saturn transiting 12th/1st/2nd from natal Moon"},
    "kantaka_shani":       {"count": int, "label": "Kantaka Shani",         "description": "Saturn in 4th from natal Moon"},
    "ashtama_shani":       {"count": int, "label": "Ashtama Shani",         "description": "Saturn in 8th from natal Moon"},
    "rahu_moon":           {"count": int, "label": "Rahu-Ketu Over Moon",   "description": "Rahu or Ketu transiting natal Moon sign"},
    "saturn_mahadasha":    {"count": int, "label": "Saturn/Rahu/Ketu Dasha","description": "Currently in Saturn, Rahu, or Ketu Mahadasha"},
    "jupiter_transit_new": {"count": int, "label": "Jupiter Ingress Window","description": "Jupiter changed signs in the last 30 days"},
  }
}
```

### 3e -- `get_segment_user_emails(db, segment_id: str, limit: int = 500) -> list[dict]`

```python
"""
Returns up to `limit` users in the given segment who have transit_alerts_consent=True.
Each entry: { "email": str, "name": str, "moon_sign": str, "segment": str }
Used by the campaign trigger endpoint.
"""
```

**Note on `moon_longitude` availability:** Not all birth profiles have a pre-stored `moon_longitude`. When it is absent:
- Look for a saved `birth_chart_reports` document for this profile -- extract `moon_sign` dict from it
- If no saved report exists: **skip this user** (do not call the chart engine at scale)
- Log the skip count in the summary response

---

## 4. Backend Endpoints -- `server.py`

### 4a -- `GET /api/admin/transit-segments/summary`

```python
@api_router.get("/admin/transit-segments/summary")
async def get_transit_segment_summary(db=Depends(get_database), admin=Depends(require_admin)):
    """Returns segment counts across all consenting birth profiles."""
```

- Calls `transit_segmentation_service.get_segment_summary(db)`
- Cache result for 4 hours (store in a module-level dict with timestamp, same pattern as other cached admin endpoints)
- Returns the dict from `get_segment_summary()`

### 4b -- `POST /api/admin/transit-campaigns/trigger`

```python
class TransitCampaignRequest(BaseModel):
    segment_id: str           # one of the 6 segment IDs
    subject: str              # email subject
    body: str                 # email body (plain text or HTML)
    channels: list[str]       # ["email"] or ["email", "whatsapp"]
    limit: int = 200          # max users to contact in one send

@api_router.post("/admin/transit-campaigns/trigger")
async def trigger_transit_campaign(request: TransitCampaignRequest, db=Depends(get_database), admin=Depends(require_admin)):
```

- Calls `get_segment_user_emails(db, segment_id, limit=request.limit)`
- For each user: calls the existing `notification_email_service.py` send function (already live)
- For WhatsApp: calls `notification_whatsapp_service.py` (already live, OTP pending)
- Logs send results to `db.notification_logs` (same collection as existing notification sends)
- Returns: `{ "sent": int, "failed": int, "skipped_no_consent": int, "segment": str }`

### 4c -- Consent field on birth profile creation

In the existing `POST /api/birth-profiles` handler (around line 970 in server.py):

```python
# Add to BirthProfileCreate model:
transit_alerts_consent: bool = False

# Store it on the document:
birth_profile["transit_alerts_consent"] = profile.transit_alerts_consent
```

Also add a backfill note: existing profiles without the field are treated as `False` (no consent). Admin can send a bulk opt-in invite to existing users via the standard Notifications → Compose flow -- this is out of scope for this commission.

---

## 5. Admin UI -- `AdminDashboard.jsx`

Add a new sub-tab `transit` inside the existing Notifications tab (alongside `subscribers`, `compose`, `scheduled`, `history`, `social`).

### Tab label: "Transit Campaigns"

### Content -- two sections:

**Section 1: Segment Overview Cards (read-only)**

On tab mount, call `GET /api/admin/transit-segments/summary`. Show one `GlassCard` per segment:

```
┌─────────────────────────────────────────┐
│  🪐 Sade Sati                           │
│  342 users currently in this phase      │
│  Saturn transiting 12th/1st/2nd from    │
│  natal Moon                             │
│                          [Send Campaign]│
└─────────────────────────────────────────┘
```

Cards: 2-column grid on desktop, 1-column on mobile. Show loading skeleton while fetching. Show "Computed at [time] · Refreshes every 4h" caption.

**Section 2: Campaign Composer (shown when [Send Campaign] is clicked)**

Opens an inline panel (not a separate modal) below the cards:

```
Sending to: Sade Sati (342 users)
Max recipients: [200 ▾]   Channels: [✓ Email] [○ WhatsApp]
Subject: _________________________________
Body:    _________________________________
         _________________________________

         [Cancel]  [Send Campaign →]
```

On send: POST to `/api/admin/transit-campaigns/trigger`. Show result toast:
- Success: "✅ Campaign sent -- 198 emails queued, 4 failed"
- Error: shows error from API

**Style:** Follow existing Notifications tab patterns -- GlassCard, gold accents, same button classes as compose tab.

---

## 6. Privacy / Consent -- Frontend Change

In the birth profile creation form (`frontend/src/pages/kundali/BirthChartPage.jsx` or wherever the birth details form renders):

Add one checkbox **below** the birth details fields, **above** the submit button:

```jsx
<label className="flex items-start gap-2 text-sm text-muted-foreground cursor-pointer">
  <input
    type="checkbox"
    checked={transitConsent}
    onChange={e => setTransitConsent(e.target.checked)}
    className="mt-0.5 accent-gold"
  />
  <span>
    Send me personalised cosmic alerts when my astrological transits shift
    (e.g. Sade Sati, Jupiter ingress). I can unsubscribe anytime.
  </span>
</label>
```

Default: unchecked. Wire `transitConsent` to `transit_alerts_consent` in the API payload.

**Do NOT make this a required field.** It is optional opt-in only.

---

## 7. Acceptance Gates (8 required)

| Gate | Test |
|---|---|
| G-01 | `GET /api/admin/transit-segments/summary` returns all 6 segment keys with `count` integer ≥ 0 |
| G-02 | `sade_sati` count > 0 when test profile with natal Moon in Pisces is in DB (Saturn currently in Aquarius = 12th from Pisces) |
| G-03 | `POST /api/admin/transit-campaigns/trigger` with `segment_id="sade_sati"`, `channels=["email"]`, `limit=1` returns `{ "sent": 1 }` for a test user with `transit_alerts_consent=True` |
| G-04 | Same POST with a test user where `transit_alerts_consent=False` returns `{ "sent": 0, "skipped_no_consent": 1 }` |
| G-05 | Admin UI Transit Campaigns tab loads without error and shows 6 segment cards |
| G-06 | Campaign composer renders when [Send Campaign] is clicked on any card |
| G-07 | Birth profile creation form shows the opt-in checkbox; submitting with checkbox ticked saves `transit_alerts_consent: true` in MongoDB |
| G-08 | `moon_longitude` absent on a profile → user is skipped (not errored), skip count appears in summary response |

---

## 8. Constraints

- **NEVER call `vedic_calculator.py` functions at the rate of one call per user per request.** Compute today's transits once, cache, apply to all profiles.
- **NEVER modify `vedic_calculator.py`.** Import from it; do not fork or replicate it.
- **NEVER send to users with `transit_alerts_consent != True`.** This is a hard gate -- not a soft default.
- **All sends go through existing notification services** (`notification_email_service.py`, `notification_whatsapp_service.py`). Do not write a parallel send path.
- **All logs go to `db.notification_logs`** -- same collection as existing sends. No new collection needed.
- **Bump `ENGINE_VERSION`** in `panchang_router.py` before any backend change.
- Commit format: `feat(growth): GRW-1 transit segmentation engine`

---

## 9. Out of Scope (Phase 2)

These are intentionally excluded from this commission:

- Automated/scheduled campaign sends (cron-based) -- manual admin trigger only for Phase 1
- Personalised message body per user (e.g. inserting user's name or sign) -- plain broadcast for Phase 1
- Privacy policy text update -- TT to update `db.policies` manually after this ships
- Bulk opt-in invite to existing users -- separate campaign via standard Notifications → Compose

---

## 10. Key Files Reference

```python
# Import these -- do NOT replicate:
from vedic_calculator import (
    calculate_vimshottari_dasha,
    get_current_dasha,
    _calc_planet,
    SWE_FLAGS,
    get_nakshatra
)

# Existing notification services -- call these:
from notification_email_service import send_email          # check exact function name
from notification_whatsapp_service import send_whatsapp    # check exact function name

# MongoDB collections in scope:
db.birth_profiles          # source of natal data + consent flag
db.notification_logs       # write send results here

# Do not touch:
db.users                   # auth only
db.horoscope_db            # wrong DB alias -- always use horoscope_db via get_database()
```
