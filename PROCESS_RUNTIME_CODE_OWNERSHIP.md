# Process: Runtime Code Ownership
> Status: **CONFIRMED** -- Temple Team approved 2026-05-15
> Issued by: Audit / PM
> Applies to: All Codex threads + Claude Code sessions

---

## Rule

The doc-cleanup process applies to **module-owned documentation only**. It does **not** require or permit migration of active runtime code.

---

## Working Rule

| Location | What it holds |
|---|---|
| `/Users/apple/Documents/New project/[MODULE_*]/` | Docs, briefs, specs, source maps, QA notes, handoff notes, delivery tracking -- **docs only** |
| `/Users/apple/DailyHoroscope-Migration/backend/` | All active runtime code -- **never move these files** |
| `/Users/apple/Documents/New project/ke_phase2a_worktree/` | Temporary staging worktree -- treat as staging area, not a module home |
| `/Users/apple/DailyHoroscope-Codex-Test/` | Read-only reference-build snapshot -- do not treat as source of truth |

---

## Knowledge Engine Example

Files such as `knowledge_engine.py`, `ke_yoga_evaluator.py`, `knowledge_router.py`, and other live backend runtime files must remain in `/Users/apple/DailyHoroscope-Migration/backend/`.

No migration of these files into `MODULE_KNOWLEDGE_ENGINE/` is required or appropriate.

---

## What Threads Should Still Do

Threads should continue to move module-owned **specs, handoff notes, QA notes, checklists, and source maps** into their Main Codex module-home folders, while leaving runtime code in place.

---

## Summary

```
MOVE TO MODULE HOME:    specs · briefs · handoff notes · QA notes · checklists · source maps
LEAVE IN PLACE:         *.py backend files · *.jsx frontend files · any live runtime code
STAGING ONLY:           ke_phase2a_worktree (not a permanent home)
READ-ONLY REFERENCE:    DailyHoroscope-Codex-Test (do not source from here)
```
