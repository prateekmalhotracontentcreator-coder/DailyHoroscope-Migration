# Codex Commission Brief — Cross-Thread Audit of Codex Main Folder
> Version 1.0 | 2 May 2026 | EverydayHoroscope / Temple Team
> Status: Ready to issue to a new Codex audit thread
> Type: Documentation / governance / cross-thread systems audit

---

## 1. Purpose

This commission opens a new Codex thread whose sole task is to conduct a **full audit of the Codex documentation and commission landscape** for EverydayHoroscope.

We are now in the advanced finalization stage of the app. Before new rule work and next-phase implementation begins, Temple Team needs:

1. a complete picture of all Codex commissions and threads
2. the current implementation/integration status of each
3. what remains open
4. blockers and dependencies
5. a better hierarchy for document storage and coordination
6. a governance structure where the **Knowledge Engine thread acts as project manager / integration coordinator** over sibling threads

This is a documentation and coordination audit, not a feature-build thread.

---

## 2. Project Brief

**EverydayHoroscope is the Temple.**

Each major system or module is a **sibling thread/module inside that Temple**. Historically, many threads, handovers, contract documents, brief drafts, and Codex delivery files have accumulated across multiple folders.

Temple Team now wants to consolidate these into a more durable operating model:

- **Knowledge Engine thread** becomes the project-management / integration coordinator layer
- sibling threads continue working in their own verticals
- cross-thread progress becomes visible in shared documents
- document arrangement becomes cleaner, more canonical, and easier to audit

---

## 3. Audit Scope

The new audit thread must review the **Codex Main Folder system**, with this order of priority:

### Primary folder
- `/Users/apple/DailyHoroscope-Migration/codex-deliveries/`

### Secondary folders / files
- `/Users/apple/DailyHoroscope-Migration/.claude/`
- root-level handovers and roadmap docs in:
  - `/Users/apple/DailyHoroscope-Migration/`
- other clearly commission-related docs found during audit

The audit should identify:
- duplicate specs
- stale specs
- conflicting source-of-truth documents
- docs that are operationally useful vs historical only
- docs that should become canonical vs archived

---

## 4. What Temple Team Needs From This Audit

At the end of the audit, Temple Team should be able to answer:

1. Which Codex commissions exist?
2. Which threads are still open, active, paused, blocked, or finished?
3. What was originally spec’d?
4. What was actually delivered?
5. What was integrated by Temple Team vs only drafted vs only committed locally?
6. What remains open for the next phase of implementation?
7. What blockers exist right now?
8. Which blockers are technical vs architectural vs documentation vs missing assets vs waiting on Temple decisions?
9. Which documents are canonical?
10. Which documents should be archived, merged, renamed, or retired?
11. What hierarchy should be adopted going forward?
12. What shared progress documents are needed so Knowledge Engine can act as project manager over sibling threads?

---

## 5. Core Audit Deliverables

The audit thread should produce **documentation artifacts**, not code features.

Minimum required outputs:

### Deliverable A — Master Commission Index
A single master document listing every identifiable commission/thread with:
- commission name
- thread/module owner
- source brief/spec file(s)
- current status
- implementation status
- integration status
- blocker status
- next action

Suggested filename:
- `CODEX_AUDIT_MASTER_INDEX.md`

### Deliverable B — Open Work Matrix
A compact matrix or table focused only on currently relevant work:
- open
- blocked
- paused
- ready-next

Suggested filename:
- `CODEX_OPEN_WORK_MATRIX.md`

### Deliverable C — Blockers Register
A dedicated blockers register with:
- blocker ID
- affected thread/module
- blocker type
- description
- owner
- unblock condition
- priority

Suggested filename:
- `CODEX_BLOCKERS_REGISTER.md`

### Deliverable D — Spec vs Delivery vs Integration Map
For each commission, show:
- spec issued
- delivery received
- Temple integration completed or not
- live/deployed or not

Suggested filename:
- `CODEX_SPEC_DELIVERY_INTEGRATION_MAP.md`

### Deliverable E — Documentation Hierarchy Proposal
Recommend the future folder/doc hierarchy:
- what stays in `.claude`
- what stays in `codex-deliveries`
- what belongs at repo root
- what should be archived
- naming standards for future docs

Suggested filename:
- `CODEX_DOCUMENT_HIERARCHY_PROPOSAL.md`

### Deliverable F — Shared Progress Registry Design
Temple wants a shared progress layer so sibling threads can keep reporting progress in a common format that Knowledge Engine can monitor.

The audit thread should propose:
- what common doc(s) should exist
- where they should live
- how each module thread updates them
- how Knowledge Engine consumes them

Suggested filenames:
- `CODEX_PROGRESS_REGISTRY_SPEC.md`
- `CODEX_MODULE_STATUS_TEMPLATE.md`

### Deliverable G — Knowledge Engine as PM Proposal
Define how Knowledge Engine should function as:
- integration coordinator
- dependency tracker
- cross-thread reviewer
- Temple-facing status owner

Suggested filename:
- `CODEX_COORDINATION_MODEL_KE_PM.md`

---

## 6. Minimum Data Fields Per Commission / Thread

For every commission/thread identified, Temple Team wants these fields captured where possible:

- commission / thread name
- module / domain
- originating brief/spec path
- delivery artifact path(s)
- Temple review status
- integration status
- deployment/live status
- current owner / thread
- current phase
- open items
- blockers
- dependencies
- next recommended action
- notes on document conflicts or ambiguity

Helpful additional fields:
- commit hash(s)
- last meaningful update date
- source-of-truth status
- whether work belongs to:
  - Temple-owned
  - joint
  - Codex-only

---

## 7. Status Taxonomy To Use

Use a consistent status model across the audit.

Recommended thread/commission status values:
- `planned`
- `brief_ready`
- `in_progress`
- `delivered_pending_review`
- `reviewed_pending_integration`
- `integrated_not_live`
- `live`
- `paused`
- `blocked`
- `superseded`
- `archived`

Recommended blocker types:
- `missing_asset`
- `missing_spec_decision`
- `missing_backend`
- `missing_frontend`
- `doc_conflict`
- `thread_lost`
- `env_or_credentials`
- `needs_temple_review`
- `depends_on_other_commission`

---

## 8. Specific Audit Questions Temple Wants Answered

The audit thread should answer these explicitly:

1. What are all currently active sibling threads?
2. Which threads are effectively abandoned, stale, or superseded?
3. Which commissions have multiple competing spec files?
4. Which areas already have enough documentation and which are under-documented?
5. Which docs are reference-only and which are operational?
6. What should become the canonical “go here first” document for:
   - project status
   - cross-thread status
   - blockers
   - commission briefs
   - handovers
7. What should the update discipline be for sibling threads so Knowledge Engine can track them without reading every local doc?

---

## 9. Future-State Goal

The desired future state after this audit is:

### Knowledge Engine role
Knowledge Engine becomes the **project manager / integration coordinator**:
- tracks major commissions
- tracks blockers and dependencies
- coordinates Temple-side review sequencing
- maintains the shared cross-thread view

### Sibling thread role
Each sibling thread:
- continues owning its own module
- keeps local technical docs as needed
- also updates a shared registry in a standard format whenever meaningful progress happens

### Documentation role
Docs become layered:
- canonical strategic docs
- active work tracking docs
- module-local docs
- archived historical docs

---

## 10. What the Audit Thread Must Not Do

- Do not begin feature implementation
- Do not rewrite all historical docs unless necessary
- Do not silently archive or delete files without explicit recommendation
- Do not assume current file location equals canonical truth
- Do not mix this audit with unrelated module development

The goal is:
- inventory
- reconciliation
- governance proposal
- recommended next structure

---

## 11. Reference Materials

The audit thread should read these first:

1. `/Users/apple/DailyHoroscope-Migration/NEW_SESSION_PRIMER.md`
2. `/Users/apple/DailyHoroscope-Migration/PROJECT_STATUS.md`
3. `/Users/apple/DailyHoroscope-Migration/CLAUDE.md`
4. `/Users/apple/DailyHoroscope-Migration/codex-deliveries/CODEX_WAYS_OF_WORKING.md`
5. `/Users/apple/DailyHoroscope-Migration/CODEX_MASTER_ROADMAP.md`
6. `/Users/apple/DailyHoroscope-Migration/KNOWLEDGE_ENGINE_HANDOVER.md`
7. root-level handover files in `/Users/apple/DailyHoroscope-Migration/`
8. commission docs in `/Users/apple/DailyHoroscope-Migration/codex-deliveries/`
9. source briefs in `/Users/apple/DailyHoroscope-Migration/.claude/`

Codex should inspect the folder layout itself before finalizing the audit output.

---

## 12. Suggested Work Sequence for the Audit Thread

The audit thread should work in this order:

1. inventory all commission/spec/handover documents
2. identify duplicates and likely canonical docs
3. build a full commission/thread matrix
4. identify open work and blockers
5. identify document conflicts and hierarchy problems
6. propose the future documentation structure
7. propose the shared progress-registry model
8. propose the Knowledge Engine PM/coordinator model
9. produce the final audit pack

---

## 13. Acceptance Criteria

Temple Team will consider the audit successful if:

1. all identifiable commissions/threads are inventoried
2. current status of each is visible at a glance
3. blockers are clearly separated from general open work
4. source-of-truth document ambiguity is called out explicitly
5. a practical folder/document hierarchy is proposed
6. a shared progress-registry design exists
7. the Knowledge Engine PM/coordinator role is clearly defined
8. the audit outputs are strong enough to drive next-phase planning without re-discovery work

---

## 14. First Response Expected From the New Audit Thread

The first response should:

1. confirm understanding that this is a **documentation/governance audit**, not a build thread
2. state which folder(s) it will inventory first
3. identify the expected output artifacts it plans to produce
4. then begin the audit

