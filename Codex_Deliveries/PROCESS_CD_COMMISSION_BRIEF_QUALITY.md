# Process: CD Commission Brief Quality Gates
> Status: **ACTIVE** -- Issued 2026-05-29
> Issued by: Temple Team / CC Audit Session
> Applies to: Every commission issued to Claude Design (CD)

---

## Why This Document Exists

The 2026-05-29 audit of Strategist Phase 2 identified the following commission brief failures:

1. **STR-2EF brief was written but never sent to CD** -- TRACKER said "BRIEF READY -- NOT YET SENT" for weeks while CC tried to build the components itself
2. **`_assets/` folder was not included in briefs** -- CD had no way to know what had already been extracted vs what was missing
3. **Commission scope was not file-specific enough** -- the brief did not specify which HTML file governs which component
4. **No acceptance test in briefs** -- no way to verify delivery completeness
5. **No diff protocol specified** -- CC had no instruction to diff against HTML files before integrating

---

## 🔴 RULE 1 -- A Brief Written Is a Brief Sent (Same Session)

**A commission brief that is drafted but not sent has zero value.** Writing a brief creates a false sense of progress.

Rule: **The same session that drafts a brief must also send it to CD.** If the session ends without sending, the brief status must be `DRAFT -- NOT SENT` in the TRACKER, and it must appear as a `P1 CRITICAL` action item in `Action Items: Claude Code.md`.

---

## 🔴 RULE 2 -- Every Brief Must Reference the CD Delivery Folder

Every CD commission brief must include a section called **"CD Delivery Folder"** that specifies:
```
Canonical delivery folder: /Users/apple/Documents/Knowledge Engine_eBooks/[module]/
Reference HTML files (authoritative source):
  - [filename].html → governs [component name]
  - ...
_assets/ folder contents (if exists): [list files + note if partial]
```

This ensures CD knows exactly where prior work lives and what the integration target is.

---

## 🔴 RULE 3 -- Every Brief Must Include an Acceptance Test

Every CD commission brief must include a section called **"Acceptance Criteria"** with:

```
1. CSS: All classes listed in [HTML file] <style> block are present in the delivered CSS file
2. JSX: All functions listed in [HTML file] <script> block are present as ES exports
3. Variants: All A/B toggle states render correctly in isolation
4. No new :root tokens introduced without explicit approval from Temple Team
5. Delivered files pass the 6-step conversion recipe (PROCESS_CD_INTEGRATION_PROTOCOL.md §4)
```

---

## 🔴 RULE 4 -- Specify Which HTML File Is Authoritative for Each Component

When commissioning a new or updated component, the brief must state:

```
Source of truth: [path to CD HTML file]
CSS to extract: Lines [N] to [M] of <style> block
JSX to extract: Lines [N] to [M] of <script type="text/babel"> block
Functions expected in delivery: [list function names]
```

This prevents CD from building from memory rather than from the signed-off canvas.

---

## 🔴 RULE 5 -- Scope Gaps Before Briefing, Not After

Before writing a brief for any Phase 2+ work:

```
[ ] 1. Run the pre-integration checklist (PROCESS_CD_INTEGRATION_PROTOCOL.md §7)
[ ] 2. Identify all components in the HTML files
[ ] 3. Identify all components missing from _assets/ 
[ ] 4. List every missing component in the brief as "Known Gap -- CD to deliver"
[ ] 5. List every canvas-only component (proof sets, demo scaffolding) as "Not required in production"
```

---

## 🔴 RULE 6 -- Never CC-Approximate While Waiting for CD

If a CD delivery is pending or a gap is identified:

```
❌ WRONG: CC writes its own version of the component while waiting
✅ RIGHT: CC logs the gap in TRACKER.md, marks it as "PENDING CD", continues with other work
```

CC approximations introduce two problems:
1. They diverge from CD's visual standard (proven: ~50% fidelity gap)
2. They must be deleted when CD delivers, wasting the session

---

## The Commission Brief Template

Every brief sent to CD must contain these sections in order:

```markdown
# CD Commission -- [Component Name]
> Module: [module name]
> Issued: [date]
> Depends on: [list prior commissions that must be integrated first]

## 1. Context
[2-3 sentences on what this component does in the live app]

## 2. CD Delivery Folder
Canonical folder: [path]
Reference HTML (authoritative): [filename + what it governs]
_assets/ status: [complete / partial / none]

## 3. What to Build
[Specific component names, variants, modes]
[Explicit: "Retain all existing A/B variants from [HTML file]"]

## 4. What NOT to Build
[List canvas-only components not needed in production]
[List components already integrated from prior commissions]

## 5. Live API Contract
[Field names from live API that replace SEEKER demo stub]
[Reference: PROCESS_CD_INTEGRATION_PROTOCOL.md §5]

## 6. Delivery Format
- One .jsx file per component (ES module format, named exports)
- One .css file per component (or appended to existing phase CSS)
- No Object.assign(window, ...) -- use export { ... }
- No window.SEEKER references -- all data via props

## 7. Acceptance Criteria
[List per RULE 3 above]

## 8. Known Gaps for This Commission
[List any components from HTML files missing from _assets/]
```

---

## Brief Quality Checklist (Run Before Sending)

```
[ ] Brief references the canonical CD delivery folder
[ ] Brief names the authoritative HTML file for each component
[ ] Brief lists all expected JSX function names
[ ] Brief lists what NOT to build (canvas scaffolding, proof sets)
[ ] Brief includes the live API field map
[ ] Brief specifies ES module delivery format (no window.assign)
[ ] Brief has explicit acceptance criteria
[ ] Known gaps are listed
[ ] Brief is being sent in this same session (not deferred)
[ ] TRACKER.md will be updated to IN PROGRESS after sending
```
