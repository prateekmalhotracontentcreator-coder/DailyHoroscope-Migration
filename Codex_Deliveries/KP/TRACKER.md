# KP Oracle (Krishna Prashnavali) -- Module Tracker
> Path: `Codex_Deliveries/KP/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- live, commissions pending |
| **Frontend** | `frontend/src/pages/KrishnaOraclePage.jsx` |
| **Backend** | `backend/krishna_prashnavali_router.py` |
| **Live URL** | `/krishna-prashnavali` |
| **DB Collections** | `krishna_prashnavali_answers` · `krishna_prashnavali_remedies` · `krishna_prashnavali_history` |
| **Bundle version** | v2 -- `behavioral_remedy` and `remedy_ref` fields populated |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **KP-2A** | Bundle Editorial + Share Card + Remedies Admin Frontend | 🟠 READY TO ISSUE -- M-3 CLEARED | `CODEX_COMMISSION_KP_2A.md` · M-3 passed 2026-05-15. Issue now. |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` · Independent of KP-2A |
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KP_2B.md` · Depends on KP-2A delivered |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~KP-OP-1~~ | ~~**M-3: KP production smoke test**~~ | TT | ✅ DONE | Passed 2026-05-15. Report excellent. Premium gate working. Share card absent (in KP-2A scope). Minor section re-alignment noted (in KP-2A scope). KP-2A unblocked. |
| KP-OP-8 | **Saved Previous Readings not loading** -- history tab/section in KrishnaOraclePage shows no saved readings. Investigate: (a) `GET /api/oracle/krishna-prashnavali/history` endpoint returning correctly? (b) `krishna_prashnavali_history` collection populated? (c) Frontend history render logic wired to correct endpoint and user session? | CC | 🔴 HIGH | Flagged 2026-05-15 during M-3 follow-up. Blocks reading history UX entirely. |
| KP-OP-2 | **`/api/remedies/ref/{remedy_ref_id}` endpoint missing** from `remedies_router.py` | CC | 🔴 HIGH | Claude Code direct fix. One endpoint lookup into `krishna_prashnavali_remedies`. Blocks KP-2A integration. |
| KP-OP-3 | Run `ingest_krishna_prashnavali_remedies_v1.py` on Render if not yet seeded | TT | 🟠 HIGH | Required for `remedy_ref` pipeline to be populated |
| KP-OP-4 | **Issue KP-Sprint2** to Codex (Week 1 -- independent, no dependency) | TT | 🟠 HIGH | `/ask-question` is currently a `ComingSoonPage` stub |
| KP-OP-5 | **Issue KP-2A** to Codex after M-3 smoke test done | TT | 🟠 HIGH | Bundle slot-level editorial + visual share card + Remedies Admin tab |
| KP-OP-6 | **Issue KP-2B** after KP-2A delivered (White Light ritual + 3-pillar Guidance Report + Astro-Filter) | TT | 🟡 MED | Depends on KP-2A |
| KP-OP-7 | `krishna_answer` ≠ slot title audit (KP-G13) -- slot-level editorial verify | TT | 🟡 MED | Flagged in KP-2A brief. Treat as Phase 2 if not addressed in KP-2A. |

---

## Architecture Notes

- KP Oracle is **Gate 0** of The Strategist -- users must complete KP before accessing Strategist diagnostics
- `/api/remedies/ref/{remedy_ref_id}` is a Claude Code direct fix -- do NOT commission Codex for this single endpoint
- KP-2B depends on KP-2A being delivered -- do not issue KP-2B until KP-2A Codex delivery is received and integrated

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-14 | KP-2A, KP-Sprint2, KP-2B briefs written. Module fully live (v2 bundle). | CC | `KP/` folder |
| v1.1 | 2026-05-15 | KP-OP-2 identified (`/remedies/ref/` endpoint missing). Tracker created. | CC | This session |
| v1.2 | 2026-05-15 | M-3 smoke test cleared (KP-OP-1 closed). KP-2A unblocked. Smoke test findings added to KP-2A brief context. | TT | M-3 2026-05-15 |
| v1.3 | 2026-05-15 | KP-OP-8 added: Saved Previous Readings not loading in KrishnaOraclePage. CC to investigate history endpoint + collection + frontend wiring. | TT | Flagged post-M-3 |
