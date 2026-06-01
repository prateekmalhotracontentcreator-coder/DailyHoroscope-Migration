# Crystal Healing -- Module Tracker
> Path: `Codex_Deliveries/Crystal_Healing/TRACKER.md`
> Last updated: 2026-05-31 IST · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟡 BLOCKED (L2/L3 fail; L1 borderline) |
| **Backend** | ✅ Delivered + registered in `server.py` |
| **Frontend routes** | ❌ NOT wired in `App.js` (blocked until scan passes) |
| **Mongo seed** | ❌ NOT seeded (blocked until scan passes) |
| **ECHO/PACE scan** | ✅ Run 2026-05-31 (L1 PASS borderline, L2 FAIL, L3 FLAGGED) |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **CRY-1** | Core: 50 crystal pages + 20 intention pages | ✅ DELIVERED + INTEGRATED (backend) | `CODEX_COMMISSION_CRYSTAL_HEALING.md` |
| **CRY-2** | Expansion content | ✅ DELIVERED (pending review) | `CODEX_COMMISSION_CRY_2_EXPANSION.md` |
| **CRY-3** | 5K engine | ✅ DELIVERED (pending review) | `CODEX_COMMISSION_CRY_3_5K_ENGINE.md` |
| **CRY-L2** | L2/L3 fix: FAQ + caution phrase variation; meta title suffix improvement | 🔴 READY TO ISSUE | (brief needed) |

---

## Open Points

| ID | Description | Owner | Status |
|---|---|---|---|
| CRY-OP-1 | Wire App.js routes (crystal profiles + intention pages) | CC | BLOCKED until scan passes |
| CRY-OP-2 | Seed Mongo crystal collections on Render | CC | BLOCKED until scan passes |
| CRY-OP-3 | Issue CRY-L2 commission: vary FAQ + caution phrase templates (5+ variants, hash-selected); improve meta_title suffix variation per crystal | TT/CC | READY |
| CRY-OP-4 | Re-run ECHO/PACE scan after CRY-L2 delivery. L1 must NOT regress past 50% | CC | PENDING CRY-L2 |
| CRY-OP-5 | Run Layer G (Serper) before seeding | CC | PENDING |
| CRY-OP-6 | Review CRY-2 expansion and CRY-3 engine deliveries -- assess if they compound or resolve L2 violations | CC | PENDING |

---

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
| v1.1 | 2026-05-31 | ECHO/PACE scan run. L1 borderline PASS (47.7%), L2/L3 FAIL. Module BLOCKED for seeding. CRY-L2 commission ready. Tracker created. | CC | `ECHO_PACE_SCAN_RUD_CRY_FAITH_2026-05-31.md` |
| v1.0 | 2026-05-25 | CRY-1 delivered + handover doc from Temple Team. Backend registered. CRY-2 + CRY-3 also delivered. | Codex/TT | `TEMPLE_TEAM_HANDOVER_CRY_1_CRY_2_2026-05-25.md` |
