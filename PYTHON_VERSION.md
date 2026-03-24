# Python Version Policy — EverydayHoroscope Backend

## Locked Version: Python 3.11

The backend is permanently pinned to Python 3.11 until further notice.

## Why

`flatlib` (our Vedic astrology calculation library) depends on `pyswisseph`,
a C extension that uses `PyUnicode_AS_DATA`. This internal Python C API was
removed in Python 3.12. Attempting to build on 3.12 produces:

```
error: implicit declaration of function 'PyUnicode_AS_DATA'
```

This breaks the Docker build on Render and affects every module that uses
astronomy calculations:

- Birth Chart
- Kundali Milan
- Brihat Kundli Pro
- Panchang

## What this means for Codex and external builders

All module code delivered to the Temple App must be **Python 3.11 compatible**.

Using `from __future__ import annotations` at the top of every file
backports modern union syntax (`str | None`, `dict[str, Any]`) to 3.11.
This is already the pattern in all delivered Codex modules.

**Do not target Python 3.12 for local validation environments.**
Use `brew install python@3.11` and `python3.11 -m venv .venv`.

## When will this change?

When `flatlib` or a replacement astronomy library ships a verified
Python 3.12-compatible build. That is a tracked future task.

Python 3.11 is supported by the Python core team until **October 2027**.
There is no urgency to change.

## Files that enforce this

| File | Version pinned |
|------|---------------|
| `backend/Dockerfile` | `FROM python:3.11-slim` |
| `backend/runtime.txt` | `3.11.0` |
| `backend/requirements.txt` | `flatlib==0.2.3` (triggers pyswisseph) |

## Change process

Any proposal to change Python version requires:

1. Confirmation that `flatlib` or a replacement builds cleanly on the target version
2. A successful local Docker build test
3. Sign-off before the Dockerfile is touched

This document is the single source of truth. Refer to it in all Codex conversations.
