# Crystal Healing -- Module Tracker
> Path: `Codex_Deliveries/Crystal_Healing/TRACKER.md`
> Last updated: 2026-06-04 IST · v1.2

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 ACTIVE -- CRY-L2 PASS, routes wired. TT to seed Mongo + run Layer G Serper. |
| **Backend** | ✅ Delivered + registered in `server.py` |
| **Frontend routes** | ✅ Wired in `App.js` 2026-06-04 -- 7 routes: hub, crystal, intention, planet, sign, problem, calculator |
| **Mongo seed** | 🟡 PENDING -- TT to run seed scripts on Render |
| **ECHO/PACE scan** | ✅ CRY-L2 PASS 2026-06-04 -- Crystal L1 49.5%, Intention L1 45.4%, L2 0, L3 0 |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **CRY-1** | Core: 50 crystal pages + 20 intention pages | ✅ DELIVERED + INTEGRATED (backend) | `CODEX_COMMISSION_CRYSTAL_HEALING.md` |
| **CRY-2** | Expansion content | ✅ DELIVERED (pending review) | `CODEX_COMMISSION_CRY_2_EXPANSION.md` |
| **CRY-3** | 5K engine | ✅ DELIVERED (pending review) | `CODEX_COMMISSION_CRY_3_5K_ENGINE.md` |
| **CRY-L2** | L2/L3 fix: tightened variant distribution, diversified labels/titles, tag-based healing-property fragments | ✅ INTEGRATED 2026-06-04 | `crystal_data.py` |

---

## Open Points

| ID | Description | Owner | Status |
|---|---|---|---|
| ~~CRY-OP-1~~ | ~~Wire App.js routes (crystal profiles + intention pages)~~ | ~~CC~~ | ✅ CLOSED 2026-06-04 | 7 routes wired: `/crystals`, `/crystals/:crystalSlug`, `/crystals/calculator`, `/crystals/for/:intentionSlug`, `/crystals/for/planet/:planet`, `/crystals/for/sign/:sign`, `/crystals/for/problem/:problem`. Frontend build clean. |
| CRY-OP-2 | Seed Mongo crystal collections on Render | TT | 🟠 HIGH -- next action | Run seed scripts on Render shell after Layer G clears. |
| ~~CRY-OP-3~~ | ~~Issue CRY-L2 commission~~ | ~~TT/CC~~ | ✅ CLOSED 2026-06-04 | CRY-L2 delivered and integrated. |
| ~~CRY-OP-4~~ | ~~Re-run ECHO/PACE scan after CRY-L2~~ | ~~CC~~ | ✅ CLOSED 2026-06-04 | Crystal 49.5% PASS, Intention 45.4% PASS. L2 0, L3 0. No regression. |
| CRY-OP-5 | Run Layer G Serper before seeding | TT | 🟠 HIGH -- gates seed | Build script + run: `Serper_Default_key=KEY python3 tests/echo_pace_cry_serper_detail.py` (script to build) |
| CRY-OP-6 | Review CRY-2 + CRY-3 deliveries -- assess if they compound or resolve violations | CC | 🟡 MED -- after Layer G | Do not integrate until base module fully signed off |

---

## ECHO/PACE Results

### CRY-L2 -- 2026-06-04 (verified by CC independent run)

| Page Type | Pages | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|---|
| CRYSTAL | 50 | 49.5% ✅ | 0 violations ✅ | 0 pairs ✅ | PASS |
| INTENTION | 20 | 45.4% ✅ | 0 violations ✅ | 0 pairs ✅ | PASS |

**Fixes applied in CRY-L2:** Tightened deterministic variant distribution, diversified cleansing-method labels and crystal titles, expanded short FAQ branches, converted healing-property copy into concise tag-based fragments to eliminate repeated 4-grams without pushing L1 over the gate.

**L1 Watch note:** Crystal pages at 49.5% are 0.5% below the 50% FLAGGED gate. CRY-2 and CRY-3 content must be ECHO/PACE tested before integration to ensure L1 does not regress.

### Baseline -- 2026-05-31 (pre-CRY-L2)

| Page Type | Pages | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|---|
| CRYSTAL | 50 | 47.7% ✅⚠️ | FAIL ❌ | FLAGGED ⚠️ | Borderline |
| INTENTION | 20 | 20.8% ✅ | FAIL ❌ | FLAGGED ⚠️ | Needs fix |

## ECHO/PACE Results (2026-05-31)

Full report: `Codex_Deliveries/ECHO_PACE/ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md`

| Page Type | Pages | L1 | L2 | L3 | Verdict |
|---|---|---|---|---|---|
| CRYSTAL | 50 | 47.7% ✅⚠️ | FAIL ❌ | FLAGGED ⚠️ | Borderline -- do not regress |
| INTENTION | 20 | 20.8% ✅ | FAIL ❌ | FLAGGED ⚠️ | Needs fix |

**L1 WARNING**: Crystal pages at 47.7% are 2.3% below the FLAGGED gate. Any future content addition that increases structural similarity could push this to FLAGGED. Must monitor.

**L2 root cause**: `_build_faq()` and caution/cleansing structural copy share fixed-phrase boilerplate appearing in 100% of pages. Examples: "option stone soft porous" (water caution caveat), "spiritual balancing simple cleansing".

**L3 root cause**: Meta title suffix `"| EverydayHoroscope"` and fixed descriptor `"Crystal - Healing Properties, Chakra & Uses"` adds shared tail that inflates Jaccard for similar-named crystals (e.g., "Garnet" vs "Hessonite Garnet" at 88%).

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.2 | 2026-06-04 | CRY-L2 integrated. ECHO/PACE PASS: Crystal 49.5% L1, Intention 45.4% L1, L2 0, L3 0. App.js routes wired (7 routes). Build clean. CRY-OP-1/3/4 closed. CRY-OP-5 (Layer G Serper) is next gate before seed. | CC | `frontend/src/App.js` |
| v1.1 | 2026-05-31 | ECHO/PACE scan run. L1 borderline PASS (47.7%), L2/L3 FAIL. Module BLOCKED for seeding. CRY-L2 commission ready. Tracker created. | CC | `ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md` |
| v1.0 | 2026-05-25 | CRY-1 delivered + handover doc from Temple Team. Backend registered. CRY-2 + CRY-3 also delivered. | Codex/TT | `TEMPLE_TEAM_HANDOVER_CRY_1_CRY_2_2026-05-25.md` |
