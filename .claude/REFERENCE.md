# REFERENCE.md -- Full Detail Archive
> Read only when needed. NOT auto-loaded at session start.
> Extracted from CLAUDE.md 2026-05-09 to reduce session token baseline.

---

## KE Batch Validation SOP
> Locked 2026-06-08. DO NOT add intermediate triage steps -- they cost extra API calls with zero benefit.

### The One-Pass Rule
Every new KE batch (ingested rules at `approval_status: "flagged"`) must be processed in **ONE validation run**, not two or three. The previous Remedies batch wasted API spend by splitting into: audit → triage → validate-PHR → validate-Bucket-C. That was wrong.

**Correct flow for any flagged batch:**
```
Ingest batch → rules land at approval_status: "flagged"
       ↓
Run: python3 backend/scripts/validate_[batch_name].py --dry-run   # review first
Run: python3 backend/scripts/validate_[batch_name].py             # live
       ↓
Outcomes: auto_approved | fixed+auto_approved | rejected
       ↓
Update TRACKER.md + #2_MASTER_TRACKER.md
```

No triage script. No PHR intermediate state (unless a human genuinely needs to review before approval). No second pass.

### Validation Script Template -- Key Requirements

1. **Query**: `approval_status: {"$in": ["pending_review", "pending_human_review", "flagged"]}`, `source.batch_id: {"$in": [target_batches]}` -- ingest scripts vary: SBC assigns `pending_human_review`, Remedies assigned `pending_review`. Always cast a wide net.
2. **Model**: `claude-haiku-4-5-20251001` for batch validation (cheap, fast, accurate for structured fixes). `claude-sonnet-4-6` only if haiku fails to provide a fix_value inline (rare).
3. **Batch size**: 7-10 rules per API call depending on field verbosity.
4. **Prompt must state explicitly** (copy-paste for every new batch):
   - What the library IS (classical Vedic / modern remedy / SBC / LK / etc.)
   - What NOT to flag (e.g. for remedy library: never flag for non-classical Vedic framework)
   - Validate ONLY: completeness, field consistency, language quality, internal consistency
5. **Fix fields**: always use dot-notation paths. Use `FIELD_PATH_MAP` to normalise bare names:
   ```python
   FIELD_PATH_MAP = {
       "trigger_condition":  "condition.trigger_condition",
       "planets_involved":   "condition.planets_involved",
       "houses_involved":    "condition.houses_involved",
       "start_day":          "interpretation.start_day",
       "mantra":             "interpretation.mantra",
       "summary":            "interpretation.summary",
       "detailed":           "interpretation.detailed",
   }
   ```
6. **Multi-fix support**: response format must be `"fixes": [{"fix_field": ..., "fix_value": ...}]` array, not single fix_field/fix_value. Allows fixing planets_involved + houses_involved + start_day + mantra in one verdict.
7. **DB writes**:
   - APPROVE → `approval_status: "auto_approved"`, `validation.verdict: "approved"`, add revalidation note
   - FIX → same as APPROVE + apply all fix fields atomically in one `$set`
   - REJECT → `approval_status: "rejected"`, `rejection_reason`, `rejected_at`
   - Error → leave at `flagged`, add `validation.revalidation_error` note

### When NOT to use AI validation (bulk-promote instead)

AI validation is only justified when rules have a **data-entry layer** that could introduce errors -- wrong mantras, empty condition arrays, wrong start days, truncated text from hand-authoring.

**Do NOT use paid API for:**
- Textbook-decoded rules where `full_text` is the verbatim passage (SBC, BPHS chapters) -- structural validation at ingest is sufficient
- Rules where condition arrays are intentionally empty by design (SBC uses engine_specification conditions, not planet/house arrays)
- Any batch where ingest structural validation passed 0 issues AND content is classical knowledge not hand-authored

**Use `promote_*_to_auto_approved.py` pattern instead:** bulk MongoDB `update_many` → `auto_approved`. No API cost.

**Decision rule:** Before writing a validation script, check: *what specific field errors am I expecting to find?* If the answer is "none -- it came from a clean textbook decode," bulk-promote.

### Prompt DO NOT flags by library type

| Library | DO NOT flag for |
|---|---|
| Remedies -- Crystals / Chakra | Non-classical Vedic, crystal healing, chakra framework, modern gemstones |
| Remedies -- Gemstones | Non-classical Vedic provenance. Flag ONLY: empty arrays, wrong start day, factual errors |
| Remedies -- Dhana / LK | Non-classical Vedic. LK has its own planetary rulerships -- do not apply BPHS rules |
| SBC (Shani/Brahma/Chandra) | Non-BPHS framework -- SBC is a specific school; do not cross-validate with standard Vedic |
| BPHS chapters | Nothing classical is wrong by definition. Flag only: truncated text, condition mismatch, incoherence |

### Reference Scripts (use as base for new batches)
| Script | Batch | Notes |
|---|---|---|
| `backend/scripts/validate_remedy_library.py` | Remedies PHR (93 rules) | PHR + validator_error query. Good template for modern remedy libs. |
| `backend/scripts/validate_bucket_c_remedies.py` | Remedies flagged (42 rules) | Multi-fix array format. FIELD_PATH_MAP normalisation. Best current template. |

**For any new batch**: copy `validate_bucket_c_remedies.py`, update query (batch_ids), update system prompt (library type + DO NOT flags), run dry-run first, then live.

### Cost Reference (2026-06-08 actuals)
- 135 Remedy rules validated across 2 scripts: ~$0.08-0.12 total (haiku batch + no sonnet calls needed -- haiku provided all fix_values inline)
- If the correct one-pass approach had been used: ~$0.04-0.06 (single script, 20 API calls @ batch-size 7)
- Waste from triage-then-validate pattern: ~50% of API spend

---

## Ayanamsha Decision Register

Full register: **`AYANAMSHA_DECISION_REGISTER.md`** (repo root) -- read before any pyswisseph computation change.

**One-line rule:**
- Vedic features (birth chart, dasha, panchang, kundali): `swe.SIDM_LAHIRI`
- KP features (sub-lords, cusps, KP Oracle): `swe.SIDM_KRISHNAMURTI`

**Live bug (AYA-1):** `backend/kp_engine.py` line 11 uses `SIDM_LAHIRI` -- must be `SIDM_KRISHNAMURTI`. Fix pending TT sign-off. Difference = 5.795 arcminutes at J2000.

---

## Panchang Engine Detail

**What it computes:** Sunrise/Sunset/Moonrise/Moonset (with seconds), Tithi, Nakshatra, Yoga, Karana, Paksha, Lunar month, Samvat, Sun/Moon signs, Amrit Kalam, Special Yogas (Amrit Siddhi, Sarvartha Siddhi, Ravi Yoga), True Choghadiya (8 daylight + 8 night slots).

**Timing windows:** Brahma Muhurta (96 min pre-sunrise) | Amrit Kalam | Rahu Kaal | Yamaganda | Gulika Kaal | Dur Muhurta ×2 | Abhijit Muhurta | Vijaya Muhurta

**Accuracy benchmark (New Delhi, 26 Mar 2026):** Sunrise 06:18 ✅ | Tithi Shukla Ashtami ✅ | Nakshatra Ardra ✅ | Yoga Shobhana ✅ | Rahu Kaal 01:58 PM ✅ | Abhijit 12:02 PM ✅ | Moonrise 11:59 AM ✅

---

## Frontend Pages Detail

- **PanchangPage.jsx** -- 6-tab sub-nav (Today/Tomorrow/Tithi/Choghadiya/Calendar/Festivals), 318-city picker with TZ badge, Five Limbs card, Timing Windows, Special Yogas, Share card, Facebook post
- **TarotPage.jsx** -- 3 tabs (Daily Draw/Spreads/History), flipping animation, 78-card SVG deck
- **NumerologyPage.jsx** -- 10 report types, computed numbers grid, remedy notes
- **BirthChartPage.jsx + BrihatKundliPage.jsx** -- Full Kundali UI, backend: vedic_calculator.py
- **Horoscope Pages (Daily/Weekly/Monthly)** -- Share cards, element-based theming, Facebook post
- **Admin Console (/admin/dashboard)** -- Overview/System/Users/Reports/Payments/Messages/Blog/Notifications tabs. Notifications: Subscribers / Compose / Scheduled / History / Social Media

---

## Share Cards (ShareCard.jsx)

**PanchangShareCard:** 900px, offscreen render (left: -9999px), gold header, Sun/Moon 4-col row, Five Limbs 3×2, Auspicious/Inauspicious timing tables, Special Yoga badge, footer.

**HoroscopeShareCard:** 900px, sign symbol in element-colored circle, sign name/dates/element/type badge, overview (first 2 sentences), lucky elements, footer.

**ShareButtons:** WhatsApp / Facebook / X / Instagram / YouTube / Save Card / Copy Link. Mobile: Web Share API. Desktop: canvas.toDataURL(). iOS: canvas.toBlob() → window.open(). html2canvas with onclone (no flash).

---

## YouTube Integration

OAuth: Google Cloud → refresh token in MongoDB `app_settings.youtube_refresh_token`.
Pipeline: PNG → ffmpeg (`-preset veryfast -threads 1 -crf 18 -tune stillimage`, 30s) → MP4 → YouTube Data API v3 resumable upload.
BackgroundTasks (async, ~2-4 min). Check: studio.youtube.com → Content.
Routes: `/api/admin/youtube/status|auth-url|callback|disconnect`

---

## WhatsApp Integration

Meta Cloud API v22.0. Template: `everydayhoroscope_update` with `{{customer_name}}` + `{{update_content}}`.
Phone `+91 96431 10001` (ID: `1062698816928895`) -- **PENDING**: complete OTP in WhatsApp Manager + add payment method.
WABA ID: `754513054261096`. Token: must be WhatsApp-specific (not FB System User token).

---

## Meta / Social Credentials

| Credential | Value |
|---|---|
| Meta App ID | 1594770155009283 |
| Business Manager ID | 878532341248169 |
| Facebook Page ID | 1084672598054073 |
| FB System User | EverydayHoroscope Bot (never-expires token) |
| YouTube | OAuth connected via Admin Console |
| WhatsApp Phone ID | 1062698816928895 -- Pending |
| WhatsApp WABA ID | 754513054261096 |
| Instagram Business ID | Pending (Meta dashboard loading issue) |

---

## Codex Workflow

1. Claude Code drafts commission brief
2. Prateek submits to Codex → receives code
3. Prateek pastes output here
4. Claude Code: aligns theme, wires Router + server.py, fixes quotes, verifies build, commits

**Smart quote fix:**
```bash
node -e "
let f=require('fs'),p='frontend/src/pages/TargetFile.jsx';
let c=f.readFileSync(p,'utf8');
c=c.replace(/"/g,'\"').replace(/"/g,'\"')
   .replace(/'/g,\"'\").replace(/'/g,\"'\");
f.writeFileSync(p,c);console.log('Done');"
```

Build verify: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build`

---

## Architecture Rule -- Commission Brief Checklist

Before ANY Codex brief:
1. Verify item exists in CPath-1 (CONTRACT.md §21)
2. Confirm exact item number and phase
3. Confirm dependencies complete
4. Read locked spec in CONTRACT.md (TD-xx)
5. Read docx mockup if exists (`.claude/` folder)
6. State: "All dasha/astronomical data from `vedic_calculator.py`"
7. State: "Do NOT add dasha functions to `knowledge_engine.py`"

---

## Completed Features (as of 2026-05-09)

Panchang ✅ | Choghadiya ✅ | Amrit Kalam ✅ | Special Yogas ✅ | Panchang share card ✅ | Horoscope share cards ✅ | Share download (desktop+mobile+iOS) ✅ | Facebook posting ✅ | YouTube posting ✅ | Tarot ✅ | Numerology ✅ | Kundali ✅ | Razorpay ✅ | SEO/GA4 ✅ | GSC ✅ | Bing ✅ | Admin Console full ✅ | Email (Resend) ✅ | Scheduled notifications ✅ | Social Media tab ✅

## Pending

WhatsApp 🔜 (OTP) | Instagram 🔜 (Account ID) | Scheduled social auto-post 🔜 | Razorpay live keys 🔜

---

## Local Dev

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn server:app --reload --port 8000

# Frontend
cd frontend && npm install && npm start
# .env.local: REACT_APP_BACKEND_URL=http://localhost:8000
```
