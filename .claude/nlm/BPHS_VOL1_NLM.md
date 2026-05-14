# BPHS_VOL1_NLM.md  (NLM Triage Tracker)
> Last updated: 2026-05-08

## Stage A -- Contradiction Pairs
Target: Resolve 13 pairs in Ch 12-23
MongoDB query:
```
col.find({
  "science_id": "jyotish",
  "validation.approval_status": "contradiction_hold",
  "source_chapter": {"$regex": "^bphs-ch(1[2-9]|2[0-3])"}
})
```
Total pairs: **13** | Resolved: 0 | Pending: 13

| Pair # | Rule IDs | Chapter | Topic | Decision | Date |
|---|---|---|---|---|---|
| (populate as NLM sessions run) | | | | | |

## Stage B -- PHR Batch Triage
Target: Clear 30-40 PHR rules per NLM session. Priority chapters: Ch 15, Ch 19.
MongoDB query (Ch 15 + 19 PHR batch):
```
col.find({
  "science_id": "jyotish",
  "source_chapter": {"$in": ["bphs-ch15", "bphs-ch19"]},
  "validation.approval_status": "pending_human_review"
}).limit(40)
```
Ch 15 PHR count: ~high (auto-approve rate 25%)
Ch 19 PHR count: ~high (auto-approve rate 33%)
Cleared this run: 0

## Stage C -- False Flag Bulk Approval
Target: Ch 34 flagged=15 (confirmed false truncation pattern -- no NLM needed)
Script ready: bulk_approve_ch34_false_flags.py (TO BE WRITTEN)
Action: Write script → dry-run → confirm 15 rules → --apply

## NLM Session Log
| Date | Stage | Rules Reviewed | Outcome |
|---|---|---|---|
| (populate after each session) | | | |

## How to Run NLM Session
1. Run Stage A query → export rule_id + rule_text + conflicting_rule_text
2. Paste into NotebookLM with BPHS source uploaded
3. Ask: "Which of these two rules is directly stated in the source text?"
4. Record decision → run apply_contradiction_decisions.py with decision list
5. For Stage B: export PHR rule texts → ask NLM to confirm source origin
