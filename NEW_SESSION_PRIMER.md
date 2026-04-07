# New Session Primer — EverydayHoroscope
> Read this first. Takes 60 seconds. Gets you fully oriented.

---

## Who You Are Working With

**Prateek Malhotra** — Founder, EverydayHoroscope.
- Non-technical product owner with strong vision
- Reviews all code before integration
- Manages Codex commissions separately (see Codex section below)
- Prefers concise responses, no filler, no trailing summaries

---

## The Product

**EverydayHoroscope** — India's premium Vedic astrology platform.
- Live at: https://www.everydayhoroscope.in
- Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
- Stack: React (Vercel) + FastAPI (Render/Docker) + MongoDB + pyswisseph
- Internal name: **"Temple App"** — a spiritual companion platform

**For full module status, file locations, and API routes → read `CLAUDE.md`**
**For current backlog and Codex commission queue → read `PROJECT_STATUS.md`**

---

## How Codex Fits Into Our Workflow

### What is Codex?
Codex is a separate AI coding tool (OpenAI) that Prateek uses to generate new feature code in parallel. Think of it as an offline contractor that writes code to spec.

### Critical: Codex Does NOT Have GitHub Access
- Codex cannot push to the repo
- Codex cannot see live code or existing files
- Codex generates standalone code files/components in isolation
- Prateek receives the Codex output and brings it here for integration

### The Integration Workflow
```
1. Claude Code (this session) → drafts Codex Commission Brief
   (spec: what to build, inputs/outputs, style guide, file names)

2. Prateek → submits brief to Codex → receives generated code

3. Prateek → pastes Codex output into this chat

4. Claude Code → reviews, adapts, integrates into Temple App
   (wires routes, fixes imports, aligns with existing theme,
    fixes any build errors, commits to main)
```

### What "Integration" Means
When Codex code arrives, Claude Code must:
- Align styles to Temple App theme (CSS vars: `--background`, `--card`, `--gold`, `--foreground`)
- Wire React Router routes in `App.js`
- Register FastAPI routers in `backend/main.py`
- Fix any curly/smart quote characters that break Babel (common Codex issue)
- Run `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` to verify build
- Commit with proper format: `feat(scope): description`

---

## Theme System (Temple App)

All components must use these CSS variables — never hardcode colors:

| Token | Usage |
|---|---|
| `bg-background` | Page background (dark: `hsl(20 25% 5%)`) |
| `bg-card` | Card/panel surface |
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary/caption text |
| `text-gold` / `border-gold` | Accent color (`#c5a059`) |
| `bg-gold` | Gold fill (active tabs, CTAs) |

**GlassCard pattern:**
```jsx
<div className="rounded-xl border border-gold/20 bg-gold/[0.04] shadow-sm">
```

**Gold tile gradient (illuminating effect):**
```jsx
className="bg-gradient-to-br from-gold/15 to-gold/5"
```

---

## Build Rules

```bash
# Always test build before pushing:
cd frontend && CI=true DISABLE_ESLINT_PLUGIN=true npx craco build

# Common build killers:
# 1. Smart/curly quotes in JS strings (copy-paste from Codex/Word)
#    Fix: node -e "let f=require('fs');let c=f.readFileSync('file.jsx','utf8');
#         c=c.replace(/\u201c/g,'"').replace(/\u201d/g,'"')
#          .replace(/\u2018/g,\"'\").replace(/\u2019/g,\"'\");
#         f.writeFileSync('file.jsx',c)"
#
# 2. react-hooks/exhaustive-deps warnings → become errors under CI=true
#    Fix: add all referenced vars to useEffect deps arrays
```

---

## Session Hygiene

- One session = one focused task or module (prevents context bloat)
- When first compacting message appears → wrap up, commit, start fresh
- Always start session with: read CLAUDE.md + PROJECT_STATUS.md + git log --oneline -10
- Commit format: `feat(scope):` / `fix(scope):` / `chore(scope):` / `docs:`
- Never use GitHub browser editor — always commit via terminal or Claude Code

---

## Current Priority Queue

See `PROJECT_STATUS.md` → Codex Commission Queue section for full list.

**Top 3 immediate:**
1. Commission A — Lumina gold/illuminating theme pass
2. Commission B — Palm anatomy SVG static asset (high-quality illustrated)
3. Commission G — 2 new strategic modules (Prateek to brief)

---

## How to Start Working

After reading this file:
1. Read `CLAUDE.md` (full technical reference)
2. Read `PROJECT_STATUS.md` (current state + backlog)
3. Run `git log --oneline -10` (see recent commits)
4. Ask Prateek: "What are we working on today?"
