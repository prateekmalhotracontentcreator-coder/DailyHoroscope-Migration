# Account 2 -- Session Start Brief
# EverydayHoroscope: Live App
> Last updated: 2026-05-14 (late evening) | Supersedes all prior versions

---

## Project

EverydayHoroscope (everydayhoroscope.in) -- India's Vedic astrology platform.
- Backend: FastAPI on Render (Docker) → `backend/server.py`
- Frontend: React on Vercel → `frontend/src/`
- DB: MongoDB (Motor async) -- env var `MONGO_URL`, db `horoscope_db`
- Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`

Read `CLAUDE.md` first -- single source of truth for architecture, env vars, commit format.
Full session detail: `.claude/HANDOVER_2026-05-14.md`

---

## What Is Live (as of 2026-05-14)

| Module | Status | Notes |
|---|---|---|
| Panchang | ✅ Live | 318 cities, 81 countries |
| Daily / Weekly / Monthly Horoscope | ✅ Live | Weekly + Monthly = Premium |
| Tarot | ✅ Live | 78-card deck, spreads, history |
| Numerology | ✅ Live | 10+ report types |
| Birth Chart / Kundali Milan / Brihat Kundli | ✅ Live | Premium |
| Lagna Kundali (full workspace) | ✅ Live | Premium |
| LK Standalone (Onboard / Report / Tracker / Browse) | ✅ Live | |
| All 5 Remedy Modules (Dana / Gemstones / Crystal / Chakra / Mantra) | ✅ Live | |
| The Strategist | ✅ Live | `/the-strategist` (public) + `/strategist` (smart auth) |
| KP Oracle (`/krishna-prashnavali`) | ✅ Live | Bundle-native remedies |
| Lumina | ✅ Live | 9-tab layout |
| Palmistry (Hasta Rekha) | ✅ Live | AI-powered |
| Arc Angel | ✅ Live | Premium gated |
| Longevity | ✅ Live | KP system, kp_engine.py |
| Admin Console | ✅ Live | Subscribers, email, scheduler, social media |
| Premium / Free tier | ✅ Live | 16+ routes behind PremiumRoute |
| On-page SEO -- all 13 modules | ✅ Live | |
| Smart-quote pre-commit hook | ✅ Live | Auto-sanitises staged files |
| Legal pages | ✅ Live | /terms /privacy /subscription-terms /refund-policy /cookie-policy -- MongoDB seeded |
| /the-tarot public SEO landing | ✅ Live | Dark-themed, FAQ JSON-LD, auth-aware CTA |
| /the-longevity-report public SEO landing | ✅ Live | Green-themed, FAQ JSON-LD, auth-aware CTA |
| /premium-reports public SEO landing | ✅ Live | 5-report tiles, blurred teaser, FAQ JSON-LD |
| Tarot v4 | ✅ Live | Journal tab, XP/streak gamification, moon phase badge, ritual notes |

---

## Premium Access Tier (locked -- do not change without user confirmation)

| Module | Logged Out | Free | Premium |
|---|---|---|---|
| Daily Horoscope / Panchang / Gemstones / Blog | Full | Full | Full |
| Weekly & Monthly Horoscope | Login → | Upgrade → | ✅ Full |
| Tarot / Numerology / Palmistry / Lumina / KP / Strategist | SEO landing | Upgrade → | ✅ Full |
| Lagna Kundali / Birth Chart / Kundali Milan / Brihat Kundli | Login → | Upgrade → | ✅ Full |
| All Reports / Ritual Engine / Arc Angel | Login → | Upgrade → | ✅ Full |

**Gate pattern:**
```jsx
// Route-level (App.js):
<Route path="/..." element={<PremiumRoute feature="..." description="..."><Page /></PremiumRoute>} />

// Inline (auth-aware pages):
if (user && !user.is_premium) return <PremiumGateCard feature="..." description="..." />;
```

`user.is_premium` from `/api/auth/me` → `auth_utils.py` → queries `db.subscriptions`.

---

## Pending -- Next Session

### KP Remedy Engine Fallback (pending from 2026-05-13, parked)
Backend (`scriptural_oracle_router.py`): Reinstate conditional `_resolve_kp_remedy_doc` -- call only when `answer.behavioral_remedy` is None/empty AND `answer.remedy_ref` exists. Bundle first, Engine fills gaps only.

### Open Commissions (priority order)
1. **Individual Reports** -- /premium-reports landing ✅ done; remaining: Web App tool page redesign (`/individual-reports` page -- animated reveals, GlassCard data)
2. **SEO / Technical SEO** -- user to share thread findings
3. **KP Remedy Engine Fallback** -- parked; reinstate when ready
4. **Remedies Engine Phase 1** -- endpoint ✅ ingest ✅; brief at `.claude/briefs/remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md`

### Pending User Decisions
- Lagna Kundali tier -- currently Premium; decision pending
- Punya Rewards route -- built (`/punya-rewards`), no App.js wire yet
- 5 split-required LK rules -- `lalkitab-ch21-fam-04` + 4 others

---

## Mandatory Architecture Rules

1. ALL live astronomical/dasha data from `vedic_calculator.py` + `pyswisseph` -- never replicate
2. `knowledge_rules` always filtered by `science_id`
3. All notifications via `/api/notifications/trigger/{type}` -- never call push/WA directly
4. Remedies Engine downstream-only for KP -- never overrides KP verdict
5. Commit format: `feat(scope):` / `fix(scope):` / `chore(scope):`
6. Bump `ENGINE_VERSION` in `panchang_router.py` before any backend change
7. All fetch calls: `withCredentials: true` / `credentials: 'include'`
8. Never spread `...form` into API payloads when backend uses `extra="forbid"` -- whitelist explicitly
9. FastAPI 422 `detail` is an array -- always guard with `typeof detail === "string"`
10. COPY, never MOVE when integrating Codex -- read Temple file first, paste delta only

**KE ingest freeze active** -- no new chapters until KE Sprint 2 (arbitration runtime) delivered.

---

## Key Spec Files

```
.claude/HANDOVER_2026-05-14.md                          ← LATEST full session summary
.claude/MASTER_DECISIONS_18_MODULE_RECONCILIATION_2026-05-14.md
.claude/briefs/remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md
.claude/briefs/knowledge-engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md
.claude/briefs/lk/LK_STANDALONE_MODULE_SPEC.md
.claude/ke/BOOK_STATUS.md
CLAUDE.md                                               ← architecture, env vars, file map
```
