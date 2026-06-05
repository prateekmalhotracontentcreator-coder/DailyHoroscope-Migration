# Claude Working Protocol -- EverydayHoroscope

> **Last updated:** 2026-05-29
> **Reason (latest):** Full audit revealed CC was building component approximations (~50% fidelity) instead of integrating CD-delivered HTML files. Two new process docs added: PROCESS_CD_INTEGRATION_PROTOCOL.md and PROCESS_CD_COMMISSION_BRIEF_QUALITY.md. Rules 10-12 added below.
> **Reason (original):** Half a day was lost because Claude attempted browser-based GitHub edits instead of using the GitHub MCP connector that was available all along.

---

## 🔴 RULE 1 -- Fix Before Moving Forward

**Never skip a failing fix and move to the next task.**

If a fix is partially done or uncertain, STOP and resolve it fully before touching anything else. A half-fixed bug compounds into a full-day debugging session. This is not optional.

- If a Vercel build fails → fix the syntax error FIRST, then continue
- If a Render API returns 500 → fix the backend FIRST, then test frontend
- If a commit didn't go through → verify it landed FIRST, then proceed

---

## 🔴 RULE 2 -- Always Use the GitHub MCP Connector for Pushes

**The GitHub connector (`github:push_files`, `github:create_or_update_file`) is ALWAYS the right way to push code.**

### ✅ CORRECT method (use this every time):
```
github:push_files        → push multiple files in one commit
github:create_or_update_file → push a single file
github:get_file_contents → read current file + get SHA before updating
```

### ❌ WRONG methods (never use these for pushing code):
- Browser GitHub web editor (copy/paste via clipboard)
- `git push` from bash (no auth token available in container)
- GitHub REST API via `fetch()` from browser JS (CORS blocked)
- GitHub GraphQL from browser (session cookies insufficient)

### Why the browser editor fails:
- The GitHub editor uses CodeMirror 6 with a virtualised DOM -- `innerText` only returns visible lines, so you cannot verify what was actually pasted
- The clipboard API requires document focus, which is unreliable in automated browser sessions
- The commit modal is triggered by a React event that doesn't always fire from programmatic clicks
- **There is no reliable way to verify the correct content was committed via browser automation**

---

## 🔴 RULE 3 -- Always Get the File SHA Before Updating

When using `github:create_or_update_file`, the SHA of the existing file is required. Always fetch it first:

```
github:get_file_contents → returns content + SHA
then use that SHA in github:create_or_update_file
```

Missing the SHA causes a 422 conflict error and the push silently fails.

---

## 🟡 RULE 4 -- Verify Every Commit Landed

After every push, confirm the commit SHA appears on GitHub before moving on:

```
github:get_commit(sha='main') → check latest commit message and files changed
```

Or check the live API endpoint directly to confirm the fix is working.

---

## 🟡 RULE 5 -- Check Render Logs Before Guessing at the Fix

When a backend API returns 500, always read the Render logs first. Do not guess.

- Navigate to https://dashboard.render.com → service → Logs
- Read the full Python traceback -- it gives the exact file, line number, and error
- Fix exactly what the log says, nothing more

The Panchang `rise_trans` bug required 3 iterations because the error message was read incorrectly the first time. The log told us exactly what was wrong from the start.

---

## 🟡 RULE 6 -- Test the API Directly Before Calling It Fixed

After every backend fix, hit the endpoint directly:

```
https://everydayhoroscope-api.onrender.com/api/panchang/daily
https://everydayhoroscope-api.onrender.com/api/health
```

Only mark a fix as done when the API returns 200 with valid JSON. "Render is green" does not mean the endpoint works.

---

## 📋 Standard Push Workflow (copy this every time)

```
1. Read current file:      github:get_file_contents(path, owner, repo)
2. Note the SHA from step 1
3. Make the edit in memory / in Claude's container
4. Push:                   github:create_or_update_file(path, content, sha, message)
   OR for multiple files:  github:push_files(files[], message)
5. Verify:                 github:get_commit(sha='main') -- confirm commit landed
6. Test live:              Hit the actual URL to confirm it works
```

---

## 🔴 RULE 9 -- Never Directly Edit Codex Deliverable Files (MANDATORY)

**If even a single line of code needs to change in a file delivered by Codex, the change must be sent back to the relevant Codex thread -- not made directly by Claude Code.**

> **Why this rule exists:** 19 April 2026 -- Claude Code made direct edits to `knowledge_engine.py`, `server.py`, and `ArcAngelPanel.jsx` (all Codex Sprint 3 / Arc Angel UI deliverables) without informing the Codex threads. This leaves Codex out of sync with the live codebase, which will cause conflicts and regressions on the next iteration.

### What counts as a "Codex deliverable file"

Any file that was **created or substantially authored** by a Codex commission -- regardless of which sprint or thread it came from. Common examples:

| File | Codex thread |
|---|---|
| `backend/knowledge_engine.py` | Commission I (Knowledge Engine) |
| `backend/server.py` routes added by Codex | Commission I sprints |
| Any file in `frontend/src/` delivered by Codex | Respective UI commission |
| `backend/scripts/ingest_bphs_dasha_v1.py` | BPHS ingest commission |

### Exceptions -- Claude Code MAY edit directly

- **Existing project files** that Codex never touched (e.g. `NavBar.jsx` when Codex explicitly said it lacked access)
- **Documentation files** (CLAUDE.md, WORKING_PROTOCOL.md, CONTRACT.md)
- **Emergency hotfixes** where a production break requires an immediate one-line patch -- but Codex must be notified in the same session

### The correct workflow

```
1. Identify the change needed in a Codex deliverable
2. Write a clear change note: file path + exact lines to add/remove + reason
3. Send to the relevant Codex thread as an amendment
4. Claude Code integrates the returned code (does not re-author it)
5. If Codex is unavailable and a fix is urgent → apply as hotfix, document in
   a CODEX_AMENDMENT log entry, flag clearly for next Codex session
```

### Codex amendments made on 19 April 2026 (need to be sent back)

The following direct edits were made before this rule was established. They must be communicated to the respective Codex threads at the next session:

**Knowledge Engine thread (Sprint 3 -- `knowledge_engine.py` + `server.py`):**
- Added `NATURAL_BENEFICS`, `NATURAL_MALEFICS`, `ARC_ANGEL_BASELINE_CONFIDENCE_PCT = 42`
- Added `_natural_quality(planet)` -- Legacy Model fallback for period quality
- Modified `_quality_from_rules()` -- added TD-29 fallback as final `return` branch
- Modified `/api/knowledge-engine/arc-angel-windows` endpoint -- enriched response from bare dict to list; added `domain_id`, `domain_label`, `period_quality_now`, `confidence_pct` per domain; added `overall_confidence_pct`

**Arc Angel UI thread (`ArcAngelPanel.jsx`):**
- Removed `subscription` from `useAuth()` destructuring (AuthContext does not expose it)
- Replaced birth data source: was `user.birth_date` / `user.birth_lat` etc. → now fetches `/api/profile/birth` and reads `date_of_birth`, `time_of_birth`, `location` from saved profile
- Fixed API params: was `birth_lat`/`birth_lon`/`timezone` → now `birth_place` (city string) matching backend endpoint signature

---

## 🔴 RULE 7 -- Codex Commission Brief Gate (MANDATORY -- no exceptions)

**Before drafting ANY Codex commission brief, complete ALL of the following steps. Do not skip even one.**

> **Why this rule exists:** On 18 April 2026, a full day was lost because the Arc Angel commission brief was drafted without reading CONTRACT.md Section 19 (TD-23) or the canonical docx mockup. The brief specified a standalone two-column page. The locked spec required a 4-column table embedded in a left-nav sidebar. The resulting architecture had to be completely discarded.

### Pre-brief checklist (verify each item before writing a single word of the brief)

```
[ ] 1. Confirm the item exists in CPath-1 (CONTRACT.md Section 21) -- get the exact item number
[ ] 2. Confirm all dependency items are ✅ complete -- do not brief an item whose deps are open
[ ] 3. Read the relevant TD-xx entry in CODEX_KNOWLEDGE_ENGINE_CONTRACT.md
[ ] 4. Check .claude/ folder for any canonical docx mockup -- read it with the docx skill FIRST
[ ] 5. Re-read the locked spec section in CONTRACT.md that the TD-xx entry references
[ ] 6. State explicitly in every brief: "All dasha/astronomical data MUST come from vedic_calculator.py"
[ ] 7. State explicitly in every brief: "Do NOT add dasha/calculation functions to knowledge_engine.py"
```

### Failure modes that trigger this rule

- Treating a new commission as a "new design problem" without checking whether the architecture is already locked
- Reading only handover notes instead of the source CONTRACT
- Drafting briefs from memory of the design intent rather than the locked spec document
- Skipping the docx mockup because "I already know what this should look like"

---

## 🔴 RULE 8 -- Legacy Model is the Sole Source of Live Astronomical Data

**`vedic_calculator.py` and `panchang_router.py` are the ONLY sources of live dasha, chart, and panchang data. `knowledge_engine.py` interprets -- it does NOT compute.**

```
✅ CORRECT: knowledge_engine.py imports calculate_vimshottari_dasha from vedic_calculator.py
❌ WRONG:   knowledge_engine.py defines its own compute_dasha_timeline() function
✅ CORRECT: Arc Angel backend route calls vedic_calculator.calculate_vimshottari_dasha()
❌ WRONG:   Arc Angel backend route calls knowledge_engine.compute_dasha_timeline()
```

Every Codex brief and every backend route for Arc Angel, Knowledge Engine reports, and any dasha-powered feature must follow this rule.
Full details and Integrated Approach definition: CLAUDE.md Section 16.

---

## 📋 Infrastructure Quick Reference

| Service | URL | Notes |
|---------|-----|-------|
| Frontend | https://www.everydayhoroscope.in | Vercel, auto-deploys on push to main |
| Backend API | https://everydayhoroscope-api.onrender.com | Render Docker, ~2-3 min deploy |
| Health check | /api/health | Must return `{"status":"ok"}` |
| Panchang API | /api/panchang/daily | Key endpoint, was broken by pyswisseph |
| GitHub repo | github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration | main branch |
| Render dashboard | https://dashboard.render.com | Check logs here on any 500 error |

---

## 📋 What Broke and Why (Session Log 2026-03-25 / 26)

### Problem 1 -- Panchang pages blank (frontend)
**Root cause:** NavBar sent users to `/panchang/today`, `/panchang/tithi`, `/panchang/choghadiya` but `PanchangPage.jsx` only handled `daily`, `calendar`, `festivals`. No ALIAS map existed.
**Fix:** Replaced `PanchangPage.jsx` with full version including ALIAS map and 6 views.
**Commit:** `53f6f48`

### Problem 2 -- Email overflow on Home page
**Root cause:** Email `<p>` tag had no `truncate` class; flex container had no `min-w-0`.
**Fix:** Added `truncate break-all` to email `<p>` in `UserAccountMenu.jsx`; added `min-w-0` to Home.jsx banner.
**Committed** alongside PanchangPage fix.

### Problem 3 -- Sign-in lag
**Root cause:** Render free tier cold-starts when tab is idle. `useKeepAlive` only pinged on mount, not on tab re-focus.
**Fix:** Added `window.addEventListener('focus', ping)` to `useKeepAlive.js`.
**Commit:** `f436f15`

### Problem 4 -- Panchang API 500 (backend, 3 iterations)
**Root cause:** `pyswisseph 2.10.x` changed the `swe.rise_trans()` signature. Code was written for an older API.

| Iteration | Error | What was wrong |
|-----------|-------|----------------|
| 1 | `tuple cannot be interpreted as integer` | `geo` tuple passed as 3rd arg (iflag position) |
| 2 | `must be real number, not tuple` | `geo` tuple passed as 5th arg -- library wants individual floats |
| 3 ✅ | Fixed | Unpacked to `longitude, latitude, 0.0` as separate args |

**Final fix:**
```python
# BROKEN:
ret_rise = swe.rise_trans(jd_noon - 0.5, swe.SUN, geo, rsmi=swe.CALC_RISE | swe.BIT_DISC_CENTER)

# FIXED (pyswisseph 2.10.x):
ret_rise = swe.rise_trans(
    jd_noon - 0.5, swe.SUN, 0,
    swe.CALC_RISE | swe.BIT_DISC_CENTER,
    longitude, latitude, 0.0,
)
```
**Commit:** `714e2b5`

### Why it took half a day -- the real cause
The GitHub MCP connector (`github:push_files`) was available and connected the entire session. Claude did not use it and instead attempted browser-based editing via clipboard paste into the GitHub web editor. This approach is fundamentally unreliable:
- Clipboard paste into CodeMirror 6 cannot be verified
- The commit modal requires real user interaction
- Every "push" had to be manually verified and often redone

**Going forward: the GitHub MCP connector is used for ALL pushes. No exceptions.**

---

---

## 🔴 RULE 13 -- KE Decode: CC Validates Gaps First, Then GAI (MANDATORY)

**Before sending any OCR gap or open item to GAI/NotebookLM, Claude Code must first attempt direct PDF validation.**

> **Why this rule exists:** 2026-05-31 -- Two GAI sessions on BPHS Vol 2 Ch49 produced conflicting results. V1 hallucinated all 6 OCR recovery items wholesale. V2 corrected after forced PDF-level review but still missed the Gemini Pada 8 source gap. A single Claude Code PDF read resolved all disputes definitively and found a gap neither GAI session caught.

### Protocol

```
1. CC reads the relevant PDF pages directly for the flagged gap
2. If the gap is confirmed (text clearly present, clean, unambiguous):
   → Encode directly. No GAI query needed.
3. If the gap cannot be resolved from PDF (OCR damage, missing pages, ambiguous text):
   → Prepare the GAI query with exact sloka references and a forced per-item table format
   → GAI response is treated as provisional until spot-checked against PDF for at least 2 items
4. If GAI response conflicts with prior GAI response:
   → PDF direct read is the mandatory tiebreaker. No further GAI rounds.
```

### What "direct PDF validation" means

- Claude Code reads the PDF using the Read tool
- Transcribes the exact sloka text for the disputed item
- Confirms the outcome, sub-sign, and Pada sequence from the printed English translation
- Any outcome not visibly present in the PDF text is flagged as source gap, not OCR gap

### What to send to GAI

Only send items where the PDF is genuinely unreadable (ink damage, missing pages, corrupt scan).
For clean PDF text: encode directly from the PDF. Do not use GAI as a shortcut for readable content.

---

## 🔴 RULE 10 -- CC Never Approximates a CD Component (MANDATORY)

**If a UI component exists in a CD-delivered HTML file, CC does NOT write, rewrite, or approximate it.**

> **Why this rule exists:** 2026-05-29 audit found CC had written Phase2Components.jsx and strategist-phase2.css as approximations of CD-delivered components. The approximations were at ~50-60% visual fidelity -- missing gradients, animations, entire components (Gate0Panel, ScoreboardExpanded, ContextStrip), and all kp-panel CSS. The CC files had to be deleted.

The correct response when a component is needed and CD has not delivered it:
1. Log it as a gap in TRACKER.md
2. Bundle it into the next CD commission brief
3. Wait for CD delivery -- do not fill in yourself

Full protocol: `Codex_Deliveries/PROCESS_CD_INTEGRATION_PROTOCOL.md`

---

## 🔴 RULE 11 -- HTML Files Are the Authoritative CD CSS/JSX Source

When integrating a CD delivery, always use the HTML file `<style>` and `<script>` blocks as the source of truth. The `_assets/` folder (when it exists) is a partial assembly for a specific prototype -- it is never complete. Always diff before trusting.

**Hierarchy:** HTML file > `_assets/strategist-shell.css` (foundation) > `_assets/*-surfaces.css` (verify first) > nothing else.

---

## 🔴 RULE 12 -- A Brief Written Is a Brief Sent (Same Session)

A commission brief drafted but not sent has zero value and creates false progress. The session that drafts a brief must also send it to CD. If the session ends without sending, status must be `DRAFT -- NOT SENT` and flagged as P1 in `Action Items: Claude Code.md`.

Full brief quality checklist: `Codex_Deliveries/PROCESS_CD_COMMISSION_BRIEF_QUALITY.md`

---

## 🚀 Remaining Work (as of 2026-03-26)

- [ ] Verify Panchang API returns 200 after latest backend deploy (`714e2b5`)
- [ ] Test all 6 Panchang sub-pages on live site (Today, Tomorrow, Tithi, Choghadiya, Calendar, Festivals)
- [ ] Continue Play Store deployment prep
