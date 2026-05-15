# Punya Rewards -- Module Tracker
> Path: `Codex_Deliveries/Punya_Rewards/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | ✅ LIVE -- engine + all earn hooks wired |
| **Backend** | `backend/punya_rewards_router.py` · `backend/punya_rewards_service.py` |
| **DB Collections** | `user_action_logs` |
| **Action codes live** | 9 codes in `DEFAULT_ACTION_RULES` |
| **Frontend hook** | `safeClaimPunyaAction()` -- fire-and-forget, never throws |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| PUN-1 | Punya Rewards Gamification Engine | ✅ INTEGRATED | `CODEX_COMMISSION_PUNYA_REWARDS_GAMIFICATION.md` |

---

## Earn Hooks Wired (7 pages)

| Page | Action Code |
|---|---|
| Daily Horoscope | `daily_horoscope_view` |
| Weekly Horoscope | `weekly_horoscope_view` |
| Monthly Horoscope | `monthly_horoscope_view` |
| Tarot -- Daily Draw | `tarot_daily_draw` |
| Tarot -- Spread Complete | `tarot_spread_complete` |
| Tarot -- Bookmark | `tarot_bookmark` |
| Numerology | `numerology_report_view` |
| Birth Chart | `birth_chart_generate` |
| Panchang | `panchang_daily_view` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| PUN-OP-1 | Arc Angel confidence % reads `user_action_logs` -- +4% per module used, capped at 3 modules | -- | 🟢 NOTE | ARC-2 commission handles this read. No new Punya work needed. |
| PUN-OP-2 | New action codes require backend change to `DEFAULT_ACTION_RULES` -- do not add silently | CC | 🔴 ENFORCE | `safeClaimPunyaAction()` is fire-and-forget -- MUST exist in `DEFAULT_ACTION_RULES` or action is silently ignored |

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-04-25 | PUN-1 integrated. Engine live, 9 action codes, leaderboard/wallet. | Codex + CC | -- |
| v1.1 | 2026-05-15 | Earn hooks wired to 7 pages (9 actions total). `safeClaimPunyaAction()` deployed sitewide. Tracker created. | CC | This session |
