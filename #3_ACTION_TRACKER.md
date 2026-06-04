# Action Items -- Temple App
> Single Source of Truth for all open items across Claude Code sessions.
> Referenced in all handover docs. **Do not create parallel lists elsewhere.**
> Last updated: 2026-06-04 (Angel Numbers: M-19 closed -- ANGEL-3 seeded, both collections live. Copyright test PASS documented. Layer G Serper script built -- ANGEL-OP-7 is now sole remaining gate for TT.)

---

## Owner: Me (Prateek) -- Action Required

These items are blocked on my input or approval. Nothing can proceed until actioned.

| # | Item | Why Blocked | Priority |
|---|---|---|---|
| ~~M-1~~ | ~~OG image replaced~~ | -- | ✅ DONE -- replaced 2026-05-20, <82KB 1200×630 |
| ~~M-2~~ | ~~Legal pages compliance refresh~~ | -- | ✅ DONE -- seed run 2026-05-20, 5 policies updated in production |
| ~~M-3~~ | ~~**KP production smoke test**~~ -- ✅ **CLEARED 2026-05-15.** Report excellent. Premium gate confirmed working. Two findings fed into KP-2A scope: (a) section box re-alignment needed, (b) share card + download not yet present in module -- both in KP-2A brief. KP-2A now unblocked. | ~~Blocks KP-2A integration~~ | ✅ DONE |
| ~~M-4~~ | ~~**Strategist 22 records approval sign-off**~~ -- ✅ **CLEARED 2026-05-15.** All 22 records (IDs 1011-1020 + 1126-1137) confirmed ingested and live. `strategist_engine.py` does not filter on `approval_status` -- pending_human_review has zero functional effect. STR-1 is unblocked. | ~~Blocks STR-1 integration~~ | ✅ DONE |
| M-5 | **WhatsApp** -- complete OTP verification for +91 96431 10001 in WhatsApp Manager + add payment method to WABA on Meta | WhatsApp notifications blocked | 🟡 MED |
| M-6 | **Instagram Business Account ID** -- not loading in Meta dashboard. Resolve to enable Instagram posting from Admin Console | Instagram posting blocked | 🟡 MED |
| M-7 | **react-snap vs helmet-async** -- design decision on pre-render strategy. Await SEO-1 thread findings before deciding | SEO-1 thread will recommend | 🟢 LOW |
| M-8 | **Service worker** -- decide if PWA offline caching is in scope. Await SEO-1 thread | SEO-1 thread scope | 🟢 LOW |
| M-9 | **App.js lazy audit** -- confirm: keep Landing + DailyHoroscope + Login eager, lazy-load the rest? | Minor perf gain; not blocking | 🟢 LOW |
| M-10 | **MODULE_ARC_ANGEL doc audit** -- only 3 files present post-cleanup. Verify whether additional docs (specs, QA notes, handoff notes, source maps) should be migrated from `Codex_Deliveries/Arc_Angel/` into the module home. | Reconciliation gap found 2026-05-15 | 🟢 LOW |
| M-11 | **MODULE_LAL_KITAB doc audit** -- only 3 files present post-cleanup (created 2026-05-15). Verify whether additional docs should migrate from `Codex_Deliveries/LK/` into the module home. | Reconciliation gap found 2026-05-15 | 🟢 LOW |
| M-12 | **MODULE_SEO_WEB_PERFORMANCE doc audit** -- only 3 files present post-cleanup (created 2026-05-15). Verify whether additional docs should migrate from `Codex_Deliveries/SEO/` into the module home. | Reconciliation gap found 2026-05-15 | 🟢 LOW |
| M-13 | **Live TV console polish (LTV-OP-1)** -- player console bar on `/live-sai-baba-arti` functional but visual design does not match original spec intent. Raise as Codex commission when final design is confirmed. | Design decision needed from TT | 🟡 MED |
| ~~M-15~~ | ~~**TAR-SEO-1 integration**~~ -- ✅ **DONE.** TAR-SEO-1 integrated `8f36fc8`. TAR-SEO-2 QA-CLEARED `cc52900`. 199 pages live. ECHO/PACE strict full pass (L1-L3 + Layer G 15/15 PASS 0% dup). | ✅ DONE | ✅ |
| ~~M-16~~ | ~~**LSG-2 integration**~~ -- ✅ **DONE 2026-05-30.** All 7 route patterns live and smoke-tested. MongoDB seeded (responses confirmed live DB data). 66-URL sitemap active. LSG-OP-3 ✅ passed. LSG-OP-2 ✅ seeded. | ✅ DONE | ✅ |
| M-17 | **KE-OP-15** -- Verify KE questionnaire live endpoints on Render: `/questionnaire`, `/api/knowledge-engine/questionnaire/profile`, `/api/knowledge-engine/questionnaire/submit`; confirm `user_questionnaire_profiles` writes in MongoDB | KE-IQ integration sign-off pending | 🟠 HIGH |
| M-18 | **LON-OP-2** -- Longevity preview API at `/api/longevity/generate` takes ~46s. Profile + optimise to bring under 10s contract target | Performance gap flagged in QA audit | 🟠 HIGH |
| ~~M-19~~ | ~~**ANGEL-OP-1** -- Re-seed Angel Numbers Mongo collections with ANGEL-3 content~~ | ✅ DONE 2026-06-04 | `angel_number_core` (1,000 modified) + `angel_number_intents` (9,000 modified) seeded on Render with ANGEL-3 content. API smoke test passed. |
| M-20 | **ECHO-UI-1** -- Deploy ECHO/PACE admin frontend: `EchoPaceTab.jsx` + `AdminDashboard.jsx` changes not in current production bundle | ECHO/PACE admin unreachable in production | 🟠 HIGH |
| M-21 | **SHC-UI-1** -- Verify Self-Healing Center "Self-Heal" tab live in Admin Console. `DiagnosticsTab.jsx` IS imported (line 25) + rendered (line 742) in `AdminDashboard.jsx` with 4 SHC strings confirmed -- QA audit finding was stale. TT to confirm tab visible at `/admin/dashboard` on current Vercel deploy. | Confirm tab visible in production; no code change needed | 🟡 MED |
| M-22 | **SHC-OPS-1** -- Configure 5 Render env vars for Gmail/GST: `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `SUPPORT_EMAIL`, `BUSINESS_STATE`, then run Gmail OAuth flow | GST + Gmail scheduler jobs blocked | 🟠 HIGH |
| ~~M-23~~ | ~~**KE-DEDUP-CONTRADICTION-1**~~ -- ✅ **DONE 2026-05-29.** `backend/ke_dedup_script.py` delivered. TF-IDF similarity + contradiction detection + idempotent write-back. 1/1 tests pass. `scikit-learn>=1.3.0` added to `requirements.txt`. | ✅ DONE | ✅ |
| M-24 | **Phaladeepika NLM** -- Begin Adhyaya II decode. Brief at `KE_TEXTBOOK_DECODE/Thread_Briefs/THREAD_BRIEF_PHALADEEPIKA_NLM.md` | Fully unblocked -- no dependency | 🟡 MED |
| M-25 | **BPHS Vol 1 Thread A** -- Confirm Q1 (Ch11-Ch24 completeness) and Q2 (folder: `BPHS_CC_Decode/` canonical), then continue with Karaka → Yoga → Dasha chapters | Brief at `KE_TEXTBOOK_DECODE/Thread_Briefs/` | 🟡 MED |
| M-26 | **KP Astrology claim_axis pass** -- Retroactive self-audit of all 77 files to populate `claim_axis: "longevity"` on ~20 rules across ~15 files | Near-complete close-out action | 🟡 MED |
| M-27 | **LTV-SCOPE-1** -- Remove `LiveTVPanel` mounts from non-home pages (`Home.jsx`, `PanchangLandingPage.jsx`, `PanchangPage.jsx`). Re-test `/`, `/home`, Panchang routes. | Scope drift from original "home page only" spec | 🟠 HIGH |
| ~~M-28~~ | ~~**KP-Sprint2 delivery review**~~ -- ✅ **DONE 2026-05-29.** Both KP-Sprint2 (`20d4d29`) + KP-2B (`20f7b83`) INTEGRATED. KP-OP-12 + KP-OP-13 TT production verify pending (passed to Operations thread). | ✅ DONE | ✅ |
| M-29 | **LK-OP-8 -- TT acceptance verify on production** -- Verify `/lal-kitab-remedies` loads, onboard flow works, diagnose returns 5 gates, debt audit functions, tracker persists, browse shows 361 records. LK module was fully built by A2 session -- this is acceptance only. | Strategist/LK thread to own | 🟠 HIGH |
| M-30 | **LK-OP-5 -- Premium PDF download not built** -- LK-1 brief included `FirstName+BirthYear+Month` password-protected PDF. Not implemented in A2 build. Raise as separate Codex commission after LK-OP-8 acceptance. | After LK-OP-8 passes | 🟡 MED |
| M-31 | **LK-OP-6 -- 5 split-required LK rules** -- `lalkitab-ch21-fam-04` + 4 age/infancy rules tagged `split_required=True`. NLM to review and provide splits. | NLM to action | 🟡 MED |
| M-32 | **LK-OP-7 -- 96 in-range master doc records not salvaged** -- Unique master doc IDs not in V2. Review: if worthwhile, add as suffix IDs (800A, 800B, etc.) per agreed protocol. | TT decision needed | 🟡 MED |
| M-33 | **SEO Sprint E -- `/horoscope/daily/:sign` NEVER BUILT** -- 12 sign-specific horoscope pages are the highest-volume astrology search queries in India. Identified in A2 session end-state but never tracked. Scope and issue as SEO commission before SEO-1 thread. | Major SEO gap -- no code exists | 🟠 HIGH |
| M-34 | **SEO Sprint D -- Organization + WebSite JSON-LD on Landing page** -- Structured data not yet added to root landing page. Identified in A2 session. | Low-lift SEO win | 🟡 MED |
| M-35 | **KE Phase 1 Ingest -- 300 Combinations (UNBLOCKED)** -- Start immediately. Handover at `ThreeHundredCombinations_CC_Decode/HANDOVER_SUMMARY.md`. No OCR issues. New KE Ingest Thread to run ingest script. | KE Ingest Thread | 🔴 HIGH |
| M-36 | **TT decisions required before ingest** -- ~~(a) 300 Horoscopes: 3 blocked rules (h300-s01-016, h300-s04-004, h300-s04-005)~~ -- ✅ ALL 3 CLEARED by CC PDF validation 2026-05-31. (b) SBC: 7 blocking priority conflicts from 40-question batch -- review and resolve. ~~(c) Longevity Unnatural: lu-s04-001 ("must" vs "should") + lu-s04-014 (AND vs OR)~~ -- ✅ BOTH CLEARED by CC PDF validation 2026-05-31. lu-s04-001: "should" confirmed (p.9), weighted condition not hard gate. lu-s04-014: 06 AND Mars required; maraka OR badhaka either sufficient (p.9). All 5 HIGH OCR items resolved -- LU Unnatural READY for ingest. ~~(d) BPHS Vol 1 doctrinal ambiguities~~ -- ✅ ALL 10 HIGH items resolved by GAI 2026-05-30. | TT to resolve (b) only | 🟠 HIGH |
| ~~M-37~~ | ~~**Aayu bucket methodology co-founder sign-off**~~ -- ✅ **DONE 2026-06-02.** Option B approved: label-based tagging + 66-75 edge gate. Longevity 58Ch ingest complete: 149 rules (batch `longevity_58ch_v1`). DB total: 10,620. | ~~TT (co-founder)~~ | ✅ DONE |
| M-38 | **BPHS Vol 2 Ch49 -- Gemini Pada 8 source gap (TT decision)** -- Gemini Pada 8 is absent from the Santhanam translation (Slokas 11-12). Confirmed by Claude Code direct PDF read 2026-05-31 -- not an OCR failure. The surrounding text is clean. Two options: (a) Accept the gap -- encode as `active: false, source_gap: true`, cap Ch49 at 107 of 108 Navamsa Pada rules permanently. (b) Cross-check against an alternate BPHS translation (Girish Chand Sharma or Rangacharya) to see if Pada 8 is documented there. TT to decide approach before ingest thread begins Ch49 encode. | TT decision | 🟡 MED |
| ~~M-14~~ | ~~**Render Free → Starter upgrade**~~ -- ✅ **DONE 2026-05-17.** Render now on Starter plan ($7/mo). Server always-on, no more cold starts. API responds in ms for first user of each session. SEO crawlers now get instant 200 responses. | ~~Cold starts hurting UX + SEO~~ | ✅ DONE |

---

## Codex Commission Status

> **Single source of truth for all commissions → `Codex_Deliveries/[Module]/TRACKER.md`**
> Do not duplicate commission status here. Open a module TRACKER to see what is integrated, in progress, or ready to issue for that module.
> Commission queue with issue-order priority → `Codex_Deliveries/List_of_Pending_Codex_Commissions.md`

---

## Done by Claude Code -- No Commission Needed

Small direct fixes completed in-session. No Codex thread required.

| Item | Status | Commit |
|---|---|---|
| Punya Rewards earn hooks -- 7 pages (Daily/Weekly/Monthly Horoscope, Tarot, Numerology, BirthChart, Panchang) | ✅ Done | This session |
| Arc Angel `isPremium` -- already correct (`user?.is_premium ?? false`) | ✅ Confirmed -- was a false alarm | -- |
| Punya Rewards + Live TV router registration in server.py | ✅ Confirmed -- already wired | -- |
| `ArcAngelPanel.jsx` API amendments (subscription, birth data source, birth_place param) | ✅ Done | `c01ec8d` |

### Still to do (Claude Code direct -- small, no commission)
- ~~🔧 **`/api/remedies/ref/{remedy_ref_id}` endpoint**~~ -- ✅ Already present at `remedies_router.py` line 827. Confirmed live 2026-05-15. Was a false alarm.
- ~~🔧 **KP Saved Previous Readings not loading** (KP-OP-8)~~ -- ✅ Fixed commit `80238a5`. Broken `window.scrollTo({top:0})` in `loadPastReading` was scrolling user away from the Guidance Report before React rendered it. Replaced with `useRef` + `useEffect` scroll-into-view.

---

## Phase 2 / Phase 3 Parking Lot -- Not Yet Actioned

Items confirmed deferred. Not in any active commission. Will be picked up in future planning sessions.

| Item | Phase | Priority | Thread |
|---|---|---|---|
| Commission J -- World Context Engine (macro α signals: conflict zones, festivals, exam periods) | Phase 2 | 🟢 LOW | KE / Commission J |
| ~~Arc Angel: persist `user_arc_angel_profile` in MongoDB (currently stateless)~~ | ✅ DONE 2026-05-17 | KE-Sprint3 built the full persistence layer -- schema, upsert, 6h cache, GET route. No longer parking lot. |
| TD-26 Country Kundali as Alpha Signal | Phase 2 | 🟡 MED | KE |
| TD-27 Forecast Tier / Life Area Outlook | Phase 2 | 🟡 MED | KE |
| KP-G7 Audio soundscapes (binaural + Sanskrit chanting) | Phase 3 | 🟢 LOW | KP |
| KP-G8 Spiritual Journal UX (beyond reading history) | Phase 3 | 🟢 LOW | KP |
| KP-G9 Panchapakshi bird state timing layer in KP | Phase 3 | 🟢 LOW | KP |
| KP-G12 Guna-Meter gamification (Tamas/Rajas/Sattva progress bar) | Phase 3 | 🟢 LOW | KP / ORACLE-P3 |
| KP-G13 krishna_answer ≠ title audit (slot-level editorial verify) | Phase 2 | 🟡 MED | KP-2A (flagged) |
| KP 20-category onboarding expansion (currently 5 categories) | Phase 2 | 🟡 MED | KP |
| Slot 33 → LK Debt Audit cross-module trigger (PRAY verdict → surfaces Debt Audit) | Phase 2 | 🟡 MED | KP / LK |
| Lumina v2 tab-by-tab audit before changes | Phase 2 | 🟡 MED | -- |
| Razorpay live keys | When Play Store ready | 🟡 MED | -- |
| Scheduled daily social posts (6 AM auto-post to FB + YT) | Phase 2 | 🟢 LOW | Notifications |
