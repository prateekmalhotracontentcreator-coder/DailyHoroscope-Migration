# BPHS_VOL1_NLM.md  (NLM Triage Tracker)
> Last updated: 2026-06-01

## ✅ CLOSED STAGES (verified in MongoDB 2026-06-01)

### Stage A -- Contradiction Pairs ✅ CLOSED
Live DB inspection (inspect_bphs_phase1_issues.py) confirmed: **0 rules in contradiction_hold**.
The 13 pairs tracked here were resolved in a prior session via `apply_contradiction_decisions.py`.
Tracker was never updated. Closing now. No further NLM action needed.

Total pairs: **13** | Resolved: 13 | Pending: **0** ✅

### Stage B -- PHR Batch Triage ✅ CLOSED
Live DB inspection confirmed:
- Ch 15: 0 / 2 rules in PHR (auto-approve rate 100%) ✅
- Ch 19: 0 / 78 rules in PHR (auto-approve rate 100%) ✅
Both chapters fully cleared in a prior session. Tracker was stale.

## Stage C -- Ch34 Flagged Rules ✅ FULLY CLOSED (2026-06-01)
All 15 flagged rules resolved. Live DB confirms: `Ch34 flagged = 0`.

### C-1: 12 Truncation Artifact Rules ✅ CLOSED
Script: `patch_ch34_flagged.py --apply` run 2026-06-01. All 12 patched `flagged → pending_human_review`.
NLM thread to re-decode from source slokas in a future session.

Rule IDs resolved: bphs-ch34-041, 042, 045, 047, 050, 053, 054, 055, 058, 059, 060, 082

### C-2: 3 Content-Flag Rules ✅ CLOSED
GAI doctrinal review 2026-06-01. Script: `patch_ch34_content_flags_v2.py --apply`.
All 3 patched `flagged → auto_approved`. Co-founder sign-off required before live.

| Rule ID | Decision | Outcome |
|---|---|---|
| bphs-ch34-024 (Jupiter/Taurus) | APPROVED_WITH_EDITS | Flag valid: 11th mischaracterised as "most evil". Corrected in condition_notes. |
| bphs-ch34-035 (Venus/Cancer) | APPROVED_WITH_EDITS | Flag valid: Moolatrikona sign conflated with own sign. Corrected in condition_notes. |
| bphs-ch34-049 (Saturn/Libra) | APPROVED_AS_IS | False flag: Yogakaraka exception not recognised by validator. Decode note added. |

## Stage D -- yoga_check ✅ CLOSED (was false alarm -- field path was wrong)

The inspect script was querying `validation.yoga_check` -- that field has never existed.
Live DB inspection (2026-06-01) confirmed yoga_check data IS fully populated at:
- `condition.yoga_check` -- rich structured object (type, checkable, description, sign_numbers, etc.)
- `metadata.yoga_checkable` -- boolean flag
- `interpretation.tags` -- includes `"yoga_checkable"` tag

Example from bphs-ch35-003:
```json
"condition": {
  "yoga_check": {
    "type": "sign_quality_all",
    "checkable": true,
    "description": "All 7 planets must be in dual/mutable signs: Gemini (3), Virgo (6), Sagittarius (9), Pisces (12).",
    "sign_quality": "dual",
    "sign_numbers": [3, 6, 9, 12]
  }
}
```

`migrate_yoga_check.py` (written in error) -- do NOT run. Data already present.
Inspect script Issue 5 query corrected to check `condition.yoga_check` instead.

## NLM Session Log
| Date | Stage | Rules Reviewed | Outcome |
|---|---|---|---|
| Prior session | Stage A | 13 contradiction pairs | All resolved ✅ (tracker was stale) |
| Prior session | Stage B | Ch15 + Ch19 PHR | All cleared ✅ (tracker was stale) |
| 2026-06-01 | Stage C-1 | 12 Ch34 truncation rules | flagged → PHR via patch_ch34_flagged.py ✅ |
| 2026-06-01 | Stage C-2 | 3 Ch34 content-flag rules | GAI review → auto_approved via patch_ch34_content_flags_v2.py ✅ |
| 2026-06-01 | Stage D | yoga_check field audit | False alarm -- condition.yoga_check fully populated (197/197 rules) ✅ |
| 2026-06-01 | Final verify | inspect_bphs_phase1_issues.py | All 5 issues confirmed 0. Phase 1 CLEAN. ✅ |

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
