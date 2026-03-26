# Claude Working Protocol — EverydayHoroscope

> **Last updated:** 2026-03-26  
> **Reason:** Half a day was lost because Claude attempted browser-based GitHub edits instead of using the GitHub MCP connector that was available all along. This document exists so that never happens again.

---

## 🔴 RULE 1 — Fix Before Moving Forward

**Never skip a failing fix and move to the next task.**

If a fix is partially done or uncertain, STOP and resolve it fully before touching anything else. A half-fixed bug compounds into a full-day debugging session. This is not optional.

- If a Vercel build fails → fix the syntax error FIRST, then continue
- If a Render API returns 500 → fix the backend FIRST, then test frontend
- If a commit didn't go through → verify it landed FIRST, then proceed

---

## 🔴 RULE 2 — Always Use the GitHub MCP Connector for Pushes

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
- The GitHub editor uses CodeMirror 6 with a virtualised DOM — `innerText` only returns visible lines, so you cannot verify what was actually pasted
- The clipboard API requires document focus, which is unreliable in automated browser sessions
- The commit modal is triggered by a React event that doesn't always fire from programmatic clicks
- **There is no reliable way to verify the correct content was committed via browser automation**

---

## 🔴 RULE 3 — Always Get the File SHA Before Updating

When using `github:create_or_update_file`, the SHA of the existing file is required. Always fetch it first:

```
github:get_file_contents → returns content + SHA
then use that SHA in github:create_or_update_file
```

Missing the SHA causes a 422 conflict error and the push silently fails.

---

## 🟡 RULE 4 — Verify Every Commit Landed

After every push, confirm the commit SHA appears on GitHub before moving on:

```
github:get_commit(sha='main') → check latest commit message and files changed
```

Or check the live API endpoint directly to confirm the fix is working.

---

## 🟡 RULE 5 — Check Render Logs Before Guessing at the Fix

When a backend API returns 500, always read the Render logs first. Do not guess.

- Navigate to https://dashboard.render.com → service → Logs
- Read the full Python traceback — it gives the exact file, line number, and error
- Fix exactly what the log says, nothing more

The Panchang `rise_trans` bug required 3 iterations because the error message was read incorrectly the first time. The log told us exactly what was wrong from the start.

---

## 🟡 RULE 6 — Test the API Directly Before Calling It Fixed

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
5. Verify:                 github:get_commit(sha='main') — confirm commit landed
6. Test live:              Hit the actual URL to confirm it works
```

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

### Problem 1 — Panchang pages blank (frontend)
**Root cause:** NavBar sent users to `/panchang/today`, `/panchang/tithi`, `/panchang/choghadiya` but `PanchangPage.jsx` only handled `daily`, `calendar`, `festivals`. No ALIAS map existed.
**Fix:** Replaced `PanchangPage.jsx` with full version including ALIAS map and 6 views.
**Commit:** `53f6f48`

### Problem 2 — Email overflow on Home page
**Root cause:** Email `<p>` tag had no `truncate` class; flex container had no `min-w-0`.
**Fix:** Added `truncate break-all` to email `<p>` in `UserAccountMenu.jsx`; added `min-w-0` to Home.jsx banner.
**Committed** alongside PanchangPage fix.

### Problem 3 — Sign-in lag
**Root cause:** Render free tier cold-starts when tab is idle. `useKeepAlive` only pinged on mount, not on tab re-focus.
**Fix:** Added `window.addEventListener('focus', ping)` to `useKeepAlive.js`.
**Commit:** `f436f15`

### Problem 4 — Panchang API 500 (backend, 3 iterations)
**Root cause:** `pyswisseph 2.10.x` changed the `swe.rise_trans()` signature. Code was written for an older API.

| Iteration | Error | What was wrong |
|-----------|-------|----------------|
| 1 | `tuple cannot be interpreted as integer` | `geo` tuple passed as 3rd arg (iflag position) |
| 2 | `must be real number, not tuple` | `geo` tuple passed as 5th arg — library wants individual floats |
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

### Why it took half a day — the real cause
The GitHub MCP connector (`github:push_files`) was available and connected the entire session. Claude did not use it and instead attempted browser-based editing via clipboard paste into the GitHub web editor. This approach is fundamentally unreliable:
- Clipboard paste into CodeMirror 6 cannot be verified
- The commit modal requires real user interaction
- Every "push" had to be manually verified and often redone

**Going forward: the GitHub MCP connector is used for ALL pushes. No exceptions.**

---

## 🚀 Remaining Work (as of 2026-03-26)

- [ ] Verify Panchang API returns 200 after latest backend deploy (`714e2b5`)
- [ ] Test all 6 Panchang sub-pages on live site (Today, Tomorrow, Tithi, Choghadiya, Calendar, Festivals)
- [ ] Continue Play Store deployment prep
