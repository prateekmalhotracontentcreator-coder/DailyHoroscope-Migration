# Codex Brief — Commission I CPath-1 Item 5: Library Console

> To: Codex  
> From: EverydayHoroscope / Temple Team  
> CPath-1 Item: 5 of 8  
> Priority: HIGH — blocks items 6–8  
> Depends on: Items 1–4 (all committed ✅)

---

## Context

Commission I is the Knowledge Engine for EverydayHoroscope (India's Vedic astrology platform).  
Items 1–4 built the schema, paraphrase pipeline, index/scan engine, and Claude narrative generator.  
Item 5 is the **Library Console** — the admin UI that lets the Temple Team review, approve, and manage
imported interpretation rules, import batches, and the in-memory rule index.

Stack: FastAPI (Render) + React 18 (Vercel) + MongoDB (Motor async) + Pydantic v2.

---

## What You Will Build

Three files + two edits:

| Deliverable | Path | New or Edit |
|---|---|---|
| Knowledge router | `backend/knowledge_router.py` | NEW |
| Library Console page | `frontend/src/pages/admin/LibraryConsolePage.jsx` | NEW |
| Register router in server | `backend/server.py` | EDIT — 2 lines |
| Add route in App.js | `frontend/src/App.js` | EDIT — 2 lines |
| Add tab in AdminDashboard | `frontend/src/pages/admin/AdminDashboard.jsx` | EDIT — small |

---

## 1. Backend — `backend/knowledge_router.py`

Create a new FastAPI router file. **Do NOT add routes directly into server.py** — create the router file and Codex is done; the Temple Team will add the two registration lines to server.py.

### Imports available in the backend

```python
from fastapi import APIRouter, HTTPException, Query, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from knowledge_schema import (
    COLLECTION_INTERPRETATION_RULES,
    COLLECTION_IMPORT_BATCHES,
    ApprovalStatus,
)
from datetime import datetime, timezone
```

The router accesses `app.state.db` (Motor `AsyncIOMotorDatabase`) and
`app.state.knowledge_engine` (KnowledgeEngine instance) from the FastAPI `Request` object.

### Router definition

```python
router = APIRouter(prefix="/api/knowledge", tags=["knowledge-library"])
```

### Route 1 — List rules (paginated + filterable)

```
GET /api/knowledge/rules
```

Query params (all optional):
- `page: int = 1` — page number (1-based)
- `page_size: int = 50` — max 200
- `science_id: str | None` — filter by science_id field
- `category: str | None` — filter: rule's `categories` list contains this value
- `approval_status: str | None` — one of `pending_review`, `approved`, `rejected`
- `strength_band: str | None` — one of `low`, `medium`, `high`, `extreme`

Response shape:
```json
{
  "rules": [ { ...rule fields... } ],
  "total": 1234,
  "page": 1,
  "page_size": 50,
  "pages": 25
}
```

Each rule object in `rules` should include: `rule_id`, `science_id`, `life_domain`,
`categories`, `strength_band`, `approval_status`, `claim_axis`, `claim_polarity`,
`claim_scope`, `priority`, `intensity_score`, `active`, `created_at`, `updated_at`.
**Do not return `interpretation.full_text_passages`** in this list view (too heavy).

MongoDB query: build a filter dict from whichever query params are provided.
For `category`, use `{"categories": category}` (Mongo array contains).
Use Motor `.count_documents(filter)` for total, `.find(filter).skip(skip).limit(page_size)` for results.

### Route 2 — Get single rule

```
GET /api/knowledge/rules/{rule_id}
```

Returns the full `InterpretationRuleDocument` including passages.
Raises `404` if not found.

### Route 3 — Approve a rule

```
PATCH /api/knowledge/rules/{rule_id}/approve
```

Sets `approval_status = "approved"` and `updated_at = utcnow()`.
Returns `{"rule_id": rule_id, "approval_status": "approved"}`.
Raises `404` if not found.

### Route 4 — Reject a rule

```
PATCH /api/knowledge/rules/{rule_id}/reject
```

Sets `approval_status = "rejected"` and `updated_at = utcnow()`.
Returns `{"rule_id": rule_id, "approval_status": "rejected"}`.
Raises `404` if not found.

### Route 5 — List import batches

```
GET /api/knowledge/import-batches
```

No query params required. Returns all batches ordered by `created_at` descending.

Response shape:
```json
{
  "batches": [ { ...batch fields... } ]
}
```

Each batch object: `batch_id`, `source_book`, `import_status`, `approval_status`,
`rules_submitted`, `rules_imported`, `duplicate_count`, `error_count`,
`index_refreshed`, `created_at`, `updated_at`.

### Route 6 — Get single batch

```
GET /api/knowledge/import-batches/{batch_id}
```

Returns full `ImportBatchDocument`. Raises `404` if not found.

### Route 7 — Bulk approve all rules in a batch

```
POST /api/knowledge/import-batches/{batch_id}/approve-all
```

1. Find all rules where `source.batch_id == batch_id` and `approval_status != "approved"`.
2. Update them all: set `approval_status = "approved"`, `updated_at = utcnow()`.
3. Also set the batch's own `approval_status = "approved"`, `updated_at = utcnow()`.
4. Return `{"batch_id": batch_id, "rules_approved": <count of rules updated>}`.

### Route 8 — Index refresh status

```
GET /api/knowledge/index/status
```

Calls `request.app.state.knowledge_engine.index_refresh_status()` and returns the dict directly.
`index_refresh_status()` returns a plain Python dict — return it as-is.

### Route 9 — Trigger index refresh

```
POST /api/knowledge/index/refresh
```

Calls `request.app.state.knowledge_engine.schedule_index_refresh()`.
`schedule_index_refresh()` returns an `asyncio.Task` — do NOT await it (fire-and-forget).
Return immediately: `{"index_refresh_triggered": True}`.

---

## 2. Frontend — `frontend/src/pages/admin/LibraryConsolePage.jsx`

### File location and export

```
frontend/src/pages/admin/LibraryConsolePage.jsx
```

Export both default and named:
```jsx
export function LibraryConsolePage({ getAuthHeaders }) { ... }
export default LibraryConsolePage;
```

`getAuthHeaders` is a function that returns an object of HTTP headers (including the admin
auth token). Call it as `getAuthHeaders()` before any axios call.

### Layout and theme

Match AdminDashboard exactly:
- Dark background: `bg-gray-900` on the page, `bg-gray-800` on cards
- Gold accent: `text-yellow-400` / `border-yellow-400/30` / `bg-yellow-400/10`
- Use Tailwind utility classes — **no custom CSS**
- Use `lucide-react` icons (already installed)
- Use `axios` for API calls (already installed)
- Use `sonner` `toast` for success/error feedback (already installed)

### Sub-tabs

Three sub-tabs rendered as buttons at the top:
1. **Rules Browser** (default active)
2. **Import Batches**
3. **Index Status**

### Sub-tab 1 — Rules Browser

**Filter bar** (horizontal, above the table):
- Text input: search by `science_id` (debounced 400ms)
- Select: `approval_status` — options: All / Pending Review / Approved / Rejected
- Select: `strength_band` — options: All / Low / Medium / High / Extreme
- "Load" button triggers fetch

**Table columns:**
| Column | Field |
|---|---|
| Rule ID | `rule_id` (truncated to 12 chars, full on hover) |
| Science | `science_id` |
| Domain | `life_domain` |
| Categories | `categories` (joined with `, `) |
| Strength | `strength_band` badge |
| Status | `approval_status` badge |
| Actions | Approve / Reject buttons |

**Status badge colours:**
- `pending_review` → yellow (`bg-yellow-500/20 text-yellow-400`)
- `approved` → green (`bg-green-500/20 text-green-400`)
- `rejected` → red (`bg-red-500/20 text-red-400`)

**Strength band badge colours:**
- `low` → gray, `medium` → blue, `high` → orange, `extreme` → red

**Row actions:**
- "Approve" button: calls `PATCH /api/knowledge/rules/{rule_id}/approve`, then refreshes the row's status in state (no full reload needed — update the rule in the local array)
- "Reject" button: calls `PATCH /api/knowledge/rules/{rule_id}/reject`, same pattern
- "View" button: opens an inline expandable row (or a modal) showing the full rule's `interpretation.summary` + `interpretation.detailed` + `interpretation.positive_aspects` + `interpretation.challenging_aspects`

**Pagination:**
- Show `page` / `pages` and Prev / Next buttons
- `page_size` fixed at 50 in the URL param

### Sub-tab 2 — Import Batches

**Batch list** — one card per batch, showing:
- Source book name (`source_book`) — large text
- Batch ID — small mono text
- Status badges: `import_status` + `approval_status`
- Stats row: `rules_submitted` / `rules_imported` / `duplicate_count` / `error_count`
- Index refreshed indicator: green check or gray dash
- Created date

**Per-batch action:**
- "Approve All Rules" button — calls `POST /api/knowledge/import-batches/{batch_id}/approve-all`
- On success: toast "X rules approved", update the batch card to show `approval_status: approved`
- Disable the button if batch `approval_status` is already `approved`

### Sub-tab 3 — Index Status

**Status card** showing data from `GET /api/knowledge/index/status`.

The `index_refresh_status()` method returns a dict with at minimum:
- `rule_count` — number of rules in the current index
- `built_at` — ISO timestamp of last build (may be null)
- `index_refreshed` — boolean

Display these fields clearly. If `built_at` is null, show "Not yet built".

**Refresh Index button:**
1. User clicks "Refresh Index"
2. POST `/api/knowledge/index/refresh` — returns `{"index_refresh_triggered": true}`
3. Show a "Refreshing..." spinner state
4. Poll `GET /api/knowledge/index/status` every 3 seconds
5. Stop polling when the response `built_at` timestamp is newer than when the button was clicked
   (compare: store `preRefreshBuiltAt` before clicking; stop when `built_at !== preRefreshBuiltAt`)
6. Show toast "Index refreshed — X rules loaded" and update the status card

**Important polling constraint (Strategy C):**  
Stale reads are tolerated. The polling is just UI feedback — the index refresh happens in the
background (asyncio.Task). The UI should not block or error if polling takes up to 30 seconds.
Cap polling at 20 attempts (60 seconds total). If not confirmed after 20 attempts, show
"Refresh triggered — check again in a moment" and stop polling.

---

## 3. Edits to Existing Files

### `backend/server.py` — 2 lines to add

After all existing router imports (around line 80), add:
```python
from knowledge_router import router as knowledge_router
```

After all existing `app.include_router(...)` calls (around line 1910), add:
```python
app.include_router(knowledge_router)
```

### `frontend/src/App.js` — 2 lines to add

After the existing AdminDashboard lazy import (around line 23), add:
```jsx
const LibraryConsolePage = lazy(() => import('./pages/admin/LibraryConsolePage').then(m => ({ default: m.LibraryConsolePage })));
```

After the existing `/admin/blog` route (line 128), add:
```jsx
<Route path="/admin/library" element={<LibraryConsolePage />} />
```

### `frontend/src/pages/admin/AdminDashboard.jsx` — add Library tab

In the `tabs` array (around line 502), add one entry after the `notifications` tab:
```jsx
{ id: 'library', label: 'Library', icon: BookOpen },
```

(`BookOpen` is already imported in AdminDashboard.)

In the tab content section (after the `notifications` block), add:
```jsx
{activeTab === 'library' && <LibraryConsolePage getAuthHeaders={getAuthHeaders} />}
```

Add the import at the top of AdminDashboard:
```jsx
import { LibraryConsolePage } from './LibraryConsolePage';
```

---

## 4. Style Constraints

- **No smart/curly quotes** in JSX strings — use straight `"` and `'` only
- **No new npm packages** — axios, sonner, lucide-react are all already installed
- **No TypeScript** — plain JSX only
- **No PropTypes** — not used in this codebase
- **GlassCard pattern** (for prominent cards): `rounded-xl border border-yellow-400/20 bg-yellow-400/[0.04] shadow-sm`
- All table/list containers: `bg-gray-800 rounded-lg border border-gray-700`
- Loading states: simple text "Loading..." — no skeleton loaders needed

---

## 5. Validation Checklist (Codex self-check before submitting)

- [ ] `knowledge_router.py` imports cleanly (no missing symbols)
- [ ] All 9 routes are present
- [ ] `approve-all` uses `update_many` (not a loop of `update_one`)
- [ ] `schedule_index_refresh()` is NOT awaited (returns asyncio.Task — fire and forget)
- [ ] LibraryConsolePage exports both default and named export
- [ ] No curly/smart quotes in JSX
- [ ] Strategy C polling is capped at 20 attempts
- [ ] No new npm packages referenced

---

## 6. What the Temple Team Will Do After Receiving This Code

1. Review `knowledge_router.py` for correctness
2. Add the 2 server.py lines themselves (import + include_router)
3. Verify LibraryConsolePage JSX builds cleanly
4. Add App.js route and AdminDashboard tab themselves if Codex output for those needs adjustment
5. Commit as: `feat(knowledge-engine): CPath-1 item 5 — Library Console (Rules Browser + Import UI)`
