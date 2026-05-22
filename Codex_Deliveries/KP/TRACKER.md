# KP Oracle (Krishna Prashnavali) -- Module Tracker
> Path: `Codex_Deliveries/KP/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-22 · v2.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- KP-2A ✅ · KP-Sprint2 ✅ INTEGRATED `20d4d29` · KP-2B ✅ INTEGRATED `20f7b83` · **TT to verify both on production** · KP-OP-10 (share card) + KP-OP-11 (report UX) open |
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
| ~~**KP-Sprint2**~~ | ~~KP Ask Question -- Guna Logic Router~~ | ✅ INTEGRATED -- commit `20d4d29` | `CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` · `AskQuestionPage.jsx` (514 lines), `ask_question_logic_router.json` (60 routes: 20 SATTVA/RAJAS/TAMAS), ask endpoint in `scriptural_oracle_router.py`. Build clean. TT acceptance checklist pending. |
| ~~**KP-2B**~~ | ~~Ritual Animation + 3-Pillar UX + Astro-Filter~~ | ✅ INTEGRATED -- commit `20f7b83` | `CODEX_COMMISSION_KP_2B.md` · `KrishnaRitualScreen.jsx` (95 lines), 3-pillar `KrishnaOraclePage.jsx` (799 lines), astro enrichment in `scriptural_oracle_router.py`. CC fix: lazy sessionStorage init (no flash). Build clean. TT acceptance checklist pending. |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ~~KP-OP-1~~ | ~~**M-3: KP production smoke test**~~ | TT | ✅ DONE | Passed 2026-05-15. Report excellent. Premium gate working. Share card absent (in KP-2A scope). Minor section re-alignment noted (in KP-2A scope). KP-2A unblocked. |
| ~~KP-OP-8~~ | ~~**Saved Previous Readings not loading**~~ | CC | ✅ DONE | Root cause: `loadPastReading` called `window.scrollTo({top:0})` before React re-rendered the Guidance Report into the DOM -- user was scrolled to page top while the report appeared silently below the grid. Fix: removed broken scrollTo, added `guidanceRef` + `useEffect` scroll-into-view that fires after render. Commit `80238a5` 2026-05-15. |
| ~~KP-OP-2~~ | ~~**`/api/remedies/ref/{remedy_ref_id}` endpoint missing**~~ | CC | ✅ CONFIRMED PRESENT | Endpoint exists at `remedies_router.py` line 827. Prefix `/api/remedies`, registered in `server.py`. `{"_id": 0}` projection already in place. Was a false alarm -- confirmed live 2026-05-15. |
| ~~KP-OP-3~~ | ~~Run `ingest_krishna_prashnavali_remedies_v1.py` on Render~~  | TT | ✅ DONE | Run 2026-05-15. upserted=0, modified=36 -- collection was already seeded; all 36 records refreshed with current bundle. `remedy_ref` pipeline confirmed populated. |
| ~~KP-OP-4~~ | ~~**Issue KP-Sprint2** to Codex~~ | TT | ✅ DONE | KP-Sprint2 issued 2026-05-14. |
| ~~KP-OP-5~~ | ~~**Issue KP-2A** to Codex~~  | TT | ✅ DONE | Issued 2026-05-15. Delivered + integrated same day at commit `7d42880`. |
| ~~KP-OP-6~~ | ~~**Issue KP-2B**~~ | TT | ✅ DONE | KP-2B issued AND integrated same session 2026-05-22. Commit `20f7b83`. |
| KP-OP-12 | **TT acceptance verification -- KP-Sprint2** on production | TT | 🟠 HIGH | Verify: `/ask-question` loads, 20 focus areas render, Guna classification shows (SATTVA/RAJAS/TAMAS), 3-card reveal works, free quota (2/month) enforced, readings persist. |
| KP-OP-13 | **TT acceptance verification -- KP-2B** on production | TT | 🟠 HIGH | Verify: ritual screen fires on first visit, skips on return (sessionStorage), orb animates, "I'm ready" skip works, grid fades in, 3 pillars visible in Guidance Report, Verdict badge colour-coded, Cosmic Context shows Mahadasha+Antardasha when birth data present, "Add birth details" CTA when absent. |
| ~~KP-OP-9~~ | ~~**TT live verification of KP-2A**~~ | CC | ✅ DONE | (1) Share bar ✅ confirmed 2026-05-16; (2) Bundle slots 11 (WAIT) ✅ · 19 (NO/Pratrodha) ✅ · 31 (PRAY/Bhakti) ✅ · 33 (PRAY/Bhakti) ✅ -- all 4 verified via browser 2026-05-22; (3) Remedies Admin PATCH ✅ endpoint live (`PATCH /api/remedies/admin/records/{id}/status` returns 422 with correct schema validation). KP-OP-9 fully cleared. |
| KP-OP-10 | **Share Card visual format** -- needs redesign | TT + CC | 🟠 HIGH | TT noted share card format needs work. Card currently uses `KrishnaShareCard.jsx` (gold dark theme). Full card format + capture review needed. To be addressed in KP-2B scope or as standalone CC fix after TT review. |
| KP-OP-11 | **KP Oracle report structure UX review** | TT + CC | 🟠 HIGH | TT noted the web app report structure needs improvement. Two-column grid layout (`xl:grid-cols-[1.2fr,0.8fr]`) + section arrangement to be reviewed. Likely KP-2B scope. |
| KP-OP-7 | `krishna_answer` ≠ slot title audit (KP-G13) -- slot-level editorial verify | TT | 🟡 MED | Flagged in KP-2A brief. Treat as Phase 2 if not addressed in KP-2A. |

---

## KP-Sprint2 -- Delivery Spec & Acceptance Checklist

> Source: `MODULE_KRISHNA_PRASHANAVALI/KP_SPRINT2_HANDOVER_SUMMARY_2026-05-22.md`
> Status: commissioned 2026-05-14 · IN PROGRESS · not yet delivered

### Runtime targets (when Codex delivers)

| Layer | Target |
|---|---|
| New page | `frontend/src/pages/kp/AskQuestionPage.jsx` |
| Route swap | `frontend/src/App.js:308` -- replace `ComingSoonPage` with `AskQuestionPage` |
| New endpoint | `POST /api/oracle/krishna-prashnavali/ask` in `backend/scriptural_oracle_router.py` |
| Logic router seed | `backend/assets/krishna_oracle/ask_question_logic_router.json` (60 combinations) |
| Persistence | MongoDB collection `ask_question_readings` |
| Dasha source | MUST use `vedic_calculator.py` -- do NOT add dasha logic to `knowledge_engine.py` |

### Locked functional spec

**Frontend flow:** Landing hero → 20 focus-area categories → text input (10-200 chars) → loading state (Diya + rotating text) → 3-card reveal (Verse · Cosmic Context · Practical Action)

**Backend flow:** Classify question into one Guna (SATTVA / RAJAS / TAMAS) → map (focus_area, guna) to seeded Gita verse → enrich with dasha context from `vedic_calculator.py` if birth data present → synthesise Krishna response → persist if authenticated

**Auth / premium rules:**
- Logged out → browse landing/categories only; submit triggers auth prompt
- Free logged-in → 2 free readings per month
- Premium → unlimited readings + full dasha enrichment visible

### Acceptance checklist (CC integration gate -- all 11 must pass)

- [ ] `/ask-question` no longer renders `ComingSoonPage`
- [ ] `AskQuestionPage.jsx` mounted and usable
- [ ] All 20 categories render correctly
- [ ] Question validation enforces 10-200 chars
- [ ] Guna classification runs
- [ ] Logic router JSON contains all 60 combinations
- [ ] Dasha enrichment uses `vedic_calculator.py`
- [ ] Reveal renders 3-card answer layout
- [ ] Readings persist to `ask_question_readings`
- [ ] Free vs premium limits behave correctly
- [ ] Share and save actions work

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
| v1.6 | 2026-05-16 | Share bar confirmed visible by TT (KP-OP-9 item 1 ✅). Share bar moved full-width below reading, matching Panchang/Horoscope pattern (`22ae365`). Copy button now copies full reading text + URL. KP-Sprint2 status corrected to IN PROGRESS, with commission issue date aligned to 2026-05-14 and `/ask-question` still explicitly tracked as a ComingSoon stub pending delivery. KP-OP-10 (share card format) + KP-OP-11 (report structure UX) opened per TT review. | CC + TT | `22ae365` |
| v1.7 | 2026-05-22 | KP-Sprint2 handover summary filed by Codex KP thread (`MODULE_KRISHNA_PRASHANAVALI/KP_SPRINT2_HANDOVER_SUMMARY_2026-05-22.md`). Acceptance checklist (11 items), locked functional spec, and premium/auth rules added to tracker. `/ask-question` confirmed still on ComingSoon stub. ORACLE-P3 dependency on KP-Sprint2 confirmed and recorded. | Codex + CC | handover doc |
| v1.8 | 2026-05-22 | KP-OP-9 fully cleared via browser verification: all 4 bundle slots confirmed live (11/WAIT · 19/NO · 31/PRAY · 33/PRAY), Remedies Admin PATCH endpoint confirmed live (422 schema validation). KP-2B unblocked -- TT to issue. | CC | browser session |
| v1.9 | 2026-05-22 | **Critical bug fixed:** `_source_bundle_path()` had `.parent.parent` causing bundle to never load on Render -- every reading served provisional seed content since launch. Fixed to `.parent`. Frontend remedy display changed from OR to AND -- both `behavioral_remedy` (Behavioural Practice) and `remedy` (Sacred Remedy) now always shown. Commit `0db820b`. | CC | TT report |
| v2.0 | 2026-05-22 | **KP-Sprint2 INTEGRATED.** Codex delivery reviewed and committed (`20d4d29`): `AskQuestionPage.jsx` (514 lines, 20 focus areas, Guna display, 3-card reveal, share/save, free quota), `ask_question_logic_router.json` (60 routes), ask endpoint in `scriptural_oracle_router.py`. Route wired in `App.js`. Build clean. TT acceptance checklist (KP-OP-12) opened. Context update + KP-2B brief sent to KP Oracle Codex thread. | CC | `20d4d29` |
| v2.1 | 2026-05-22 | **KP-2B INTEGRATED.** `KrishnaRitualScreen.jsx` (25s white-orb meditation, sequential text reveals, sessionStorage gate, "I'm ready" skip). `KrishnaOraclePage.jsx` rebuilt with 3-pillar Guidance Report (Sacred Verse · Cosmic Context · Practical Action), VerdictBadge (YES/WAIT/NO/PRAY), OracleGlassCard, staggered fadeInUp animation, Pillar 2 birth-data conditional. CC fix: lazy `useState(() => sessionStorage)` init prevents grid flash on first load. `scriptural_oracle_router.py`: `astro_context`, `current_mahadasha`, `current_antardasha`, `birth_data_present` fields added with Claude enrichment + fallback. Build clean. TT acceptance checklist (KP-OP-13) opened. | CC | `20f7b83` |
