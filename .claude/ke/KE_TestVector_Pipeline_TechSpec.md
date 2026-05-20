# KE Test Vector Pipeline -- Technical Specification
> **Status:** DRAFT -- Awaiting TT Review & Approval before Codex Commission is issued
> **Prepared:** 2026-05-20 | **Author:** Claude Code
> **Scope:** a) Test SBC engine · b) Universal framework for all KE modules and reports

---

## 1. Purpose

The Test Vector Pipeline is the KE's regression and validation layer. It allows the engine to:
- Verify that a set of known historical events is correctly predicted by the rule set
- Catch regressions when rules are added, modified, or arbitration logic changes
- Build confidence scores for each `science_id` based on historical hit-rate
- Scale to 1,000+ cases across all sciences (SBC, BPHS, Longevity, KP, Mundane, etc.)

**It does not predict the future. It validates that the engine correctly reads the past.**

---

## 2. MongoDB Collection: `ke_test_vectors`

### Schema

```json
{
  "_id": "sbc-tv-pm-001",

  "science_id": "sbc",
  "vector_type": "historical_validation",
  "module": "sbc_individual_forecasting",

  "source": {
    "book": "Sarvato Bhadra Chakra V2",
    "chapter": 19,
    "subject_class": "prime_ministers_india",
    "case_ref": "PM-001",
    "page_ref": "49"
  },

  "subject": {
    "name": "Jawaharlal Nehru",
    "birth_date": "1889-11-14",
    "birth_time": "23:36:00",
    "birth_lat": 25.4358,
    "birth_lon": 81.8464,
    "birth_tz": "Asia/Kolkata",
    "birth_place_label": "Allahabad, India"
  },

  "sbc_state_at_event": {
    "transit_date": "1964-05-27",
    "transit_time": "14:00:00",
    "transit_lat": 28.6139,
    "transit_lon": 77.2090,
    "transit_tz": "Asia/Kolkata",
    "transit_place_label": "New Delhi, India",
    "vedha_active": [],
    "panchaka_score": {},
    "rules_expected_to_fire": ["sbc-ch02-014", "sbc-ch10-020"]
  },

  "expected_output": {
    "event_type": "death",
    "claim_axis": "mortality",
    "claim_polarity": "negative",
    "severity": "terminal",
    "threshold_rule": "5-malefic-saturation"
  },

  "actual_outcome": {
    "event": "Death in office -- cardiac arrest",
    "date": "1964-05-27",
    "verified": true,
    "source": "Historical record"
  },

  "validation_result": {
    "status": "pending",
    "engine_output": null,
    "rules_fired": [],
    "pass": null,
    "confidence_delta": null,
    "run_timestamp": null,
    "notes": null
  },

  "tags": ["mortality", "elevation", "political", "PM-india"],
  "approval_status": "pending_human_review",
  "created": "2026-05-20",
  "last_run": null
}
```

### Key Schema Design Decisions

| Decision | Rationale |
|---|---|
| `birth_lat` / `birth_lon` / `birth_tz` stored as numbers | Direct coordinates -- no geocoding API call at runtime |
| `transit_lat` / `transit_lon` in `sbc_state_at_event` | Event location matters (person born in India may die in London -- changes transit houses) |
| `rules_expected_to_fire` | Pre-populated from decode -- allows targeted rule-level pass/fail |
| `confidence_delta` | Tracks by how much engine score diverged from expected -- not just binary pass/fail |
| `science_id` field | Collection is science-agnostic -- same schema handles SBC, BPHS, Longevity, KP, Mundane |

---

## 3. Pipeline Architecture

### 3a. Test Runner Flow

```
Step 1 -- Load vector from ke_test_vectors (filter by science_id, status: pending)
    │
Step 2 -- Reconstruct birth chart
    │     → Call vedic_calculator.py with subject birth_date/time/lat/lon
    │     → Returns: planetary positions, house cusps, nakshatra, dasha
    │
Step 3 -- Compute SBC grid state at event date
    │     → Call panchang_router.py for transit_date planetary positions
    │     → Overlay onto SBC grid (28-star coordinate matrix)
    │     → Identify active Vedha intersections + Panchaka scores
    │
Step 4 -- Run rule matching
    │     → Query interpretation_rules WHERE science_id = vector.science_id
    │     → Fire all matching rules against computed state
    │     → Collect: rule IDs fired, claim_axis, claim_polarity, severity
    │
Step 5 -- Compare output vs expected
    │     → Match event_type, claim_axis, claim_polarity
    │     → Check rules_expected_to_fire ⊆ rules_fired
    │     → Compute confidence_delta
    │
Step 6 -- Write validation_result back to ke_test_vectors document
          → pass: true / false / partial
          → confidence_delta: float
          → run_timestamp: now()
```

### 3b. Result States

| Status | Meaning |
|---|---|
| `pass` | Engine output matches expected_output on all fields |
| `partial` | claim_axis and polarity match; specific rules differ |
| `fail` | Output contradicts expected (wrong polarity or event_type) |
| `miss` | Engine produced no output (no rules fired) |
| `pending` | Not yet run |

---

## 4. Scope A -- SBC Engine Test (Ch 19, 45 PM Cases)

### What gets extracted from Ch 19

- 45 Prime Minister of India birth charts
- Each PM: birth data (date/time/place), event data (elevation to PM, death, major political events)
- SBC grid state at each event date
- Rules expected to fire (from Ch 19's validation narrative)
- Actual historical outcome

### Codex Commission (Ch 19 decode → test vectors)

The decode thread re-reads Ch 19 and produces:
- 45 JSON documents in `ke_test_vectors` schema
- One ingest script: `seed_sbc_test_vectors_ch19.py`
- Covers: elevation events, mortality events, political crisis events

### Acceptance Criteria

- [ ] All 45 PM cases extracted with complete birth data (lat/lon resolved)
- [ ] `rules_expected_to_fire` populated per case from Ch 19 narrative
- [ ] `actual_outcome` verified against historical record
- [ ] Ingest script seeds to `horoscope_db.ke_test_vectors`
- [ ] Engine hits ≥ 70% pass rate on Ch 19 cases when run post-ingest

---

## 5. Scope B -- Universal Framework (All Modules + Reports)

### Extended science coverage

| Science | Vector Source | Planned Cases |
|---|---|---|
| `sbc` | Ch 19 PM cases + future cases | 45 now + scaling |
| `bphs` | Historical charts with known outcomes | TBD |
| `longevity` | Ch 25-58 benchmark case studies (38 charts) | 38 now + scaling |
| `kp` | KP case studies from books | TBD |
| `mundane_jyotish` | Historical geopolitical events | TBD |
| `sbc_macro` | Historical market / geopolitical events | TBD |

### Additional vector_types beyond historical_validation

| `vector_type` | Purpose |
|---|---|
| `historical_validation` | Known historical event -- was it predicted correctly? |
| `regression_gate` | Engine must NOT change output after a code change |
| `boundary_condition` | Edge case -- tests rule priority, veto, override logic |
| `contradiction_probe` | Tests arbitration runtime when two rules conflict |
| `null_case` | No event should fire -- tests false-positive rate |

### Report-level test vectors

For premium report validation (not just rule-level):
```json
{
  "vector_type": "report_output",
  "science_id": "longevity",
  "expected_output": {
    "aayu_bucket": "Madhya",
    "range_years": "32-66",
    "gate_1_trigger": "8th CSL links 8th house"
  }
}
```

---

## 6. New MongoDB Collections Required

| Collection | Purpose | When Created |
|---|---|---|
| `ke_test_vectors` | All test cases across all sciences | Codex commission -- seed script |
| `ke_validation_runs` | Log of each pipeline run (timestamp, pass rate, deltas) | Codex commission -- runner script |

---

## 7. Open Points for TT Decision

| # | Question | Default if no decision |
|---|---|---|
| TV-OP-1 | Minimum pass rate threshold before a science is marked "validated"? (GAI suggested 70%) | 70% |
| TV-OP-2 | Should partial matches count as 0.5 in the pass-rate calculation? | Yes |
| TV-OP-3 | When engine fails a test vector -- auto-flag the rule for NLM review, or just log? | Log only |
| TV-OP-4 | Ch 19 PM cases: include living PMs or only historical (deceased)? | Historical only |
| TV-OP-5 | 1,000+ future cases -- will these come from TT directly as JSON, or via a new decode thread? | TT to confirm source |

---

## 8. Codex Commissions Required

| Commission ID | Scope | Dependency | Status |
|---|---|---|---|
| **KE-TV-1** | Ch 19 decode → 45 PM test vectors + ingest script | KE freeze must lift | READY TO BRIEF (pending TT approval of this spec) |
| **KE-TV-2** | Test runner script + validation_runs logger | KE-TV-1 delivered | After KE-TV-1 |
| **KE-TV-3** | Longevity Ch 25-35 case studies → test vectors (38 charts) | KE-TV-2 | Phase 2 |
| **KE-TV-4** | Universal framework extension (BPHS, KP, Mundane) | KE-TV-2 | Phase 3 |

---

## 9. What TT Needs to Decide Before Commission is Issued

1. **Approve this spec** (or flag changes)
2. **Confirm pass-rate threshold** (TV-OP-1)
3. **Confirm source for 1,000+ future cases** (TV-OP-5) -- will TT provide structured data or is a new decode thread needed?
4. **Confirm scope of Ch 19** -- all 45 cases, or a subset first?
