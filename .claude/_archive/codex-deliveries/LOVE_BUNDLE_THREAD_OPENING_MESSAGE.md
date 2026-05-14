# Love & Engagement Module — Full Thread Opening Message
# Ready to send to Codex Love Bundle thread

> **Prepared by:** Temple Team — 2 April 2026
> **Copy-paste this entire message into the new Codex Love Bundle thread**

---

---

**Subject: New Contract — Love & Engagement Module + Ritual Trigger Engine (Subscription Product)**

Temple Team here. This message opens the Love & Engagement Module thread. Read the full brief before starting — there are two distinct workstreams inside this module: (1) a suite of 6 on-demand reports, and (2) a flagship subscription product called the Ritual Trigger Engine. Both are contracted here.

---

## Part 1 — Governing Decisions

The following decisions from the Individual Reports contract apply in full to this thread:

- **D1:** Vedic-first only. `pyswisseph 2.10.x`, Lahiri ayanamsa, sidereal. No external astrology API.
- **D7:** Remedies approved — mantras, gemstones, rituals, vastu. Supportive framing only. No guaranteed outcomes.
- **D9:** All report artifacts write to `individual_reports` collection with `report_type` field. *(Exception: Ritual Engine has its own collections — see Part 3.)*
- **D10:** Route prefix `/api/reports/` for report routers. Route prefix `/api/ritual-engine/` for the Ritual Engine router.
- **D11:** Codex delivers compute and trigger detection endpoints. Temple wires all scheduling, subscription lifecycle, payment handling, and notification dispatch.

**Decision updates specific to this thread:**
- **D5 update:** Transit-based reports approved from the start. Use `swe.calc_ut()` with current date.
- **D6 update:** Deep Synastry (two-person data) approved as Phase 2 within this thread. Temple handles consent and storage. Codex delivers compute endpoint only.
- **D8 update:** "Intimacy & Vitality Forecast" confirmed for Phase 1 of this thread under that exact name.

---

## Part 2 — Step 1 Required: Brief Idea + Engineering Structure

Before building anything, deliver **`LOVE_ENGAGEMENT_BRIEF_IDEA_CODEX.md`** covering:

1. **Report-by-report engineering overview** — For each of the 6 reports: what it computes, which pyswisseph calls are required, what the output structure looks like
2. **Ritual Trigger Engine architecture** — How the 5 trigger scenarios are detected, the subscription check endpoint design, the dashboard endpoint design, the `notification_worthy` flag logic
3. **Data requirements** — Natal only vs. transit vs. two-person data per report/feature
4. **Shared compute layer** — Reusable functions across reports and the engine (Venus position, house lord calculation, aspect detection). Align with `vedic_shared_utils.py` being designed in the Individual Reports thread.
5. **Proposed additions** — Any reports or trigger scenarios you recommend beyond what is specified
6. **Risk flags** — Any astrological concepts needing Temple clarification before implementation

Temple will review, give feedback, and confirm final scope before you build.

---

## Part 3 — The Ritual Trigger Engine (Subscription Product)

This is the **flagship product of the Love module** and the primary driver of subscription revenue from this workstream. It is positioned differently from the 6 reports below — it is not a report the user generates on demand. It is an always-on personal cosmic coach that monitors the user's chart against live transits and fires a notification the moment a meaningful alignment occurs.

### Product Positioning

**Marketing description:** *"Your personal cosmic love coach. The Ritual Trigger Engine monitors your birth chart 24/7 and alerts you the moment the stars align for attraction, passion, healing, or a lasting connection — with a personalised ritual for each moment."*

**Subscription model:** Users subscribe to the Ritual Trigger Engine as a premium tier. Temple handles all payment processing (Razorpay), subscription status, and lifecycle UI. Codex delivers the compute and trigger detection endpoints only. The engine runs daily for all subscribed users — Temple's APScheduler calls the check endpoint.

**Marketing homepage:** The Ritual Engine is a featured product on the EverydayHoroscope marketing homepage. Temple builds the homepage. Codex should design the dashboard endpoint so the homepage can display a live preview (anonymised trigger example or the user's current Love Battery if authenticated).

---

### Architecture — How It Differs from Reports

| Reports (Part 4) | Ritual Trigger Engine |
|---|---|
| User-initiated (POST /generate) | System-initiated (APScheduler calls daily) |
| One-time or occasional | Always-on for subscribed users |
| On-demand output | Proactive push notification when alignment fires |
| `individual_reports` collection | Own collections: `ritual_engine_subscriptions`, `ritual_engine_trigger_log` |
| Route prefix: `/api/reports/` | Route prefix: `/api/ritual-engine/` |

---

### MongoDB Collections

**`ritual_engine_subscriptions`** — one document per subscribed user
```json
{
  "user_email": "string",
  "subscribed": true,
  "subscribed_since": "iso-8601-utc",
  "natal_data": {
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone": "Asia/Kolkata",
    "city_name": "New Delhi"
  },
  "triggers_opted_in": ["first_date_magnet", "steamy_encounter", "ex_recovery", "long_term_love", "lunar_daily_score"],
  "last_checked": "iso-8601-utc"
}
```

**`ritual_engine_trigger_log`** — one document per fired trigger per user
```json
{
  "id": "uuid",
  "user_email": "string",
  "trigger_type": "first_date_magnet | steamy_encounter | ex_recovery | long_term_love | lunar_daily_score",
  "check_date": "YYYY-MM-DD",
  "intensity": "exact | close | wide",
  "orb_degrees": 1.2,
  "alignment_description": "string",
  "ritual_suggestion": "string",
  "notification_worthy": true,
  "active_from": "YYYY-MM-DD",
  "active_until": "YYYY-MM-DD",
  "fired_at": "iso-8601-utc"
}
```

---

### API Endpoints

**`POST /api/ritual-engine/enroll`**
Called by Temple when a user's subscription is activated (Razorpay webhook → Temple → this endpoint).
Accepts natal data + user email. Writes to `ritual_engine_subscriptions`. Does not run a check — enrollment only.

**`POST /api/ritual-engine/check`**
Called by Temple's APScheduler daily (once per opted-in user). Accepts `{ user_email, check_date (optional, defaults to today) }`.
- Reads the user's natal data from `ritual_engine_subscriptions`
- Runs all 5 trigger scenarios (see below) against today's transits
- Writes results to `ritual_engine_trigger_log`
- Returns the list of active triggers with `notification_worthy` flags
- Temple reads the response: fires Notification Engine for all `notification_worthy: true` triggers

**`GET /api/ritual-engine/dashboard`**
Authenticated user endpoint. Returns:
- Today's Love Battery percentage (Trigger V — Lunar Daily Score)
- Active triggers today (if any) with alignment description and ritual
- Next upcoming trigger (nearest future window) — type, date, days away
- Last 7 days of trigger history

**`GET /api/ritual-engine/history`**
Authenticated user endpoint. Returns last 30 days of `ritual_engine_trigger_log` entries for the user.

**`DELETE /api/ritual-engine/unenroll`**
Called by Temple when subscription lapses. Sets `subscribed: false` in `ritual_engine_subscriptions`.

---

### The 5 Trigger Scenarios

These are the exact triggers the engine detects. Implement all five.

---

#### Trigger I — The "First Date" Magnet (Venus Conjunctions)

**Astrological logic:**
Trigger when Transiting Venus is within 3° of the user's Natal Sun, Natal Ascendant, or Natal 7th House Lord.

**What it means:** This is when the user is most physically attractive, socially charming, and magnetically irresistible to others. The Venus glow is on.

**`trigger_type`:** `"first_date_magnet"`

**Intensity logic:**
- `exact`: orb ≤ 1° → `notification_worthy: true`
- `close`: orb 1°–3° → `notification_worthy: true`
- `wide`: orb 3°–5° → `notification_worthy: false` (compute but do not fire notification)

**Push notification text:**
*"The stars are aligning for a 'Meet-Cute.' Your charm is at a 10/10 today."*

**`ritual_suggestion` output:**
*"Venus Sound Therapy — Chant 'Om Shum Shukraya Namaha' 108 times today. Wear pink or white to amplify your natural magnetism. Step out — you are at your most irresistible."*

**`alignment_description` example:**
*"Transiting Venus is 1.3° from your natal Ascendant — your magnetic field is at its peak."*

---

#### Trigger II — The "Steamy Encounter" Alert (Mars–Venus Transits)

**Astrological logic:**
Trigger when:
- Transiting Mars forms a Trine (120° ± 3°) to the user's Natal Venus, **or**
- Transiting Mars forms a Conjunction (0° ± 3°) to the user's Natal Venus, **or**
- Transiting Mars enters the user's Natal 8th House

**What it means:** High physical energy, heightened passion, and bold romantic initiative. This is the window for the user to make the first move.

**`trigger_type`:** `"steamy_encounter"`

**Intensity logic:**
- Mars conjunct natal Venus, orb ≤ 2°: `exact`
- Mars trine natal Venus, orb ≤ 2°: `exact`
- Mars entering 8th house (within 3 days): `close`
- All of the above at wider orbs: `wide`
- `notification_worthy: true` for `exact` and `close`

**Push notification text:**
*"Heat Warning: Your passion levels are peaking. Don't be afraid to make the first move tonight."*

**`ritual_suggestion` output:**
*"Red Candle Manifestation — Light a red candle and visualise your desire with full clarity. Carry a Garnet or Ruby for confidence and boldness. Act on your instinct — the universe is amplifying your signal."*

**`alignment_description` example:**
*"Transiting Mars is forming a trine to your natal Venus — passion and boldness are surging."*

---

#### Trigger III — The "Ex-Recovery" & Healing Phase (Retrograde Transits)

**Astrological logic:**
Trigger when:
- Venus goes Retrograde AND is transiting through the user's Natal 5th House or Natal 7th House, **or**
- Mercury goes Retrograde AND is transiting through the user's Natal 5th House or Natal 7th House

**Detection method:** Use `swe.calc_ut()` to check retrograde status (negative daily motion) and current house position of the transiting planet relative to the user's natal house cusps.

**What it means:** Past lovers may resurface. Communication in relationships hits snags. This is a powerful emotional clearing window — not a time to start, but to heal and release.

**`trigger_type`:** `"ex_recovery"`

**Intensity logic:**
- Retrograde planet within 5th or 7th house: `close` → `notification_worthy: true`
- Retrograde planet within 3° of 5th or 7th house cusp (about to enter): `wide` → `notification_worthy: false` (pre-alert)

**Push notification text:**
*"Ghost from the past? Venus is retrograde in your house of romance. Time for a 'Heart Detox.'"*

**`ritual_suggestion` output:**
*"Full Moon Release — On the next full moon, write the name of an ex or a toxic pattern on paper. Burn it safely to reset and clear your 7th house energy. This window is for releasing, not beginning."*

**`alignment_description` example:**
*"Venus is retrograde in your 7th house of partnerships — old connections resurface, emotions run deep."*

**Note:** This trigger may be active for several weeks (duration of retrograde in that house). Set `active_from` to the date the retrograde planet entered the house and `active_until` to the date it exits or stations direct.

---

#### Trigger IV — The "Long-Term Love" Window (Jupiter Transits)

**Astrological logic:**
Trigger when:
- Transiting Jupiter enters the user's Natal 7th House (happens approximately once every 12 years), **or**
- Transiting Jupiter forms a Trine (120° ± 5°) to the user's Natal Ascendant

**What it means:** The most auspicious and rare window for serious relationships, marriage prospects, and soulmate-level connections. Jupiter expands whatever it touches.

**`trigger_type`:** `"long_term_love"`

**Intensity logic:**
- Jupiter entering 7th house (within 7 days of ingress): `exact` → `notification_worthy: true`
- Jupiter already in 7th house (ongoing): `close` → `notification_worthy: true` (fire once on entry, then weekly digest only)
- Jupiter trine Ascendant, orb ≤ 3°: `exact` → `notification_worthy: true`
- Jupiter trine Ascendant, orb 3°–5°: `close` → `notification_worthy: true`

**Push notification text:**
*"A Golden Year for Love: Jupiter is expanding your partnership sector. This is the time for 'The One.'"*

**`ritual_suggestion` output:**
*"Vastu Reset — Clean the Southwest corner of your bedroom thoroughly. Place a pair of Rose Quartz stones there to anchor the energy of partnership and draw in a lasting bond. This window is rare — act with intention."*

**`alignment_description` example:**
*"Transiting Jupiter has entered your 7th house — a 12-year window for serious love is now open."*

**Note on re-notification:** Jupiter in the 7th house can last 12–13 months. Set `notification_worthy: true` on entry and at each exact degree crossing of significant natal planets in the 7th. Do not fire the notification daily for the entire transit — only at the ingress and at meaningful degree contacts within the house.

---

#### Trigger V — The Lunar Daily Score ("Love Battery")

**Astrological logic:**
Calculate the angular distance (shortest arc) between Transiting Moon's longitude and the user's Natal Venus longitude, updated daily.

**Scoring:**
| Angular Distance | Score Category | Love Battery % |
|---|---|---|
| 0° (Conjunction) | Peak | 95–100% |
| 60° (Sextile) | High | 75–85% |
| 120° (Trine) | High | 80–90% |
| 90° (Square) | Caution | 35–50% |
| 180° (Opposition) | Low | 15–30% |
| All other angles | Neutral | 50–65% |

**Score interpolation:** Use the orb from the exact angle to smooth the percentage. Exact conjunction = 100%. 10° from conjunction = ~80%. Implement a smooth curve, not hard step changes.

**`trigger_type`:** `"lunar_daily_score"`

**This trigger is different from I–IV:**
- It fires **every day** for every subscribed user — it is the always-on dashboard feature
- `notification_worthy`: Only `true` when score ≥ 80% (peak and high categories) — do not send a push notification for neutral or low days. Users see the score on their dashboard regardless.
- The Love Battery % is the **primary dashboard display** — shown as a visual meter on the Ritual Engine dashboard and on the app homepage for subscribed users

**`alignment_description` examples:**
- Score 92%: *"The Moon is conjunct your natal Venus — your emotional radar is finely tuned. A perfect day for connection."*
- Score 28%: *"The Moon opposes your natal Venus — emotional turbulence is possible. Ideal for rest and reflection, not pursuit."*
- Score 63%: *"Neutral lunar energy today — steady and grounded. Good for nurturing existing connections."*

**Dashboard card output:**
```json
{
  "trigger_type": "lunar_daily_score",
  "check_date": "YYYY-MM-DD",
  "love_battery_percent": 87,
  "score_category": "high",
  "moon_natal_venus_angle": 61.3,
  "alignment_description": "string",
  "action_note": "string (max 20 words — one-line suggested action)",
  "notification_worthy": true
}
```

---

### Ritual Engine — Summary Output from `check` Endpoint

The `POST /api/ritual-engine/check` response should aggregate all 5 triggers and return:

```json
{
  "user_email": "string",
  "check_date": "YYYY-MM-DD",
  "love_battery": { /* Trigger V output */ },
  "active_triggers": [ /* Array of Trigger I–IV objects that are active today */ ],
  "notification_worthy_triggers": ["first_date_magnet", "steamy_encounter"],
  "coach_summary": "string (max 60 words — synthesises all active triggers into one personalised coaching message for the day)",
  "next_upcoming_trigger": {
    "trigger_type": "long_term_love",
    "starts_in_days": 14,
    "preview": "Jupiter enters your 7th house in 14 days — prepare for a major love season."
  }
}
```

The `coach_summary` is the daily personalised message. This is what makes the product feel like a cosmic coach rather than a data feed.

---

## Part 4 — The 6 On-Demand Reports

These are user-initiated reports. Standard `POST /generate` + `GET /history` pattern. All write to `individual_reports` collection.

---

### Report 1 — Encounter Window *(Transit-based, Single User)*
**Commercial hook:** "When is your next best window to meet someone?"
- Trigger: Transiting Venus within 3° of natal Sun, natal Ascendant, or 7th House Lord
- Secondary: Transiting Jupiter entering natal 5th or 7th house
- Output: Date windows (next 90 days) when conditions are active
- Sections: Current window status, next 3 peak windows with dates, personalised context, remedies
- **File:** `encounter_window_router.py` | **Route:** `/api/reports/encounter-window`

---

### Report 2 — Love Weather Forecast *(Transit-based, Single User — Seasonal)*
**Commercial hook:** "Your 90-day romantic forecast — when to move, when to wait."
- Aggregate transiting Venus, Jupiter, Mars, Saturn activity over natal 5th and 7th houses
- Score each month: expansion (benefic), caution (malefic), neutral
- Sections: 90-day arc summary, month-by-month quality rating, key dates, action guidance, remedies
- **File:** `love_weather_router.py` | **Route:** `/api/reports/love-weather`

---

### Report 3 — Date-Night Score *(Transit-based, Daily Micro-Forecast)*
**Commercial hook:** "Should I ask them out tonight? Check your cosmic score."
- Angular distance between Transiting Moon and natal Venus (same logic as Ritual Engine Trigger V — the report version)
- 0°, 60°, 120°: High score | 90°, 180°: Caution
- Also check: Transiting Venus aspect to natal Mars (passion amplifier)
- Output: Daily Love Battery % + 1-line note + suggested action
- **Note:** The Ritual Engine's Lunar Daily Score (Trigger V) is the subscription version of this same logic. The Date-Night Score report is the on-demand, pay-per-use version. Both should share the same underlying compute function.
- **File:** `date_night_router.py` | **Route:** `/api/reports/date-night`

---

### Report 4 — Digital Dating Strategy Report *(Natal-based, Single User)*
**Commercial hook:** "Your cosmic dating profile — what you attract and what attracts you."
- 5th house sign + lord: romantic style and what you attract
- Venus sign + house: desire nature and expression of affection
- Mars sign + house: pursuit style and physical attraction
- 7th house sign + lord: long-term partner archetype
- Sections: Attraction signature, dating style, ideal partner profile, what to lead with on a first date, red flags in yourself, remedies
- **File:** `digital_dating_router.py` | **Route:** `/api/reports/digital-dating`

---

### Report 5 — Intimacy & Vitality Forecast *(Transit-based, Single User)*
**Commercial hook:** "Your peak energy windows — emotional, romantic, and vital."
- 8th house lord natal position: intimacy style and depth
- Transiting Mars trine (120°) or conjunct (0°) natal Venus
- Transiting Mars entering natal 8th house
- Output: Current energy assessment + next peak window dates (next 60 days)
- Sections: Natal intimacy signature, current vitality phase, peak window dates, energy navigation tips, remedies
- **Tone:** Energy, passion, confidence, romantic connection. Not explicit.
- **Note:** Partially overlaps with Ritual Engine Trigger II. The report is a full narrative output. Trigger II is a push notification with a ritual. Share the underlying Mars–Venus aspect detection logic.
- **File:** `intimacy_vitality_router.py` | **Route:** `/api/reports/intimacy-vitality`

---

### Report 6 — Deep Synastry: Soul Connection *(Phase 2 — Two Persons)*
**Commercial hook:** "How deep is your connection? The cosmic compatibility deep-dive."
- Compute natal charts for both persons
- Key synastry overlays: Person A's planets in Person B's houses (and vice versa)
- Venus–Mars inter-aspects, Moon–Moon and Moon–Sun compatibility
- Saturn overlays: long-term stability vs. friction
- Sections: Connection archetype, attraction dynamic, emotional resonance score, long-term compatibility, growth areas, remedies for both
- Data input: Two birth datasets (date, time, location)
- Temple handles consent and storage. Codex delivers compute endpoint only.
- **File:** `soul_connection_router.py` | **Route:** `/api/reports/soul-connection`

---

## Part 5 — Proposed Additions

Please include in the Brief Idea document any additions you recommend. Temple is open to:
- Venus Retrograde personal impact report
- "Soulmate Timing" — strongest relationship window in Dasha sequence
- Rahu/Ketu axis love karma (nodes in 5th/7th)
- Additional Ritual Engine trigger scenarios beyond the 5 specified
- Any commercially strong concept you identify

---

## Part 6 — Technical Constraints

Same as all Temple contracts — no exceptions:

| Constraint | Requirement |
|---|---|
| Computation | `pyswisseph 2.10.x`, Lahiri ayanamsa, sidereal |
| No external APIs | No third-party astrology or transit API |
| Backend language | Python 3.12 |
| Python boilerplate | `from __future__ import annotations` at top |
| Datetime | `timezone.utc` — never `datetime.UTC` |
| Pydantic | v2 with `ConfigDict` |
| Database (reports) | `request.app.state.db`, collection: `individual_reports` |
| Database (engine) | `request.app.state.db`, collections: `ritual_engine_subscriptions`, `ritual_engine_trigger_log` |
| Auth | `request.state.user.get("email")` |
| No Temple imports | No imports from any live Temple source file |
| Routes — reports | `POST .../generate` + `GET .../history` |
| Routes — engine | `POST /enroll`, `POST /check`, `GET /dashboard`, `GET /history`, `DELETE /unenroll` |
| Delivery folder | `codex-deliveries/` |

---

## Part 7 — Build Approach (After Brief Idea Approved)

Once Temple approves the Brief Idea:

- Build all 6 report routers + the Ritual Engine router as standalone files
- Deliver in one drop — no phased delivery within this module
- Include `vedic_shared_utils.py` (shared compute layer used by reports and the engine)
- Include `LOVE_MODULE_TEMPLE_HANDOFF_NOTES.md` covering: router registration list for `main.py`, APScheduler wiring guide for the `/check` endpoint, env vars, any frontend data contract notes for the dashboard

Temple reviews all files in one pass.

---

*This thread is the authoritative contract for the Love & Engagement Module and the Ritual Trigger Engine. The Ritual Engine is the commercial flagship of this module — design it as a production-grade subscription service, not a report.*

---
