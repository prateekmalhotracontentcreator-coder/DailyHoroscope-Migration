# STRATEGIST_INGEST.md  (The Strategist — lalkitab_strategist)
> Created: 2026-05-11  |  Last updated: 2026-05-13  |  STATUS: ✅ FULLY LIVE — ALL PHASES COMPLETE

---

## Coverage

| Block | IDs | Count | Status |
|---|---|---|---|
| Battlefield Foundation | 701–743 | 43 | ✅ Ingested |
| Sleeping Enemy patch | 744 | 1 | ✅ Patched |
| Siege Operations | 745–951 | 207 | ✅ Ingested |
| Strategic Window Framework | 952–960 | 9 | ✅ Patched |
| Hurdle Library Part 1 | 961–970 | 10 | ✅ Ingested |
| Hurdle Library Part 2 | 971–975 | 5 | ✅ Patched |
| Peak Reach & Expansion | 976–1021 | 46 | ✅ Ingested |
| Success Algorithm | 1022 | 1 | ✅ Patched |
| Final Exit & Archiving | 1023–1025 | 3 | ✅ Ingested |
| Golden Hour UI | 1027 | 1 | ✅ New |
| Universal Surrogates | 651–675 | 25 | ✅ Ingested |
| **Patch v2 batch** | **1011–1020 + 1126–1137** | **22** | ✅ APPROVED & LIVE (2026-05-12) |

**science_id:** `lalkitab_strategist` | **collection:** `knowledge_rules`

---

## Scripts

| Script | Purpose | Status |
|---|---|---|
| `ingest_strategist_v1.py` | Main Strategist ingest (Phase 1) | ✅ Done |
| `ingest_strategist_patch_v2.py` | Patch — 22 records (Digital Warfare 1011–1020 + salvage 1126–1137) | ✅ Run + approved 2026-05-12 |

---

## Application Layer Status

- Phase 1 War Room: **fully live** (StrategistPage, StrategistMissionsPage, StrategistReportPage, StrategistSurrogatePage)
- Backend: `strategist_router.py`, `strategist_engine.py` — live
- Phase 2A–2I: **all live** (KP Gate 0, Pre-Flight banners, Score-gated re-entry, 5-Gate summaries, Scoreboard, Action Plan, 7 notification triggers, PRAY path)
- Premium gating: live — PremiumRoute + PremiumGateCard
- On-page SEO content: live (2026-05-13)

## Pending Items

- **2J — UI Polish**: mobile layout, mission cards, dasha display — listed in spec, not yet built
- **5 split-required LK rules**: `lalkitab-ch21-fam-04` + 4 others — affects rule quality, not blocking
- **Phase 2 Plug-ins (deferred)**: KP Astrology + Numerology plugins — data-driven, no code until data ready

---

## ID Architecture Notes

- Surrogate IDs 651–675 under `science_id: "lalkitab_strategist"` — no collision with `jyotish_lk_remedies` IDs 656–668 (compound upsert key: `{id, science_id}`)
- `remedy_id` cross-references inside surrogate rows point to `jyotish_lk_remedies` — do not change
- IDs 1022 + 1027 are module config objects — exempt from schema validation

---

## Status
Phase 1: ✅ LIVE | Patch v2: ✅ APPROVED & LIVE | Phase 2A–2I: ✅ ALL LIVE | 2J UI Polish: ⏸ NOT YET BUILT
