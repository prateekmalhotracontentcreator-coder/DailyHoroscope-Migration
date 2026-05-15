# Commission KP-2A -- KP Oracle: Bundle Editorial + Share Card + Remedies Admin Frontend

> EverydayHoroscope · Stack: React 18, Tailwind CSS, FastAPI, MongoDB  
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`  
> Live app: https://www.everydayhoroscope.in/krishna-prashnavali  
> Date issued: 2026-05-14

---

## Context

The Krishna Prashnavali oracle is fully live. The 18×18 grid, 36-answer bundle, deterministic chaupai algorithm, bilingual content, and all backend routes are production-ready. This commission covers three discrete, non-overlapping tasks that complete the Phase 2A layer.

**Production smoke test completed 2026-05-15 (M-3):**
- Report generation: ✅ Excellent
- Premium gate: ✅ Confirmed working
- Share card / download: ❌ Not present -- Task 2 of this commission delivers it
- Section box alignment: Minor re-alignment needed -- address as part of Task 1 UI polish
- Saved Previous Readings: not loading in the history section -- under CC investigation (KP-OP-8); do NOT attempt to fix in this commission

**Existing files (do NOT restructure):**
- `backend/assets/krishna_oracle/krishna_oracle_content.json` -- the v2 canonical bundle
- `backend/scriptural_oracle_router.py` -- router prefix `/api/oracle/krishna-prashnavali`
- `frontend/src/pages/kp/KrishnaOraclePage.jsx` -- main page (704 lines)
- `frontend/src/components/KrishnaOracleGrid.jsx` -- grid component
- `backend/remedies_router.py` -- remedies router (prefix `/api/remedies`)

---

## Task 1 -- v2 Bundle Editorial Completion

### What to edit
File: `backend/assets/krishna_oracle/krishna_oracle_content.json`

The bundle contains 36 answer objects under `answers` (a list). Each object has these fields:
`answer_id`, `answer_slot`, `source_category`, `verdict_traditional`, `verdict_backend`, `verdict_display`, `chaupai_phrase`, `title`, `krishna_answer`, `meaning`, `what_to_do`, `precaution`, `duration`, `krishna_message`, `theme_tags`, `source_ref`, `content_status`, `behavioral_remedy`, `remedy_ref`

### Editorial changes -- apply across all 36 slots

**A. Unique `krishna_answer` in divine voice (ALL 36 slots)**  
Current: `krishna_answer.english_block` duplicates `title.english_block` verbatim.  
Required: `krishna_answer` must be Krishna speaking directly to the seeker -- a first-person divine voice, distinct from the title label.  
Pattern: `"O seeker, [direct divine counsel in 1-2 sentences related to the slot's theme]"`  
`title` = a label (e.g., "Work will be successful"). `krishna_answer` = the voice (e.g., "O seeker, your path is clear. Move forward with faith and righteous action.").  
Apply this distinction to all 36 slots. Sanskrit block must be authored in parallel.

**B. Honorifics on all divine names (ALL 36 slots, ALL text fields)**  
Apply these substitutions globally across every `sanskrit_block` and `english_block` in every field:

| Current | Correct |
|---|---|
| हनुमान | हनुमान जी |
| Hanuman | Hanuman Ji |
| कृष्ण | श्री कृष्ण जी |
| Krishna | Shri Krishna Ji |
| राम | श्री राम जी |
| Ram | Shri Ram Ji |
| Any Goddess name | Maa [Name] |

**C. Slot-specific editorial changes**

**Slot 11 (WAIT verdict) -- title edit**  
Current title: `"Delay in work"` -- reads as negative  
New title: `"Success through patience -- your effort is not lost"`  
`krishna_answer` for Slot 11: Counsel on the Dhairya (patience) theme in divine voice.

**Slot 19 (NO verdict) -- remedy specificity + source_ref**  
Current remedy: generic.  
New `remedy.english_block`: `"Recite Hanuman Ji Chalisa for 11 consecutive days, or chant Om Namo Hanumate Namah 108 times each morning at sunrise."`  
Update `source_ref` to include: `"Hanuman Chalisa -- Tulsidas (Verse 1-2); Sankat Mochan tradition"`

**Slot 31 (PRAY verdict) -- remedy restructure**  
Current: behavioral guidance sitting in `remedy` field.  
Restructure:  
- Move existing behavioral content to `behavioral_remedy.english_block` (e.g., "Practice humility and stop ego-driven reactions.")  
- Author a new ritual `remedy.english_block`: a specific sunrise water-offering or similar ritual action  
- Both `behavioral_remedy` and `remedy` must be non-empty

**Slot 33 (PRAY verdict) -- cross-module tag**  
Add a `cross_module_trigger` field to this slot only:  
```json
"cross_module_trigger": {
  "module": "lk_debt_audit",
  "condition": "returned_inside_strategist",
  "prompt": "This answer points to an ancestral karmic duty. Your Lal Kitab Karmic Debt profile is relevant -- review your Debt Audit."
}
```

**D. `content_status` update**  
After all edits, update `content_status` on each modified slot from `"temple_reviewed_pending_remedies_runtime"` to `"temple_approved_v2"`.  
Update the bundle-level `content_status` field to `"fully_authored_v2"`.

---

## Task 2 -- KP Visual Share Card

### What to build
New component: `frontend/src/components/KrishnaShareCard.jsx`  
This follows the exact same pattern as `HoroscopeShareCard` in `frontend/src/components/ShareCard.jsx`.

### Spec

**Dimensions:** 900px wide, fixed height ~520px  
**Position:** `position: fixed; left: -9999px; top: 0` (offscreen, same pattern as existing share cards)  
**Ref:** Accept a `ref` prop for html2canvas capture

**Layout:**
```
┌─────────────────────────────────────────────────┐
│  [Logo] EverydayHoroscope         [Gold divider] │  ← header, bg: deep navy/indigo
│         "Krishna Prashnavali"                    │
├─────────────────────────────────────────────────┤
│  [Verdict badge]  YES / WAIT / NO / PRAY        │  ← large centered badge
│                                                  │  bg matches verdict:
│  "सिद्ध काज सब होये"  (chaupai_phrase)          │    YES=gold, WAIT=blue, NO=red, PRAY=purple
│                                                  │
│  [Title in English]                              │
├─────────────────────────────────────────────────┤
│  [Krishna message -- krishna_answer.english_block]│  ← italic, Playfair Display font
│  (max 2 lines, truncate with ellipsis)           │
├─────────────────────────────────────────────────┤
│  🌿 [what_to_do.english_block -- first sentence] │  ← action line
├─────────────────────────────────────────────────┤
│  everydayhoroscope.in/krishna-prashnavali        │  ← footer
└─────────────────────────────────────────────────┘
```

**Color tokens:** Use CSS vars: `--gold: #c5a059`, `text-foreground`, `bg-card`. Match existing share card styling.

**Props:**
```typescript
{
  reading: {
    verdict_display: string,       // "YES" | "WAIT" | "NO" | "PRAY"
    chaupai_phrase: string,        // Sanskrit chaupai
    title: { english_block: string },
    krishna_answer: { english_block: string },
    what_to_do: { english_block: string },
    krishna_message: { english_block: string }
  }
}
```

### Wire into KrishnaOraclePage.jsx

In `KrishnaOraclePage.jsx`, the share button currently calls a clipboard copy function. Replace/extend with:
1. Add `useRef` for `KrishnaShareCard`
2. On "Share" click: capture card via html2canvas (same pattern as `ShareButtons` in `ShareCard.jsx`)
3. Show 4 share buttons: WhatsApp, Facebook, Save, Copy Link
4. "Post to Page" Facebook button: include `fbPageCaption` prop when admin is logged in

Import pattern (same as existing):
```jsx
import html2canvas from 'html2canvas';
```

---

## Task 3 -- Remedies Admin Tab (Frontend Only)

### What exists
Backend endpoint already live: `GET /api/remedies/admin/records`  
This is in `backend/remedies_router.py` at line 866.  
Auth: requires admin token (same as other admin endpoints).

### What to build
New sub-tab in `frontend/src/pages/admin/AdminDashboard.jsx`

**Tab placement:** Add "Remedies" as a new top-level tab in `AdminDashboard.jsx` alongside the existing tabs (Overview, System, Users, etc.). **Do NOT place inside Library Console.**

**Tab content -- `RemediesAdminTab` component:**

**Controls row:**
- Search input (filter by `remedy_id`, `planet`, `tradition`, or free text)
- Filter dropdown: `All Collections` | `krishna_prashnavali_remedies` | `jyotish_remedies` | `lk_remedies`
- Filter dropdown: `All Statuses` | `approved` | `pending_human_review` | `flagged`
- Results count badge

**Records table columns:**
| remedy_id | tradition/science | planet | status | updated | actions |

**Row expand:** Clicking a row expands an inline detail panel showing:
- `mantra` (if present)
- `ritual` (if present)
- `behavioral_remedy` (if present)
- `remedy_ref` value
- Full JSON viewer (collapsible)

**Inline status update:** Each row has a status dropdown (`approved` / `pending_human_review` / `flagged`). On change → `PATCH /api/remedies/admin/records/{remedy_id}/status` (add this endpoint to `remedies_router.py` -- simple single-field update).

**Style:** Match existing Admin Console card/table pattern. Use `GlassCard` (`rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm`).

### New backend endpoint to add (small addition)
In `backend/remedies_router.py`, add:
```python
@router.patch("/admin/records/{remedy_id}/status")
async def update_remedy_status(remedy_id: str, body: RemedyStatusUpdate, admin=Depends(require_admin)):
    # Update approval_status field in the relevant collection
    # Try krishna_prashnavali_remedies first, then other collections
```

---

## Constraints

- Do NOT modify `kp_engine.py`
- Do NOT modify the chaupai extraction algorithm in `scriptural_oracle_router.py`
- Do NOT change the 18×18 grid matrix or cell_answer_map
- The `answers` list order (slots 1-36) must remain unchanged
- All new React components must use existing Tailwind tokens and GlassCard pattern
- No new npm packages unless absolutely unavoidable

## Acceptance Criteria

- [ ] All 36 slots have unique `krishna_answer` text distinct from `title`
- [ ] All divine names have correct honorifics in both language blocks
- [ ] Slots 11, 19, 31, 33 edited per spec above
- [ ] `KrishnaShareCard.jsx` renders correctly offscreen, captures via html2canvas
- [ ] Share card shows verdict badge in correct color, chaupai, krishna_answer, what_to_do
- [ ] Share buttons: WhatsApp, Facebook, Save, Copy Link wired
- [ ] Remedies Admin tab appears in AdminDashboard
- [ ] Records load from `/api/remedies/admin/records`
- [ ] Search, collection filter, status filter all functional
- [ ] Inline status PATCH works and reflects immediately in UI
- [ ] All code committed to `main`
