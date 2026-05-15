# KP Oracle (Krishna Prashnavali) -- Module Tracker
> Path: `Codex_Deliveries/KP/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.5

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- KP-2A INTEGRATED (`7d42880`) · KP-Sprint2 IN PROGRESS · KP-2B ready to issue after TT live verification |
| **Frontend** | `frontend/src/pages/kp/KrishnaOraclePage.jsx` |
| **Backend** | `backend/scriptural_oracle_router.py` · `backend/remedies_router.py` |
| **Live URL** | `/krishna-prashnavali` |
| **DB Collections** | `krishna_prashnavali_answers` · `krishna_prashnavali_remedies` · `krishna_prashnavali_history` |
| **Bundle version** | v2 -- `content_status = fully_authored_v2` · all 36 slots `temple_approved_v2` · slot 33 has `cross_module_trigger` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **KP-2A** | Bundle Editorial + Share Card + Remedies Admin Frontend | ✅ INTEGRATED -- commit `7d42880` | `CODEX_COMMISSION_KP_2A.md` · Delivered + integrated 2026-05-15. TT live verification pending. |
| **KP-Sprint2** | /ask-question LLM Logic Router (Guna + Gita) | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` · Independent of KP-2A |
| **KP-2B** | Ritual Animation + 3-Pillar UX + Astro-Filter | 🟣 READY TO ISSUE | `CODEX_COMMISSION_KP_2B.md` · Depends on KP-2A delivered |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~KP-OP-1~~ | ~~**M-3: KP production smoke test**~~ | TT | ✅ DONE | Passed 2026-05-15. Report excellent. Premium gate working. Share card absent (in KP-2A scope). Minor section re-alignment noted (in KP-2A scope). KP-2A unblocked. |
| ~~KP-OP-8~~ | ~~**Saved Previous Readings not loading**~~ | CC | ✅ DONE | Root cause: `loadPastReading` called `window.scrollTo({top:0})` before React re-rendered the Guidance Report into the DOM -- user was scrolled to page top while the report appeared silently below the grid. Fix: removed broken scrollTo, added `guidanceRef` + `useEffect` scroll-into-view that fires after render. Commit `80238a5` 2026-05-15. |
| ~~KP-OP-2~~ | ~~**`/api/remedies/ref/{remedy_ref_id}` endpoint missing**~~ | CC | ✅ CONFIRMED PRESENT | Endpoint exists at `remedies_router.py` line 827. Prefix `/api/remedies`, registered in `server.py`. `{"_id": 0}` projection already in place. Was a false alarm -- confirmed live 2026-05-15. |
| ~~KP-OP-3~~ | ~~Run `ingest_krishna_prashnavali_remedies_v1.py` on Render~~  | TT | ✅ DONE | Run 2026-05-15. upserted=0, modified=36 -- collection was already seeded; all 36 records refreshed with current bundle. `remedy_ref` pipeline confirmed populated. |
| ~~KP-OP-4~~ | ~~**Issue KP-Sprint2** to Codex~~ | TT | ✅ DONE | KP-Sprint2 issued 2026-05-15. |
| ~~KP-OP-5~~ | ~~**Issue KP-2A** to Codex~~  | TT | ✅ DONE | Issued 2026-05-15. Delivered + integrated same day at commit `7d42880`. |
| KP-OP-6 | **Issue KP-2B** after TT live verification of KP-2A | TT | 🟠 HIGH | KP-2A integrated. TT to verify share card (WhatsApp/Facebook/Save/Copy), bundle slots 11/19/31/33, remedies admin PATCH. Issue KP-2B once satisfied. |
| KP-OP-9 | **TT live verification of KP-2A** | TT | 🟠 HIGH | Verify: (1) Share card renders + 4-button share works; (2) Bundle slots 11/19/31/33 content correct; (3) Remedies Admin Panel -- search, filters, inline status patch. Blocker for KP-2B. |
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
| v1.3 | 2026-05-15 | KP-OP-8 added: Saved Previous Readings not loading. KP-OP-2 confirmed present (false alarm). KP-OP-3 remedies seeded (36 records). | TT + CC | Flagged post-M-3 |
| v1.4 | 2026-05-15 | KP-OP-8 fixed (two commits): (1) scroll bug -- `guidanceRef` + `useEffect` replacing broken `window.scrollTo` (`80238a5`); (2) MongoDB `_id` ValidationError on `/reports/{report_id}` -- added `{"_id": 0}` projection (`302f24e`). KP-2A brief reviewed and updated with CC changes. All CC open points closed. KP-2A ready to issue. | CC | `80238a5`, `302f24e` |
| v1.5 | 2026-05-15 | KP-2A delivered by Codex and integrated. Build verified green. Python parse clean. CC fixes (guidanceRef + _id projection) confirmed preserved. KP-OP-5 closed. KP-OP-6 + KP-OP-9 (TT live verification) opened. Commission status → INTEGRATED `7d42880`. | CC | `7d42880` |
