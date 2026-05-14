# KP_INGEST.md  (Krishna Prashanavali — Scriptural Oracle)
> Created: 2026-05-11  |  STATUS: MIGRATION PENDING

---

## Module Overview

Krishna Prashanavali is a deterministic oracle module built by Codex in a test host.
It must be migrated to the live codebase before any ingest work begins.

---

## File Migration Status

| Source (Codex test host) | Destination (live codebase) | Status |
|---|---|---|
| `/Users/apple/DailyHoroscope-Codex-Test/backend/scriptural_oracle_router.py` | `backend/scriptural_oracle_router.py` | ✅ Migrated 2026-05-11 |
| `/Users/apple/DailyHoroscope-Codex-Test/frontend/src/pages/KrishnaOraclePage.jsx` | `frontend/src/pages/KrishnaOraclePage.jsx` | ✅ Migrated 2026-05-11 |
| `/Users/apple/DailyHoroscope-Codex-Test/frontend/src/components/KrishnaOracleGrid.jsx` | `frontend/src/components/KrishnaOracleGrid.jsx` | ✅ Migrated 2026-05-11 |
| `/Users/apple/DailyHoroscope-Codex-Test/frontend/src/utils/chaupaiExtractor.js` | `frontend/src/utils/chaupaiExtractor.js` | ✅ Migrated 2026-05-11 |
| `/Users/apple/Documents/New project/KRISHNA_ORACLE_CONTENT_CANONICAL_V2_FOR_TEMPLE.json` | `backend/assets/krishna_oracle_content.json` | ❌ Pending Codex v2 bundle delivery |

**Use v2 Temple bundle** — NOT the host-test bundle. Wait for Codex to deliver updated bundle with `behavioral_remedy` + `remedy_ref` fields before migrating content.

---

## Oracle Content Architecture (Final — Do Not Change)

| Parameter | Value |
|---|---|
| Answer slots | 36 |
| Grid | 18×18 (324 cells) |
| Verdicts | 4: YES (Pratibha) / WAIT (Dhairya) / NO (Pratrodha) / PRAY (Bhakti) |
| Selection formula | `chaupaiExtractor.js` — cell tap → 36-slot index |
| Content fields | title, chaupai_phrase, krishna_answer, meaning, what_to_do, remedy, behavioral_remedy (NEW), precaution, mantra, duration, krishna_message, theme_tags, remedy_ref (NEW) |

---

## Remedies Engine Integration

### `krishna_prashnavali_remedies` Collection

| Parameter | Value |
|---|---|
| science_id | `krishna_prashnavali_remedies` |
| collection | `knowledge_rules` (or `interpretation_rules` — TBD at commission opening) |
| Source | `/Users/apple/Documents/New project/KRISHNA_PRASHNAVALI_REMEDIES_INGEST_V1.json` |
| Status | ❌ Not yet ingested — pending Codex updated bundle + formal commission opening |
| Scope | App-wide — queryable by Tarot, Numerology, Strategist, not KP-exclusive |

### Structural Rules
- All 36 KP answer slots carry `remedy_ref` ID pointing to a record in this collection
- `remedy_type` field: `"ritual"` or `"behavioral"` (both supported)
- Cross-discipline tags allowed: e.g. `science:krishna_prashnavali + science:jyotish_saturn`
- No mantras hardcoded in KP module — all via `remedy_ref` lookup

---

## Editorial Decisions Applied (2026-05-11)

| Slot | Change |
|---|---|
| All 36 | `krishna_answer` must be unique per slot (not repeat of `title`) |
| All 36 | `behavioral_remedy` new field added |
| All 36 | Honorifics: Ji/Maa/Shri on all divine names |
| All 36 | `remedy_ref` replaces inline `mantra` + `remedy` strings |
| Slot 11 | Title: "Delay in work — success through patience. Maintain momentum." |
| Slot 19 | Remedy: Hanuman Ji Chalisa 11 days / 108 chants; source_ref += Gita Ch.3 V.35 |
| Slot 31 | Behavioral remedy → `behavioral_remedy` field; ritual `remedy` added |

Full editorial decisions: `/Users/apple/Documents/New project/KRISHNA_ORACLE_EDITORIAL_SAMPLE_REVIEW_SHEET.md`

---

## Routes to Register

```python
# backend/server.py
from scriptural_oracle_router import router as kp_router
app.include_router(kp_router, prefix="/api/oracle")
```

```javascript
// frontend/src/App.js
<Route path="/krishna-prashnavali" element={<KrishnaOraclePage />} />
```

NavBar: Direct top-level link (not in any dropdown)

---

## Dual Placement in App

1. **Standalone** — `/krishna-prashnavali` (direct NavBar link)
2. **Strategist Gate 0** — inline in War Room (`StrategistPage.jsx`) — verdict stored in `kp_sessions` collection

---

## Status
Migration: ✅ CODE FILES LIVE (2026-05-11) | Content bundle: ⚠️ AWAITING CODEX v2 DELIVERY | Remedies collection: ❌ NOT INGESTED

### Routes Registered
- Backend: `from scriptural_oracle_router import router as kp_router` + `app.include_router(kp_router)` — live
- Frontend: lazy import `KrishnaOraclePage` + `<Route path="/krishna-prashnavali" element={<ProtectedRoute><KrishnaOraclePage /></ProtectedRoute>} />` — live
- NavBar: `{ label: 'Krishna Prashanavali', icon: Sparkles, path: '/krishna-prashnavali' }` — direct top-level link, live
