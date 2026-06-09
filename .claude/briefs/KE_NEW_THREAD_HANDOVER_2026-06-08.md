# Knowledge Engine -- New Thread Handover Brief
> **Compiled:** 2026-06-08 | **Author:** Account 1 (Main Thread)
> **Purpose:** Self-contained brief for a new Claude Code thread picking up KE decode/ingest work.
> **Read this file in full before running any script or touching any JSON.**

---

## 🔴 STEP 0 -- Resolve MongoDB Connectivity FIRST

**The previous Account 2 sessions stopped because MongoDB ingest was broken.**
All `seed_*` and `ingest_*` scripts were failing to connect. No rules could be uploaded.
**This is the first thing to fix -- before NLM triage, before any ingest, before anything.**

```bash
# 1. Confirm MONGO_URL is set
echo $MONGO_URL     # Must NOT be empty

# 2. Confirm ANTHROPIC_API_KEY is set (needed for the validator)
echo $ANTHROPIC_API_KEY   # Must start with sk-ant-

# 3. Quick connectivity check
PYTHONPATH=backend python3 -c "
import asyncio, motor.motor_asyncio, os
async def check():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ['MONGO_URL'])
    dbs = await client.list_database_names()
    print('Connected. Databases:', dbs)
asyncio.run(check())
"
```

**Expected output:** `Connected. Databases: ['horoscope_db', ...]`
- `horoscope_db` must appear in the list -- this is PRODUCTION.
- `EverydayHoroscope` may appear -- it is RETIRED. Never use it.

**If connection fails:** Go to Render dashboard → MongoDB service → confirm the service is running
and copy a fresh `MONGO_URL` connection string. The IP allowlist may have changed.

**Do NOT proceed to any ingest or triage work until this check passes cleanly.**

---

## 1. Project Context

**EverydayHoroscope** (`everydayhoroscope.in`) -- Vedic astrology platform.
- Backend: FastAPI on Render (Docker) | DB: MongoDB `horoscope_db`
- Repo: `github.com/prateekmalhotracontentcreator-coder/DailyHoroscope-Migration`
- **Read `CLAUDE.md` first** -- it is auto-loaded and governs architecture, env vars, and commit format.

The **Knowledge Engine (KE)** is a MongoDB collection (`interpretation_rules`) of decoded
astrology rules extracted from source books. Rules power the live interpretation layer.
Zero `approved` rules are live yet -- Legacy Model is the only active signal.

### Two Approval Levels -- Critical Distinction

| Status | Meaning | Reaches Live Users? |
|---|---|---|
| `auto_approved` | AI validator passed | ❌ NO -- co-founder sign-off still required |
| `approved` | Co-founder signed off | ✅ YES -- only this status is live |
| `pending_human_review` | Minor validator doubts | ❌ NO -- in review queue |
| `flagged` | Validator found a problem | ❌ NO -- must investigate |

---

## 2. The Two Worktrees to Reference

All decode session state lives in these worktrees. Read them directly -- do not guess.

### Worktree A -- Process docs + Book Status (most recent)
```
/Users/apple/DailyHoroscope-Migration/.claude/worktrees/sleepy-mcnulty-2c4e13/
```

Key files:
```
KE_Book_Decode_Process_Technical.md    ← Read before any decode work
.claude/ke/BOOK_STATUS.md              ← Chapter-by-chapter ingest status (last updated 2026-05-20)
.claude/ke/INGEST_PROCESS_BRIEF.md     ← 7-step workflow (live copy in main repo too)
.claude/HANDOVER_2026-05-14.md         ← Last full Account 2 session summary
```

### Worktree B -- Branch A process clarification (critical)
```
/Users/apple/DailyHoroscope-Migration/.claude/worktrees/dreamy-mahavira-4e7336/
```

Key files:
```
.claude/ke/nlm/BPHS_VOL1_NLM.md       ← NLM triage tracker (13 contradiction pairs, 0 resolved)
```

Last commit on this worktree (`3e471fe`) contains the critical correction:
> **Branch A = refine and complete the existing NLM JSON. NOT writing rules from scratch.
> If a JSON Ready doc already exists for a chapter, that is your starting point.
> Writing from scratch when NLM work exists is a PROCESS VIOLATION.**

### Additional Worktrees (for reference)
```
bold-heisenberg-a698a3   ← BPHS Vol 2 Ch 55 split-upgrade (last active KE ingest session)
brave-antonelli-f0f104   ← 829 rules ingested, Ch 48 next (older session)
```

---

## 3. Process Reference Files (Main Repo)

All process documentation lives in the **main repo** (not only in worktrees):

```
.claude/ke/INGEST_PROCESS_BRIEF.md          ← THE 7-step workflow -- read before any ingest
.claude/ke/BOOK_STATUS.md                   ← Chapter-by-chapter book progress
.claude/ke/KNOWLEDGE_VALIDATION_WORKFLOW.md ← Validator reference
.claude/ke/KE_DEDUP_SEMANTIC_PASS_SPEC.md   ← Dedup strategy spec
.claude/ke/ingest/                          ← Per-book ingest guides (9 books)
.claude/ke/nlm/BPHS_VOL1_NLM.md            ← NLM triage tracker (see Worktree B for latest)

Codex_Deliveries/Knowledge_Engine/
  CODEX_KNOWLEDGE_ENGINE_CONTRACT.md        ← Master KE contract
  TRACKER.md                                ← Module-level tracker
  CODEX_COMMISSION_KE_2A_YOGA_CHECK.md      ← KE-2A yoga check commission (not yet issued)

backend/scripts/INGEST_NOTES.md             ← Per-chapter ingest log with batch IDs
backend/scripts/validate_rules.py           ← AI validator script
backend/scripts/ke_dedup_script.py          ← Cross-book dedup script
```

---

## 4. Current DB State (as of 2026-05-20)

**Database: `horoscope_db` -- ALL WORK TARGETS THIS DB. Never `EverydayHoroscope`.**

| Book | Chapters In | Total Rules | Auto-Approved | PHR | Status |
|---|---|---|---|---|---|
| **BPHS Vol 1** | Ch 12-24, 27, 34, 35-40, 43, 44 | ~1,069 | ~628 | ~447 (352 PHR + 95 flagged) | Ingested + Validated; NLM triage pending |
| **BPHS Vol 2** | Ch 47, 48, 52-60 | ~2,227 | 1,092 | ~772 (582 PHR + 190 flagged) | Ingested + Split-Upgrade; PHR triage pending |
| **A Text-Book of Astrology** | Ch 15, 16 | 1,659 | 589 | ~941 (639 PHR + 302 flagged) | Ingested + Validated; PHR triage pending |
| **Lal Kitab** | Ch 19-28 | ~445 | ~275 | ~159 (149 PHR + 10 flagged) | Ingested + Validated; PHR triage pending |
| **Mundane Astrology** | Multiple chapters | 328 rules + 102 specs | **326 approved** | 2 intentional holds | ✅ COMPLETE |
| **Jyotish Remedies & Mantras** | Book E (100 Remedies) | 100 | 45 | 50 PHR | Ingested; PHR triage pending |
| **Strategist Rules** | 22-record patch | 22 | **22 approved** | 0 | ✅ Approved + live |
| **Sarvato Bhadra Chakra V2** | Ch 2-18 (Ch 15/19/20 scoped out) | 181 rules extracted | ✅ Decoded | ⛔ Awaiting decisions | 7 blocking priority conflicts (OQ-08-01 to OQ-18-01) + 6 architecture decisions TT must resolve |
| **Longevity & Astro System (KP)** | Ch 4-58 | Ch 6-19: full rules; Ch 20-58: benchmark log only | ✅ Decoded | ⛔ Awaiting ingest | Ch 36-58 case study rules = separate Codex commission not yet briefed |

**Chapters NOT yet ingested (future roadmap):**
- BPHS Vol 1: Ch 1-11, 25-26, 28-33, 41-42, 45-46, 61+
- BPHS Vol 2: Ch 49-51 excluded by co-founder decision; other chapters open
- A Text-Book of Astrology: Ch 1-14, 17+ (RTF source needed)
- Lal Kitab: Ch 29+ (confirm if remaining chapters exist in source folder)

---

## 5. Ingest Freeze Status

**FREEZE LIFTED ✅ -- confirmed 2026-05-17.**
KE-Sprint2 (arbitration runtime) closed -- all 5 acceptance gates passed. Co-founder confirmed 2026-05-22.
New chapter ingest may proceed. All ingest targets `horoscope_db`.

> Note: Worktrees `sleepy-mcnulty-2c4e13` and `dreamy-mahavira-4e7336` still show
> "FREEZE ACTIVE" in their local `CLAUDE.md` -- this is stale. The main repo `CLAUDE.md`
> and `INGEST_PROCESS_BRIEF.md` are correct: **FREEZE LIFTED**.

---

## 6. NLM Triage Queue -- Active Work (nothing started yet)

Three stages in priority order. Read `BPHS_VOL1_NLM.md` in Worktree B for the full tracker.

### Stage A -- Contradiction Pairs (highest priority)
13 contradiction pairs in BPHS Ch 12-23. **Zero resolved.** This is the most pressing KE task.

```python
# MongoDB query to pull them:
col.find({
  "science_id": "jyotish",
  "validation.approval_status": "contradiction_hold",
  "source_chapter": {"$regex": "^bphs-ch(1[2-9]|2[0-3])"}
})
```

Process:
1. Export rule_text + conflicting_rule_text for each pair
2. Paste into NotebookLM with BPHS source PDF uploaded
3. Ask: "Which of these two rules is directly stated in the source text?"
4. Record decision → run `apply_contradiction_decisions.py`

### Stage B -- PHR Batch Triage (Ch 15 and Ch 19 first)
Ch 15 has 25% auto-approve rate (worst in BPHS Vol 1). Ch 19 at 33%.

```python
col.find({
  "science_id": "jyotish",
  "source_chapter": {"$in": ["bphs-ch15", "bphs-ch19"]},
  "validation.approval_status": "pending_human_review"
}).limit(40)
```

### Stage C -- Ch 34 False Flag Bulk Approval
15 flagged rules in Ch 34 confirmed as truncation false flags.
`bulk_approve_ch34_false_flags.py` needs to be written, dry-run, confirmed, then `--apply`.

---

## 7. The 7-Step Ingest Workflow (never skip any step)

Full detail in `.claude/ke/INGEST_PROCESS_BRIEF.md`. Short version:

```
Step 0  → Source schema audit (before writing any ingest script)
Step 1  → Dry run --dry-run --save rules.json
Step 2  → Review the JSON (batch_id, science_id, approval_status = "pending_review")
Step 2B → AI validate LOCAL JSON before upload (validate_rules.py --json-file)
Step 3  → Upload the _VALIDATED.json (NOT the raw dry-run JSON)
Step 4  → Post-upload structural confirm (validate_rules.py --batch-id --mongo-url)
Step 5  → Inspect flagged rules (read flag reason -- 7 flag types, most are false flags)
Step 6  → Patch script (inspect-only first, then --patch)
Step 7  → Commit (update INGEST_NOTES.md first)
Step 7A → Yoga chapter sync (backfill_metadata_yoga_checkable.py) -- yoga chapters only
```

### Critical field rules (learned from prior session failures):

| Field | Rule |
|---|---|
| `approval_status` at upload | Must be `"pending_review"` (NOT `"pending_human_review"`) -- validator filters on this. Wrong value = validator finds 0 rules and silently skips the batch. |
| `source.batch_id` | Must be set INSIDE the `source` dict AND as top-level `batch_id`. Both. |
| "Found 0 rules to validate" | RED FLAG after a fresh upload -- investigate immediately, never accept and move on. |
| Validator doctrinal flags | Validator is authoritative on STRUCTURE, NOT on Vedic doctrine. Always cross-check the source PDF before accepting a doctrinal flag. |
| KP / Jaimini / Nadi rules | Validator applies classical BPHS frame -- will generate false flags on non-BPHS rules. Classify as Bucket B (framework error), patch to `pending_human_review` + `validator_error: True`. |

---

## 8. Five Do-Nots (process violations from prior sessions)

1. **Do NOT write rules from scratch** on a Branch A chapter if a JSON Ready doc already exists -- refine it
2. **Do NOT use `EverydayHoroscope` DB** -- it is a retired snapshot of ~3,796 stale rules
3. **Do NOT upload without dry run** -- idempotent upsert protects DB but wastes credits on bad data
4. **Do NOT patch flagged rules without reading the flag reason** -- classify the flag type first
5. **Do NOT confuse `auto_approved` with `approved`** -- zero `approved` rules means Legacy Model is the only live signal

---

## 9. Session Decode Links

These are the prior Account 2 sessions you are picking up from, in chronological order.
Each worktree represents a session. The branch name is the session identifier.

| Session / Worktree | Key Work Done | State Left |
|---|---|---|
| `brave-antonelli-f0f104` | BPHS Vol 1 Phase 1 ingest (earlier chapters). 829 rules total at close. Ch 48 identified as next. | Old -- superseded by later sessions |
| `bold-heisenberg-a698a3` | BPHS Vol 2 Ch 55 split-upgrade complete (+153 rules). Last active ingest session. | Split-upgrade done; PHR triage pending |
| `dreamy-mahavira-4e7336` | NLM tracker setup for BPHS Vol 1 (BPHS_VOL1_NLM.md). Branch A protocol clarification (commit 3e471fe). | 13 contradiction pairs documented, 0 resolved |
| `sleepy-mcnulty-2c4e13` | Process doc updates: KE_Book_Decode_Process_Technical.md, INGEST_PROCESS_BRIEF.md. BOOK_STATUS.md updated to 2026-05-20. | Latest process state -- read this worktree's docs as authoritative |

**The most recent state is in `sleepy-mcnulty-2c4e13`.** Use it as your starting point for all process references.

---

## 10. Source Book Folder Locations

Decoded JSON files and source PDFs are at:
```
/Users/apple/Documents/Knowledge Engine_eBooks/
```

Sub-folders per book (confirm exact names by running `ls` on that path):
- `BPHS_Vol1_CC_Decode/`
- `BPHS_Vol2_CC_Decode/`
- `New Ingest_5 Books/1. Sarvato Bhadra Chakra_V2/`  ← SBC V2 (181 rules, ready to ingest pending TT decisions)
- `Longevity_CC_Decode/`  ← 14 decoded files + 2 benchmark files

---

## 11. What the Co-Founder Needs to Decide (blockers)

These are NOT a new thread's job -- surface them to the user so they can unblock:

1. **SBC 7 Priority Conflicts** (OQ-08-01 to OQ-18-01): Which rule wins when two SBC signals conflict? These are architectural decisions that block SBC ingest.
2. **SBC 6 Architecture Decisions**: 6 lookup datasets to ingest as separate collections (`vedha_coordinates`, `latta_coordinates`, etc.) -- need collection and schema approval before ingest.
3. **Longevity Ch 36-58**: Case study rule extraction is a separate Codex commission not yet briefed. New thread cannot ingest these without that commission.

---

## 12. Immediate Next Steps (in order)

1. ✅ Run MongoDB connectivity check (Step 0 above) -- fix before anything else
2. ✅ Read `KE_Book_Decode_Process_Technical.md` in `sleepy-mcnulty-2c4e13`
3. ✅ Read `.claude/ke/INGEST_PROCESS_BRIEF.md` (main repo)
4. ✅ Read `.claude/ke/BOOK_STATUS.md` for current chapter state
5. **Await co-founder instruction** on which task to start:
   - Option A: Begin Stage A NLM triage (13 contradiction pairs -- most pressing)
   - Option B: Run Stage C bulk approval script for Ch 34 (15 false flags -- quickest win)
   - Option C: Begin new chapter ingest (freeze lifted -- co-founder to specify which chapter)

---

## 13. Environment Checklist (run before every session)

```bash
echo $MONGO_URL            # Must not be empty
echo $ANTHROPIC_API_KEY    # Must not be empty (sk-ant-...)
```

All scripts run from repo root with `PYTHONPATH=backend`.

Never set `--db-name EverydayHoroscope`. Always `--db-name horoscope_db`.
