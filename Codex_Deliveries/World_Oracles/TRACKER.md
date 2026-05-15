# World Oracles -- Module Tracker
> Path: `Codex_Deliveries/World_Oracles/TRACKER.md`
> Update this file at the end of every session that touches this module.
> Last updated: 2026-05-15 · v1.0

---

## Current Status

| Field | Value |
|---|---|
| **Status** | 🟣 PLANNED -- Phase 3 · do NOT issue yet |
| **Frontend** | None -- KP Oracle is the only built oracle |
| **Live URL** | None |
| **Phase** | Phase 3A: Bible + Fal-nama + I Ching · Phase 3B: Greek + Sikh |

---

## Five Modules Planned

| Module | Route | Sacred Tradition | Phase |
|---|---|---|---|
| The Promise Box | `/bible-oracle` | Christian Bible | 3A |
| Fal-nama | `/falnama-oracle` | Islamic Fal-nama | 3A |
| I Ching | `/i-ching` | Taoist | 3A |
| Oracle of Delphi | `/oracle-of-delphi` | Greek | 3B |
| Hukamnama | `/hukamnama` | Sikh | 3B |

---

## Commission Status

| ID | Commission | Status | Brief |
|---|---|---|---|
| **ORACLE-P3** | Multi-Scriptural World Oracles (all 5 modules + Guna-Meter) | 🟣 READY TO ISSUE -- ⚠️ Phase 3 only | `CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` |

---

## Open Points

| # | Item | Owner | Priority | Notes |
|---|---|---|---|---|
| ORC-OP-1 | **Do NOT issue ORACLE-P3** until KP-2A + KP-2B + KP-Sprint2 all integrated and KP Oracle live 30+ days | TT | 🔴 GATE | Same grid mechanic as KP -- must prove KP stable first |
| ORC-OP-2 | **Content packs must be prepared by Temple Team** before Codex can build | TT | 🟠 HIGH | Bible verses (selection + attribution) · Fal-nama passages · I Ching hexagrams (64 + interpretations) -- prepare during Phase 2 |
| ORC-OP-3 | Guna-Meter (Tamas/Rajas/Sattva progress bar) reads `user_action_logs` from Punya Rewards + remedy completion | BOTH | 🟡 MED | Part of ORACLE-P3 brief. Design confirmed. |
| ORC-OP-4 | Phase 3A budget/timeline must be confirmed before brief issuance | TT | 🟡 MED | Large scope -- 3 full oracle modules × (grid + content pack + ritual animation + audio) |

---

## Architecture Notes

- Shared OracleFramework backend pattern: `GET /api/{oracle-slug}/meta` · `POST /api/{oracle-slug}/select` · `GET /api/{oracle-slug}/history`
- Same 18×18 grid mechanic as KP Oracle -- reuse interaction model
- Audio identity: each oracle has distinct ambient soundscape (no shared audio)
- Phase 3A before Phase 3B -- do not build all 5 simultaneously

---

## Version History

| Version | Date | What Changed | By | Ref |
|---|---|---|---|---|
| v1.0 | 2026-05-15 | ORACLE-P3 brief written. 5-module spec documented. Phase 3 planning doc. Tracker created. | CC | `CODEX_COMMISSION_ORACLE_P3_WORLD_ORACLES.md` |
