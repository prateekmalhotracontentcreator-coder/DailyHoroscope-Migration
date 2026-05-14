# LIGHT TOUCH CLEANUP PLAN
**Scope:** Document review & arrangement ONLY (no code rewrites, no refactoring)  
**Duration:** 3-5 days  
**Purpose:** Clarity & insight without resource drain  
**When ready for refactor:** Use findings as blueprint for Phase 2 (later)

---

## CATEGORIZATION MATRIX

### **🔴 MUST HAVE (Do This Week)**

**Why:** Blocks clarity, needed for go-live roadmap, prevents knowledge loss

| Task | Effort | Output | Reason |
|---|---|---|---|
| **Phase 1A: Backend routers audit** | 4 hrs | `docs/BACKEND_ROUTERS_AUDIT.md` | 70+ files; need to know what exists |
| **Phase 1B: Root-level doc audit** | 3 hrs | `docs/ROOT_LEVEL_DOCS_AUDIT.md` | HANDOVER reconciliation critical |
| **Phase 2A: Extract 11 exported sessions** | 8 hrs | `memory/SESSION_1-11_SUMMARIES.md` | Know what was done; prevent repeats |
| **Phase 3A: Reconcile docs vs. sessions** | 4 hrs | `memory/RECONCILIATION_MATRIX.md` | Identify gaps (key deliverable) |
| **Deliverable A: Progress Tracker** | 3 hrs | `docs/PROGRESS_TRACKER.md` | Go-live roadmap (needed for Play Store) |
| **Deliverable C: Codex tracker** | 2 hrs | `docs/CODEX_COMMISSIONS_TRACKER.md` | Know commission status |
| **Deliverable D: Optimization insights** | 2 hrs | `docs/OPTIMIZATION_REPORT_SUMMARY.md` | Tech debt awareness |
| **Total Must Have Effort** | **26 hrs** ≈ **3-4 days** | -- | -- |

---

### **🟢 GOOD TO HAVE (Do if time allows this week; else next week)**

**Why:** Useful for future refactors, but not blocking go-live

| Task | Effort | Output | Reason |
|---|---|---|---|
| **Phase 1A: Frontend pages audit** | 3 hrs | `docs/FRONTEND_PAGES_AUDIT.md` | Feature completeness check |
| **.claude/ folder audit (briefs)** | 2 hrs | `.claude/BRIEFS_INVENTORY.md` | Codex comm organization (deferred) |
| **Phase 2B: Read 11 chat-mode sessions** | 10 hrs | `memory/SESSION_0.01-0.11_SUMMARIES.md` | Context, but can read async |
| **Deliverable E: Modules/Features inventory** | 2 hrs | `docs/MODULES_FEATURES_INVENTORY.md` | Launch checklist (defer to after Play Store) |
| **Deliverable F: Documentation audit** | 3 hrs | `docs/DOCUMENTATION_AUDIT.md` | Decide what to keep/retire (Phase 2 task) |
| **Deliverable G: Session-wise summaries (full)** | 8 hrs | `memory/SESSION_SUMMARIES_BY_FEATURE.md` | Detailed; can do async |
| **Total Good To Have Effort** | **28 hrs** ≈ **3-4 days** | -- | **Defer to Week 2** |

---

### **🟡 CAN WAIT (Phase 2+ work)**

**Why:** Resource-heavy, requires code knowledge, no blocking impact now

| Task | Effort | Impact | Why Wait |
|---|---|---|---|
| **Folder reorganization** (backend routers → routers/ subdir) | 8 hrs | Code structure | Use audit findings as blueprint; defer until after Play Store |
| **Codex briefs reorganization** (.claude/briefs/) | 4 hrs | Navigation | Use inventory as guide; do when refactoring |
| **.claude/archived/** setup | 2 hrs | Cleanup | After you've read old HANDOVERs |
| **CLAUDE.md update** (post-session-22) | 4 hrs | Documentation | After full reconciliation; defer to Week 2 |
| **Settings.local.json documentation** | 1 hr | Reference | Low priority |
| **Database schema review** (vs. actual code) | 6 hrs | Tech debt | Analysis; action in Phase 2 |
| **Test reports classification** | 2 hrs | Housekeeping | Do when deploying to Play Store |
| **Total Can Wait Effort** | **27 hrs** | -- | **Week 2 or later** |

---

## EXECUTION PLAN (This Week)

### **Day 1 (Monday):** Foundation Audit
- [ ] Phase 1A: Backend routers audit (map 70+ files)
  - Output: Categorize by: core / premium-reports / engagement / notifications / admin
  - Time: 4 hrs
  
- [ ] Phase 1B: Root-level doc audit (HANDOVER + specs)
  - Output: Timeline of decisions (which HANDOVER decided what)
  - Time: 3 hrs

**Deliverable:** `docs/BACKEND_ROUTERS_AUDIT.md` + `docs/ROOT_LEVEL_DOCS_AUDIT.md`

---

### **Day 2 (Tuesday):** Session Extraction (Exported Sessions)
- [ ] Phase 2A: Extract all 11 exported sessions (folders 1-11)
  - Parse .jsonl for: key decisions, blockers, deliverables, Codex commission status
  - Time: 8 hrs
  
**Deliverable:** `memory/SESSION_1-11_SUMMARIES.md` (key findings per session)

---

### **Day 3 (Wednesday):** Reconciliation
- [ ] Phase 3A: Reconcile findings (docs vs. sessions)
  - Identify: What was decided in sessions but not documented?
  - Identify: What was documented but contradicted by sessions?
  - Time: 4 hrs
  
- [ ] Deliverable A: Progress Tracker
  - Status of all 27 modules (% complete, blockers, next milestone)
  - Time: 3 hrs

**Deliverable:** `memory/RECONCILIATION_MATRIX.md` + `docs/PROGRESS_TRACKER.md`

---

### **Day 4 (Thursday):** Commission & Optimization Tracking
- [ ] Deliverable C: Codex Commissions Tracker
  - All 18+ commissions: status, gaps, integration notes
  - Time: 2 hrs
  
- [ ] Deliverable D: Optimization Insights (summary)
  - Token usage, perf, code structure observations
  - Time: 2 hrs

**Deliverable:** `docs/CODEX_COMMISSIONS_TRACKER.md` + `docs/OPTIMIZATION_REPORT_SUMMARY.md`

---

### **Day 5 (Friday):** Review & Buffer
- [ ] Review all outputs from Days 1-4
- [ ] Spot-check for contradictions or gaps
- [ ] If time: Start Phase 2B (chat-mode sessions) -- but defer if not complete

**Deliverable:** Clean, final versions ready for archive

---

## DELIVERABLES FOR THIS WEEK (MUST HAVE)

| Deliverable | File | Purpose | Input | Output |
|---|---|---|---|---|
| A | `docs/PROGRESS_TRACKER.md` | Go-live roadmap | Reconciliation findings | Module status + blockers + next steps |
| C | `docs/CODEX_COMMISSIONS_TRACKER.md` | Commission status | Exported session summaries | 18+ commissions: complete/pending/blocked |
| D | `docs/OPTIMIZATION_REPORT_SUMMARY.md` | Tech debt awareness | Backend/frontend audit | 5-10 key optimization opportunities |
| -- | `docs/BACKEND_ROUTERS_AUDIT.md` | Router inventory | Code review | 70+ routers categorized by purpose |
| -- | `docs/ROOT_LEVEL_DOCS_AUDIT.md` | Doc reconciliation | HANDOVER review | Decision timeline + conflicts identified |
| -- | `memory/SESSION_1-11_SUMMARIES.md` | What was done | .jsonl parsing | 11 session snapshots (key decisions + deliverables) |
| -- | `memory/RECONCILIATION_MATRIX.md` | Gaps identified | Docs vs. sessions | Where docs are incomplete/outdated |

**Total deliverables this week:** 7 documents  
**Total effort:** ~26 hours ≈ 3-4 days  
**Expected completion:** Friday EOD

---

## SCOPE BOUNDARIES (LIGHT TOUCH = Document Review Only)

### ✅ DO:
- [x] Read existing code files (routers, services) to understand what exists
- [x] Parse .jsonl chat transcripts to extract key decisions
- [x] Create audit/inventory documents (listing, categorizing)
- [x] Identify gaps between what's documented vs. what exists
- [x] Note observations (e.g., "70+ routers in root folder -- recommend subfolder structure")
- [x] Create recommendations (no implementation)
- [x] Write synthesis documents (combining audit findings)

### ❌ DON'T:
- [ ] Move files around (defer folder reorganization to Phase 2)
- [ ] Rename routers, services, or components
- [ ] Edit existing code files
- [ ] Create new folder structures
- [ ] Run refactoring scripts
- [ ] Modify database schema
- [ ] Update CLAUDE.md or any live reference docs (yet)
- [ ] Archive chat sessions (you said "don't touch sessions for now")
- [ ] Rewrite any markdown files that are currently in use

---

## QUESTIONS / CLARIFICATIONS

1. **Phase 2B (11 chat-mode sessions):** Should I read these this week (if time allows after Must Have) or defer to Week 2? They require visiting shared links (no local files).
   
2. **Observation format:** For audit documents, should I use:
   - Simple list? (`Router1.py - purpose: X, status: Y`)
   - Detailed table? (name / purpose / status / notes / module area)
   - Categorized summary? (grouped by feature area)

3. **Reconciliation approach:** When I find contradictions (e.g., "Session 6 says X, but HANDOVER says Y"), should I:
   - Flag as `⚠️ CONFLICT FOUND` and note both versions?
   - Try to determine which is current?
   - List both with dates for you to decide?

4. **Backend audit depth:** For the 70+ routers, should I:
   - List file name + docstring purpose only? (quick)
   - Also note dependencies (what they import)? (detailed)

5. **Output format:** All outputs as `.md` files in `docs/` and `memory/` folders? Or would you prefer JSON for any (for programmatic use later)?

---

## RESOURCE IMPLICATION

**This week:**
- 26 hours of document review/analysis
- 0 hours of code changes
- 0 disruption to SEO/Marketing/Performance sessions
- Clarity gained → ready for Phase 2 refactoring later

**Next week (if approved):**
- Phase 2 can execute folder reorganization (4-5 days)
- Phase 2 can update CLAUDE.md based on findings
- Minimal disruption since blueprint is clear

---

**Ready to proceed with Light Touch Cleanup?**  
**Any clarifications needed before I start Day 1?**
