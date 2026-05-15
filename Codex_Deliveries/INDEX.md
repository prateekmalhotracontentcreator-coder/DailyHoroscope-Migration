# Codex Deliveries -- Master Commission Index

> EverydayHoroscope · Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
> Last updated: 2026-05-15
>
> **Rule:** Every commission issued to Codex gets a row here + a file in the relevant module folder.
> Temple Team creates the Codex folder and adds the INDEX row before issuing each commission.

---

## How to use this folder

```
Codex_Deliveries/
├── INDEX.md                          ← this file -- master tracker
├── CODEX_WAYS_OF_WORKING.md          ← governance: how Codex works with Temple Team
├── [Module]/
│   ├── CODEX_COMMISSION_[ID].md      ← active brief (one per commission)
│   └── _archive/                     ← superseded drafts / delivered/integrated versions
```

**Active brief** = the file Codex reads. One file per commission, always latest version.
**_archive/** = older drafts, pre-spec consultations, delivered commissions -- kept for reference.
**Version suffix** = applied only when archiving: `_v2026-05-14.md` or `_delivered.md`.

---

## Status Key

| Status | Meaning |
|---|---|
| `READY TO ISSUE` | Brief complete. Temple Team opens Codex thread + shares this file. |
| `IN PROGRESS` | Commission open in Codex. Awaiting delivery. |
| `DELIVERED -- PENDING INTEGRATION` | Codex output received. Claude Code to review + integrate. |
| `INTEGRATED` | Code built, committed to `main`. Commission closed. |
| `REFERENCE DOC` | Architecture/contract doc -- not a commission, shared as Codex reading material. |

---

## Commission Registry -- All Modules

### Knowledge Engine

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| KE-Contract | Master KE Architecture Contract (TD-01 to TD-30) | `Knowledge_Engine/CODEX_KNOWLEDGE_ENGINE_CONTRACT.md` | REFERENCE DOC | 2026-04-10 |
| KE-CPath1-Order | CPath-1 Build Order (Items 1-8 sequencing) | `Knowledge_Engine/CODEX_KE_CPATH1_BUILD_ORDER.md` | REFERENCE DOC | 2026-04-10 |
| KE-WIM | Paraphrase Workflow Instructions Manual | `Knowledge_Engine/CODEX_PARAPHRASE_WIM.md` | REFERENCE DOC | 2026-04-10 |
| KE-Amendment | Library Amendment Contract Template | `Knowledge_Engine/CODEX_LIBRARY_AMENDMENT_TEMPLATE.md` | REFERENCE DOC | 2026-04-10 |
| KE-Ingest | Batch Book Ingest Automation v2 | `Knowledge_Engine/CODEX_COMMISSION_KE_BATCH_INGEST.md` | INTEGRATED | 2026-04-10 |
| KE-Val | Automated Rule Validation Engine | `Knowledge_Engine/CODEX_COMMISSION_KE_VALIDATION_ENGINE.md` | INTEGRATED | 2026-04-10 |
| KE-Item5 | Library Console (CPath-1 Item 5) | `Knowledge_Engine/_archive/CODEX_KE_ITEM5_LIBRARY_CONSOLE_delivered.md` | INTEGRATED | 2026-04-10 |
| KE-Item6 | Brihat Kundali × KE Route (CPath-1 Item 6) | `Knowledge_Engine/_archive/CODEX_KE_ITEM6_BRIHAT_KUNDALI_KE_delivered.md` | INTEGRATED | 2026-04-10 |
| KE-Item7 | Simplified Tranche Filter (CPath-1 Item 7) | `Knowledge_Engine/_archive/CODEX_KE_ITEM7_TRANCHE_FILTER_delivered.md` | INTEGRATED | 2026-04-10 |
| KE-Item8 | Tranche Filter UI Feedback (CPath-1 Item 8) | `Knowledge_Engine/_archive/CODEX_KE_ITEM8_TRANCHE_UI_delivered.md` | INTEGRATED | 2026-04-10 |
| KE-2A | Yoga Check Evaluation Engine (16 evaluator types) | `Knowledge_Engine/CODEX_COMMISSION_KE_2A_YOGA_CHECK.md` | READY TO ISSUE | 2026-05-15 |

### KP Oracle (Krishna Prashnavali)

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| KP-2A | Bundle Editorial + Share Card + Remedies Admin Frontend | `KP/CODEX_COMMISSION_KP_2A.md` | READY TO ISSUE | 2026-05-14 |
| KP-2B | Ritual Animation + 3-Pillar UX + Astro-Filter | `KP/CODEX_COMMISSION_KP_2B.md` | READY TO ISSUE -- depends on KP-2A | 2026-05-14 |
| KP-Sprint2 | /ask-question LLM Logic Router (Guna + Gita) | `KP/CODEX_COMMISSION_KP_SPRINT2_ASK_QUESTION.md` | READY TO ISSUE | 2026-05-14 |

### Individual Reports

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| IR-1 | 5 Public SEO Landing Pages | `Individual_Reports/CODEX_COMMISSION_IR_1_LANDING_PAGES.md` | READY TO ISSUE | 2026-05-14 |
| IR-Contract-v1 | Original Contract Appointment (30 Mar 2026) | `Individual_Reports/_archive/CONTRACT_APPOINTMENT_v2026-03-30.md` | SUPERSEDED | 2026-03-30 |
| IR-Contract-v2 | Contract Update (2 Apr 2026) | `Individual_Reports/_archive/CONTRACT_UPDATE_v2026-04-02.md` | SUPERSEDED | 2026-04-02 |
| IR-Frontend-v1 | Frontend Commission (2 Apr 2026) | `Individual_Reports/_archive/INDIVIDUAL_REPORTS_FRONTEND_v2026-04-02.md` | SUPERSEDED by IR-1 | 2026-04-02 |

### Remedies Engine

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| REM-P1 | Remedies Engine Phase 1 (KP collection + remedy_ref pipeline) | `Remedies/CODEX_COMMISSION_REMEDIES_ENGINE_PHASE1.md` | READY TO ISSUE | 2026-05-14 |

### The Strategist

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| STR-1 | Premium Landing Page + War Room Visual Rebuild | `Strategist/CODEX_COMMISSION_STRATEGIST_LANDING_WARROOM.md` | READY TO ISSUE | 2026-05-14 |
| STR-Spec | Full Strategist Build Spec | `Strategist/THE_STRATEGIST_FULL_SPEC.md` | REFERENCE DOC | 2026-05-09 |

### Arc Angel

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| ARC-UI | Arc Angel UI Panel (ArcAngelPanel.jsx) | `Arc_Angel/CODEX_COMMISSION_ARC_ANGEL_UI_PANEL.md` | INTEGRATED | 2026-04-19 |

### Tarot

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| TAR-v4 | Tarot UI v4 Enhancement | `Tarot/CODEX_COMMISSION_TAROT_V4_UI.md` | READY TO ISSUE | 2026-04-30 |

### Kundali / Birth Chart

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| KUN-1 | Lagna Kundali Module Contract | `Kundali/CODEX_COMMISSION_KUNDALI_LAGNA_CONTRACT.md` | READY TO ISSUE | 2026-04-10 |
| KUN-Shadbala | Shadbala Engine (vedic_calculator.py) | `Kundali/_archive/CODEX_COMMISSION_SHADBALA_ENGINE_delivered.md` | INTEGRATED | 2026-04-25 |

### Lal Kitab (LK)

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| LK-1 | LK Standalone Module (onboard, remedies, debt audit, tracker) | `LK/CODEX_COMMISSION_LK_STANDALONE_MODULE.md` | READY TO ISSUE | 2026-05-09 |

### Longevity Report

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| LON-1 | Ayur Jyotish Longevity Report (main contract) | `Longevity/CODEX_COMMISSION_LONGEVITY_REPORT_CONTRACT.md` | READY TO ISSUE | 2026-04-10 |
| LON-H | Commission H brief (older, superseded by LON-1) | `Longevity/_archive/CODEX_COMMISSION_H_BRIEF_v2026-04-10.md` | SUPERSEDED | 2026-04-10 |

### Love & Engagement Module

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| LOVE-1 | Love & Engagement Module -- Backend Contract | `Love_Module/CODEX_COMMISSION_LOVE_ENGAGEMENT_MODULE.md` | INTEGRATED | 2026-04-02 |
| LOVE-FE | Love Module -- Frontend + SEO | `Love_Module/CODEX_COMMISSION_LOVE_MODULE_FRONTEND.md` | INTEGRATED | 2026-04-02 |

### Live TV

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| LTV-1 | Live TV: Sai Baba Arti (backend + frontend) | `Live_TV/CODEX_COMMISSION_LIVE_TV_SAI_BABA_ARTI.md` | INTEGRATED | 2026-04-25 |

### Punya Rewards (Offers & Gamification)

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| PUN-1 | Offers & Gamification (Punya Rewards engine) | `Punya_Rewards/CODEX_COMMISSION_PUNYA_REWARDS_GAMIFICATION.md` | INTEGRATED | 2026-04-25 |

### Notifications

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| NOTIF-1 | Notification Engine (web-app wide) | `Notifications/CODEX_COMMISSION_NOTIFICATION_ENGINE.md` | INTEGRATED | 2026-04-02 |

### Panchang

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| PAN-L1 | Language/Regional Pages (Tamil, Telugu, Malayalam, etc.) | `Panchang/CODEX_COMMISSION_PANCHANG_LANGUAGE_PAGES.md` | READY TO ISSUE | 2026-04-30 |

### SEO & Web Performance

| ID | Commission | Brief file | Status | Issued |
|---|---|---|---|---|
| SEO-1 | SEO + Marketing + Web Performance Optimisation | `SEO/CODEX_COMMISSION_SEO_WEBPERF.md` | READY TO ISSUE | 2026-04-30 |

---

## Archive Policy

When a commission is superseded or completed:
1. Rename the file with a suffix: `_delivered.md` or `_v2026-05-11.md`
2. Move to `[Module]/_archive/`
3. Update status in the INDEX row above

---

## Module Folder Map

| Folder | Module |
|---|---|
| `KP/` | Krishna Prashnavali Oracle |
| `Knowledge_Engine/` | Jyotish Knowledge Engine (rules library, yoga evaluator, library console) |
| `Individual_Reports/` | 5 Individual Report types + public landing pages |
| `Remedies/` | Remedies Engine (KP + LK collections, remedy_ref pipeline) |
| `Strategist/` | The Strategist premium tool (Lal Kitab career + landing page) |
| `Arc_Angel/` | Arc Angel (12 Areas of Life, dasha panel) |
| `Tarot/` | Tarot (daily draw, spreads, history, v4 UI) |
| `Kundali/` | Birth Chart / Lagna Kundali + Shadbala |
| `LK/` | Lal Kitab (onboard, remedies, debt audit, tracker) |
| `Longevity/` | Ayur Jyotish Longevity Report |
| `Love_Module/` | Love & Engagement Module (backend + frontend) |
| `Live_TV/` | Live TV: Sai Baba Arti |
| `Punya_Rewards/` | Punya Rewards (gamification, offers, wheel spin) |
| `Notifications/` | Notification Engine (email, push, WhatsApp) |
| `Panchang/` | Panchang language/regional pages |
| `SEO/` | SEO + Marketing + Web Performance |
