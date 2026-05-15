# Codex Deliveries -- Master Commission Index

> EverydayHoroscope · Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Last updated: 2026-05-15
>
> **Rule:** Every commission issued to Codex gets a row here and a file in the relevant module folder.
> Temple Team creates the Codex folder + adds this row before issuing each commission.

---

## How to use this folder

```
Codex_Deliveries/
├── INDEX.md                          ← this file -- master tracker
├── [Module]/
│   ├── CODEX_COMMISSION_[ID].md      ← active brief (latest version)
│   └── _archive/                     ← superseded drafts / older versions
```

- **Active brief** = the file Codex reads. One per commission.
- **_archive/** = previous drafts, reconciled specs, earlier briefs -- kept for reference.
- **Version control** = filename carries date suffix only when archiving: `_v2026-05-14.md`

---

## Commission Registry

| ID | Module | Commission | Brief file | Status | Issued | Depends on |
|---|---|---|---|---|---|---|
| KE-Contract | Knowledge Engine | Master KE Architecture Contract | `Knowledge_Engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` | LOCKED -- reference doc | 2026-04-10 | -- |
| KE-2A | Knowledge Engine | Yoga Check Evaluation Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | READY TO ISSUE | 2026-05-15 | -- |
| KP-2A | KP Oracle | Bundle Editorial + Share Card + Remedies Admin Frontend | `KP/CODEX_COMMISSION_KP_2A.md` | READY TO ISSUE | 2026-05-14 | -- |
| KP-2B | KP Oracle | Ritual Animation + 3-Pillar UX + Astro-Filter | `KP/CODEX_COMMISSION_KP_2B.md` | READY TO ISSUE | 2026-05-14 | KP-2A complete |
| KP-Sprint2 | KP Oracle | /ask-question LLM Logic Router | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | READY TO ISSUE | 2026-05-14 | -- |
| IR-1 | Individual Reports | 5 Public SEO Landing Pages | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | READY TO ISSUE | 2026-05-14 | -- |
| REM-P1 | Remedies | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | READY TO ISSUE | 2026-05-14 | -- |
| TAR-v4 | Tarot | Tarot UI v4 Enhancement | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | READY TO ISSUE | 2026-04-30 | -- |
| KUN-1 | Kundali | Lagna Kundali Module Contract | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | READY TO ISSUE | 2026-04-10 | -- |
| LK-1 | Lal Kitab | LK Standalone Module | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | READY TO ISSUE | 2026-05-09 | -- |
| LON-1 | Longevity | Ayur Jyotish Longevity Report | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | READY TO ISSUE | 2026-04-10 | -- |
| PAN-L1 | Panchang | Language/Regional Pages | `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` | READY TO ISSUE | 2026-04-30 | -- |
| SEO-1 | SEO | SEO + Marketing + Web Performance | `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` | READY TO ISSUE | 2026-04-30 | -- |

---

## Status Key

| Status | Meaning |
|---|---|
| `READY TO ISSUE` | Brief is complete. Temple Team opens Codex thread and shares brief. |
| `IN PROGRESS` | Commission opened in Codex. Awaiting delivery. |
| `DELIVERED -- PENDING INTEGRATION` | Codex output received. Claude Code to review + integrate. |
| `INTEGRATED` | Code integrated, built, committed to `main`. |
| `LOCKED -- reference doc` | Architecture/contract doc -- not a commission, used as Codex reading material. |

---

## Archive Policy

When a commission is superseded by a newer version:
1. Rename old file with date suffix: `CODEX_COMMISSION_X_v2026-05-11.md`
2. Move to `[Module]/_archive/`
3. Update this INDEX row to point to the new active file

---

## Module folders

| Folder | Module | Description |
|---|---|---|
| `KP/` | Krishna Prashnavali Oracle | 18×18 grid oracle, /ask-question, ritual UX, share card |
| `Knowledge_Engine/` | Jyotish Knowledge Engine | Rules library, yoga evaluator, narrative engine, Library Console |
| `Individual_Reports/` | Individual Reports | Karmic Debt, Career Blueprint, Shadow Self, Retrograde, Life Cycles |
| `Remedies/` | Remedies Engine | KP remedies collection, LK remedies, remedy_ref pipeline |
| `Tarot/` | Tarot | Daily draw, spreads, history, share card |
| `Kundali/` | Kundali / Birth Chart | Lagna chart, Brihat Kundali, BirthChartPage |
| `LK/` | Lal Kitab | LK onboard, remedies, debt audit, tracker |
| `Longevity/` | Longevity Report | Ayur Jyotish longevity analysis |
| `Panchang/` | Panchang | Language pages, multilingual SEO |
| `SEO/` | SEO & Web Performance | Technical SEO, Core Web Vitals, sitemap, meta |
