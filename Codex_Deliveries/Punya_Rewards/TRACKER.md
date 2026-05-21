# Punya Rewards -- Module Tracker
> Path: `Codex_Deliveries/Punya_Rewards/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 · v1.2

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ✅ LIVE -- engine + core earn hooks wired; PUN-2 frontend uplift in progress |
| **Backend** | `backend/punya_rewards_router.py` · `backend/punya_rewards_service.py` |
| **DB Collections** | `user_action_logs` |
| **Action codes live** | 9 codes in `DEFAULT_ACTION_RULES` |
| **Frontend hook** | `safeClaimPunyaAction()` -- fire-and-forget, never throws |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| PUN-1 | Punya Rewards Gamification Engine | ✅ INTEGRATED | `CODEX_COMMISSION_PUNYA_REWARDS_GAMIFICATION.md` |
| PUN-2 | Punya Rewards Home Promo + Module Hooks + SVG Wheel | 🟡 IN PROGRESS | `CODEX_COMMISSION_PUN_2_FRONTEND_INTEGRATION.md` |

---

## Earn Hooks Wired (7 pages)

| Page | Action Code |
|---|---|
| Daily Horoscope | `horoscope_daily_view` |
| Weekly Horoscope | `horoscope_weekly_view` |
| Monthly Horoscope | `horoscope_monthly_view` |
| Tarot -- Daily Draw | `tarot_daily_draw` |
| Tarot -- Spread Complete | `tarot_spread_complete` |
| Tarot -- Bookmark | `tarot_bookmark` |
| Numerology | `numerology_report_generate` |
| Birth Chart | `birth_chart_generate` |
| Panchang | `panchang_daily_view` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| PUN-OP-1 | Arc Angel confidence % reads `user_action_logs` -- +4% per module used, capped at 3 modules | -- | 🟢 NOTE | ARC-2 commission handles this read. No new Punya work needed. |
| PUN-OP-2 | New action codes require backend change to `DEFAULT_ACTION_RULES` -- do not add silently | CC | 🔴 ENFORCE | `safeClaimPunyaAction()` is fire-and-forget -- MUST exist in `DEFAULT_ACTION_RULES` or action is silently ignored |
| PUN-OP-3 | PUN-2 brief asks for `individual_report`, but backend `DEFAULT_ACTION_RULES` does not define that action code | CC | 🟠 OPEN | Do not wire the Individual Reports trigger until Temple either adds a backend rule or confirms a different live action code. |

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-25 | PUN-1 integrated. Engine live, 9 action codes, leaderboard/wallet. | Codex + CC | -- |
| v1.1 | 2026-05-15 | Earn hooks wired to 7 pages (9 actions total). `safeClaimPunyaAction()` deployed sitewide. Tracker created. | CC | This session |
| v1.2 | 2026-05-22 | PUN-2 started: added landing-page promo section, mirrored PUN-2 brief into module-home docs, upgraded `/punya-rewards` wheel UX with SVG/countdown/grouped ledger, and corrected tracker hook labels to match live backend action codes. | Codex | This session |
