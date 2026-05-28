# #1 -- START HERE
## EverydayHoroscope -- Daily Session Entry Point

> Read this before every work session. Updated at each session end.
> Last updated: 2026-05-29

---

## Root Folder Map

| File / Folder | What it is |
|---|---|
| **`#1_START_HERE.md`** | This file -- daily briefing |
| **`#2_MASTER_TRACKER.md`** | All live modules + status dashboard |
| **`#3_ACTION_TRACKER.md`** | Open action items (owner: TT or CC) |
| **`#4_ROADMAP.md`** | Product roadmap to Play Store + Razorpay live |
| **`#5_CODEX_COMMISSION_TABLE.md`** | All commissions ever issued -- status + IDs |
| **`#6_WAYS_OF_WORKING.md`** | Governance: how Temple Team works with Codex |
| **`CLAUDE.md`** | Claude Code session guide -- infrastructure, file locations, env vars |
| **`PROJECT_STATUS.md`** | Module-level live status snapshot |
| **`EverydayHoroscope-WebApp_Architecture.md`** | Full architecture reference |
| **`KE_TEXTBOOK_DECODE/`** | All KE book decode + ingest work |
| **`SEO_20K/`** | All SEO 20K pages commissions + ECHO/PACE + process docs |
| **`Codex_Deliveries/`** | Module delivery folders + module-specific trackers |

---

## Platform Quick Reference

| | |
|---|---|
| Live URL | https://www.everydayhoroscope.in |
| Backend API | https://everydayhoroscope-api.onrender.com |
| Repo | `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration` |
| Main branch | `main` (deploy-on-push) |
| Frontend | Vercel (~2 min deploy) |
| Backend | Render Docker (~3 min deploy) |

---

## What's Live -- Module Snapshot

### Free Calculators (on NavBar)
| Calculator | Route | Status |
|---|---|---|
| Daily Horoscope | `/horoscope` | ✅ Live |
| Weekly Horoscope | `/weekly` | ✅ Live |
| Monthly Horoscope | `/monthly` | ✅ Live |
| Panchang | `/panchang` | ✅ Live |
| Birth Chart (Kundali) | `/birth-chart` | ✅ Live |
| Nakshatra Calculator | `/nakshatra-calculator` | ✅ Live |
| Auspicious Day Calculator | `/auspicious-calculator` | ✅ Live |
| Compatibility (Moon Sign) | `/compatibility/name` | ✅ Live |
| Numerology | `/numerology` | ✅ Live |
| Tarot | `/tarot` | ✅ Live |
| Lo Shu Grid | `/lo-shu-grid` | ✅ Live |

### Premium Reports
| Report | Route | Status |
|---|---|---|
| KP Oracle | `/kp-oracle` | ✅ Live |
| Arc Angel | `/arc-angel` | ✅ Live |
| The Strategist | `/strategist` | ✅ Live |
| Longevity Report | `/longevity-report` | ✅ Live |
| Love & Engagement | `/love-engagement` | ✅ Live |
| Brihat Kundali | `/brihat-kundali` | ✅ Live |
| Lumina (Spiritual Companion) | `/lumina` | ✅ Live |

### Other Live Modules
| Module | Status |
|---|---|
| Punya Rewards | ✅ Live |
| Live TV | ✅ Live |
| Faith Hubs (Gita, etc.) | ✅ Live |
| Admin Console | ✅ Live |
| Facebook Page Posting | ✅ Live |
| YouTube Posting | ✅ Live |

---

## Hottest Open Items This Week

| Priority | Item | Owner | Where |
|---|---|---|---|
| 🔴 HIGH | TAR-SEO-1 Tarot SEO -- build-verified locally, TT to integrate | TT | `Codex_Deliveries/Tarot/` |
| 🔴 HIGH | KE-OP-15 -- verify KE questionnaire live endpoints on Render | TT | `Codex_Deliveries/Knowledge_Engine/` |
| 🟡 MED | KP-OP-10/11 -- share card redesign + UX review | TT | `Codex_Deliveries/KP/` |
| 🟡 MED | Phaladeepika NLM -- begin Adhyaya II decode | NLM thread | `KE_TEXTBOOK_DECODE/Thread_Briefs/` |
| 🟡 MED | BPHS Vol 1 -- Thread A to confirm Q1/Q2 | BPHS thread | `KE_TEXTBOOK_DECODE/Thread_Briefs/` |
| 🟡 MED | KP Astrology -- claim_axis longevity retroactive pass | KP thread | `KE_TEXTBOOK_DECODE/Thread_Briefs/` |
| 🟡 MED | Codex Commission Tracker reconciliation -- GAP analysis | TT + CC | `#5_CODEX_COMMISSION_TABLE.md` |
| 🟢 LOW | WhatsApp OTP verification (M-5) | TT | Meta WhatsApp Manager |
| 🟢 LOW | Instagram Business Account ID (M-6) | TT | Meta Business Dashboard |

---

## Knowledge Engine -- Decode Status Summary

| Book | Status | Rules decoded | Next step |
|---|---|---|---|
| KP Astrology | 🟡 NEAR COMPLETE | 256 / 77 files | claim_axis longevity pass |
| BPHS Vol 1 | 🟡 IN PROGRESS | Ch11-Ch24 done | Karaka → Yoga → Dasha chapters |
| Phaladeepika | 🟢 UNBLOCKED | 0 (not yet started) | Begin Adhyaya II |
| Longevity (Unnatural) | See tracker | -- | -- |
| Medical Astrology | See tracker | -- | -- |

Schema amendments live as of commit `25201e4`. Dedup commission ready to issue when Codex quota resets.

---

## Session End Checklist

Before ending every session:
- [ ] Update `#2_MASTER_TRACKER.md` -- add version history row for each module touched
- [ ] Update `#3_ACTION_TRACKER.md` -- tick off completed items, add new ones
- [ ] Commit all doc changes with `docs:` prefix
- [ ] If any Codex commission was issued or integrated, update `#5_CODEX_COMMISSION_TABLE.md`

---

*Template: update the "Last updated" date and "Hottest Open Items" section at every session start.*
