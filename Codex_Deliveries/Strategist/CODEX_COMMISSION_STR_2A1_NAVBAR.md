# Codex Commission -- STR-2A1: NavBar Update

> Module: The Strategist
> Spec ref: §P2.5
> Depends on: None -- issue immediately
> Stack: React 18 + Tailwind
> Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Issued: 2026-05-26

---

## What Needs to Change

The global site NavBar currently does not include a link to The Strategist module. Per spec §P2.5:
1. Add **"The Strategist"** as a nav link in the main navigation
2. Move **Blog** and **Career** links from the main nav to the footer nav
3. The Strategist link should route to `/strategist`

---

## Files to Modify

Locate the main NavBar component -- likely one of:
- `frontend/src/components/Navbar.jsx`
- `frontend/src/components/Navigation.jsx`
- `frontend/src/components/Header.jsx`

Find the file that renders the top-level navigation links and make the following changes:

### Change 1 -- Add Strategist link
Add to the main nav link list:
```jsx
<NavLink to="/strategist">The Strategist</NavLink>
```
Place it as a top-level item -- after the existing premium feature links (Birth Chart, Tarot, etc.) and before any utility links.

### Change 2 -- Move Blog + Career to footer
- Remove Blog and Career links from the main nav
- Add them to the footer nav component (locate the Footer component in the same component folder)

### Styling
Follow the existing nav link style exactly -- same font, same active state, same hover treatment. Do NOT introduce new CSS. The Strategist link should use the same Tailwind classes as adjacent nav items.

---

## What You Must NOT Touch

| File | Rule |
|---|---|
| Any Strategist page or component | DO NOT modify |
| `App.js` routing | DO NOT modify routes -- `/strategist` route already exists |
| Any backend file | DO NOT touch |

---

## Acceptance Checklist

- [ ] "The Strategist" appears in main nav and routes to `/strategist`
- [ ] Blog and Career links no longer appear in main nav
- [ ] Blog and Career links appear in the footer nav
- [ ] Active state on The Strategist link works correctly
- [ ] Mobile nav (hamburger menu if present) also reflects these changes
- [ ] Build: `CI=true DISABLE_ESLINT_PLUGIN=true npx craco build` → 0 errors
