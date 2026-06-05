# Vedic Calculator -- Module Tracker
> Path: `Codex_Deliveries/Vedic_Calculator/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-06-04 · v1.1

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟢 ACTIVE -- Vimshottari ✅ LIVE · Kalachakra ✅ LOCAL DELIVERY 2026-06-04 · Chara ✅ LOCAL DELIVERY 2026-06-04 |
| **File** | `backend/vedic_calculator.py` |
| **Architecture rule** | SINGLE SOURCE OF TRUTH for all live astronomical + dasha computations. No dasha logic in `knowledge_engine.py`. |
| **Active dasha engines** | Vimshottari (live) · Kalachakra (built, awaiting deploy) · Chara (built, awaiting deploy) |
| **Dasha functions** | `calculate_vimshottari_dasha` · `build_dasha_timeline` · `get_current_dasha` · `calculate_kalachakra_dasha` · `build_kalachakra_timeline` · `get_current_kalachakra_dasha` · `chara_duration` · `calculate_chara_dasha_durations` · `calculate_chara_dasha` · `build_chara_timeline` · `get_current_chara_dasha` |
| **Test file** | `backend/tests/test_dasha_engines.py` -- 16 tests |
| **ENGINE_VERSION** | `panchang-router-v22-vc1-kal-chara` |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **VC-1** | Kalachakra + Chara Dasa Engines | ✅ DELIVERED -- CC DIRECT 2026-06-04 | `CODEX_COMMISSION_DASHA_ENGINES_KAL_CHARA.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| VC-OP-01 | Deploy to Render + verify `kalachakra_dasha` / `chara_dasha` keys in live `/api/birth-chart` response | TT | 🟠 HIGH | Local delivery complete. Push to Render triggers ~3 min rolling deploy. No breaking changes -- new keys added alongside existing `dashas`. |
| VC-OP-02 | Verify KALACHAKRA_PERIODS against BPHS Ch.46 PDF by manual inspection | TT | 🟡 MEDIUM | Taurus=16 confirmed by sloka text. OCR of Ch.46 table was too corrupted to read reliably. All other values from classical commentaries. If any values differ from PDF, update `KALACHAKRA_PERIODS` dict in `vedic_calculator.py`. |
| VC-OP-03 | KE engine: wire `build_kalachakra_timeline()` + `build_chara_timeline()` into `scan_chart()` to activate 227 rules | CC | 🟠 HIGH | 154 Kalachakra + 73 Chara rules currently in MongoDB `auto_approved`/`pending_human_review` status. Will activate once KE calls these engines. |
| VC-OP-04 | Brihat Kundali + Strategist: expose Kalachakra / Chara dasha sections in UI | TT + CC | 🟡 MEDIUM | New dasha keys now available in chart payload. UI work is separate from engine delivery. |

---

## Architecture Notes (Permanent)

- **Return format:** Both new engines return identical structure to `build_dasha_timeline()`: `[{sign, planet, start, end, years, antardashas: [{sign, planet, start, end}]}]`.  `planet` field = `SIGN_LORDS[sign]` (standard lord) in ALL cases -- NOT the Chara substitute lord.
- **Chara substitute lords** (`CHARA_SIGN_LORDS`): Rahu for Aquarius, Ketu for Scorpio -- used ONLY for duration calculation and antardasha start determination, never for the `planet` output field.
- **Kalachakra direction:** Savya (forward) for Moon in Aries-Virgo navamsa; Apasavya (backward) for Libra-Pisces navamsa.
- **Mortality flag:** `mortality_flag: True` tags any Kalachakra dasha sign that is the 8th house from Lagna. Tag only -- dates unchanged.
- **Deep debilitation veto:** `deep_debilitation_veto: True` tags any Chara maha where the maha lord is within ±1° of its exact debilitation degree. Requires `planet_degree_map` to be passed; returns `None` otherwise.
- **Ashtakvarga veto:** `ashtakvarga_veto: None` on all Chara entries -- set by KE pipeline (cannot compute without Ashtakvarga scores).
- **Coverage:** Both engines generate ~150 years from birth date.
- **No knowledge_engine imports:** `vedic_calculator.py` must never import `knowledge_engine.py`.

---

## Version History

| Version | Date | What Changed | By |
|---|---|---|---|
| v1.0 | (pre-2026-05-17) | Vimshottari Dasha: `calculate_vimshottari_dasha`, `build_dasha_timeline`, `get_current_dasha`. Full birth chart via `calculate_vedic_chart()`. | CC + Codex |
| v1.1 | 2026-06-04 | **VC-1 DELIVERED -- KALACHAKRA + CHARA ENGINES.** Added `KALACHAKRA_PERIODS` (12-sign Savya/Apasavya periods, 91yr total) · `KALACHAKRA_SAVYA_SIGNS` / `KALACHAKRA_APASAVYA_SIGNS` · `calculate_kalachakra_dasha()` · `build_kalachakra_timeline()` · `get_current_kalachakra_dasha()` · `CHARA_RAHU_FOR_AQ` · `SIGN_MODALITY` · `CHARA_SIGN_LORDS` · `chara_duration()` · `calculate_chara_dasha_durations()` · `calculate_chara_dasha()` · `build_chara_timeline()` · `get_current_chara_dasha()` · `_DISPLAY_TO_PLAIN` · `_DEBILITATION_DEGREES` · `_chara_deep_debi_veto()`. `calculate_vedic_chart()` extended: `kalachakra_dasha` + `chara_dasha` keys added to chart output. Test file `backend/tests/test_dasha_engines.py`: 16/16 tests green. ENGINE_VERSION bumped to `panchang-router-v22-vc1-kal-chara`. All 8 acceptance gates from commission brief pass. Unlocks 154 Kalachakra + 73 Chara KE rules already in MongoDB. | CC |
