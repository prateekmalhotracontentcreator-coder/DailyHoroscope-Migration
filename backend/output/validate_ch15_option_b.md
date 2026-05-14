# Knowledge Engine Validation Report
Generated: 2026-04-14 09:31 UTC

## Summary

| Status | Count | % |
|---|---|---|
| auto_approved | 247 | 40% |
| flagged | 210 | 34% |
| pending_human_review | 115 | 18% |
| rejected | 50 | 8% |
| **Total** | **622** | |

## Contradictions Detected

- `R-ATEXTB-SUN-8H-OWN-V-008-03` <-> `R-ATEXTB-SUN-8H-EXA-V-008-02`: Rule 008-03 states Sun in 8H own sign gives both long life AND barrenness, while Rule 008-02 states Sun in 8H own sign gives long life only, creating internal inconsistency about the same placement.
- `R-ATEXTB-MOO-7H-CAN-V-018-02` <-> `R-ATEXTB-MOO-7H-AQU-V-018-01`: Rule 018-02 states Moon in 7H in signs other than Taurus and Cancer causes 'loss of married life', while Rule 018-01 states Moon in 7H in Aquarius causes 'early marriage' -- opposite outcomes for the same placement.
- `R-ATEXTB-MOO-7H-CAN-V-018-02` <-> `R-ATEXTB-MOO-7H-PIS-V-018-03`: Rule 018-02 states Moon in 7H in signs other than Taurus and Cancer causes 'loss of married life', while Rule 018-03 states Moon in 7H in Pisces causes 'early marriage' -- opposite outcomes for the same placement.
- `R-ATEXTB-MOO-7H-CAN-V-018-02` <-> `R-ATEXTB-MOO-7H-SAG-V-018-04`: Rule 018-02 states Moon in 7H in signs other than Taurus and Cancer causes 'loss of married life', while Rule 018-04 states Moon in 7H in Sagittarius causes 'early marriage' -- opposite outcomes for the same placement.
- `R-ATEXTB-MAR-1H-SCO-V-024-06` <-> `R-ATEXTB-MAR-1H-SCO-V-024-06`: Mars in Scorpio in House 1 simultaneously causes spouse to suffer AND produces healthy, long-lived, famous results with benefic outcomes.
- `R-ATEXTB-MAR-7H-ARI-V-030-01` <-> `R-ATEXTB-MAR-7H-SCO-V-030-05`: Both rules claim Mars in 7H Aries/Scorpio gives marital happiness AND vaginal disease simultaneously, which are contradictory outcomes for the same planetary placement.
- `R-ATEXTB-JUP-7H-EXA-V-054-06` <-> `R-ATEXTB-JUP-7H-OWN-V-054-07`: Rule 054-06 states exalted Jupiter in 7H gives knowledge of religions and salvation, while rule 054-07 states exalted or own sign Jupiter in 7H is definitely corrupt--opposite moral outcomes for the same exalted condition.
- `R-ATEXTB-JUP-12H-DEB-V-058-01` <-> `R-ATEXTB-JUP-12H-DEB-V-058-01`: Within the same rule, debilitated Jupiter in 12th house is stated to produce both 'very wealthy' and 'devoid of wealth' outcomes.
- `R-ATEXTB-VEN-1H-EXA-V-059-10` <-> `R-ATEXTB-VEN-1H-OWN-V-059-11`: R-ATEXTB-VEN-1H-EXA-V-059-10 states Venus exalted in House 1 gives 'not very beautiful', while R-ATEXTB-VEN-1H-OWN-V-059-11 states Venus in own sign in House 1 gives 'very beautiful' and the detailed text also mentions 'not very beautiful' for exalted Venus, creating internal inconsistency about beauty outcomes.
- `R-ATEXTB-VEN-7H-SCO-V-065-05` <-> `R-ATEXTB-VEN-7H-SCO-V-065-05`: Venus in 7H Scorpio is stated to make native a 'pleasure seeker' AND cause 'death of wife' - opposite outcomes for identical planetary placement.
- `R-ATEXTB-SAT-1H-VIR-V-071-11` <-> `R-ATEXTB-SAT-1H-ARI-V-071-02`: Saturn in Virgo (1H) is stated to give 'no malefic effects, wealthy, intellectual' AND 'malefic results' simultaneously in the same source text.
- `R-ATEXTB-SAT-1H-CAN-V-071-03` <-> `R-ATEXTB-SAT-1H-ARI-V-071-02`: Saturn in Cancer (1H) is stated to produce both 'malefic results' and 'benefic results, fond of jewellery' in the same source text.
- `R-ATEXTB-SAT-7H-PIS-V-077-05` <-> `R-ATEXTB-SAT-7H-PIS-V-077-05`: Within the same rule for Saturn in 7H Pisces: 'two marriages' contradicts 'death of spouse' as mutually exclusive outcomes.
- `R-ATEXTB-SAT-7H-SAG-V-077-06` <-> `R-ATEXTB-SAT-7H-SAG-V-077-06`: Within the same rule for Saturn in 7H Sagittarius: 'two marriages' contradicts 'sexual' (interpreted as sexual dysfunction/impotence) as incompatible marital outcomes.
- `R-ATEXTB-KET-1H-GEM-V-094-05` <-> `R-ATEXTB-KET-1H-VIR-V-094-11`: Ketu in Gemini is stated to cause both 'short life, poor' and 'very happy' with 'all comforts', which are directly opposite outcomes.
- `R-ATEXTB-KET-1H-SCO-V-094-09` <-> `R-ATEXTB-KET-1H-VIR-V-094-11`: Ketu in Scorpio is stated to make one 'wealthy, happy, hard working' but also causes 'stomach ailments', which contradicts the positive health/prosperity claim.
- `R-ATEXTB-KET-1H-SAG-V-094-08` <-> `R-ATEXTB-KET-1H-LEO-V-094-06`: Ketu in Sagittarius is stated to give 'more gains' but also causes 'loss of wealth and father at the age of 12', which directly contradicts the gains claim.
- `R-ATEXTB-KET-7H-CAN-V-099-01` <-> `R-ATEXTB-KET-7H-SCO-V-099-03`: Rule 1 states Ketu in Cancer gives gains, while Rule 3 states Ketu in Scorpio causes opposition from husband, widow status, danger, and loss in profession--directly opposite outcomes for the same planet in the same house across different signs.

## Flagged Rules (first 20)

| rule_id | book | reason |
|---|---|---|
| R-ATEXTB-SUN-1H-ARI-V-001-01 | A Text Book of Astrology | Rule condition specifies Aries only, but summary/detailed text references three signs (Cancer, Aries, Leo) with different outcomes; rule should be split or condition clarified. |
| R-ATEXTB-SUN-1H-CAN-V-001-02 | A Text Book of Astrology | Rule condition specifies Cancer only, but summary/detailed text references three signs (Cancer, Aries, Leo) with different outcomes; rule should be split or condition clarified. |
| R-ATEXTB-SUN-1H-LEO-V-001-03 | A Text Book of Astrology | Rule condition specifies Leo only, but summary/detailed text references three signs (Cancer, Aries, Leo) with different outcomes; rule should be split or condition clarified. |
| R-ATEXTB-SUN-1H-PIS-V-001-04 | A Text Book of Astrology | Rule condition specifies Pisces only, but summary/detailed text references two signs (Scorpio, Pisces); rule should be split or condition clarified. |
| R-ATEXTB-SUN-1H-SCO-V-001-05 | A Text Book of Astrology | Rule condition specifies Scorpio only, but summary/detailed text references two signs (Scorpio, Pisces); rule should be split or condition clarified. |
| R-ATEXTB-SUN-2H-AQU-V-002-01 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-ARI-V-002-02 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-CAN-V-002-03 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-CAP-V-002-04 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-LEO-V-002-05 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-LIB-V-002-06 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-PIS-V-002-07 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-SAG-V-002-08 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-2H-SCO-V-002-09 | A Text Book of Astrology | Placeholder text with no actual interpretation content; not suitable for production use. |
| R-ATEXTB-SUN-3H-V-003 | A Text Book of Astrology | Detailed text is truncated mid-sentence ('having number of disc') making it incomplete and unusable. |
| R-ATEXTB-SUN-4H-V-004 | A Text Book of Astrology | Detailed text is truncated mid-sentence ('Have sexual relations with n') making it incomplete and incoherent. |
| R-ATEXTB-SUN-5H-V-005 | A Text Book of Astrology | Detailed text is truncated mid-sentence ('Devotee of L') making it incomplete and unusable. |
| R-ATEXTB-SUN-6H-V-006 | A Text Book of Astrology | Detailed text is truncated mid-sentence ('Teeth get damag') making it incomplete and unusable. |
| R-ATEXTB-SUN-6H-AQU-V-006-01 | A Text Book of Astrology | Condition specifies Aquarius only, but summary/detailed text lists 'Taurus, Scorpio or Aquarius' -- mismatch between condition and interpretation scope. |
| R-ATEXTB-SUN-6H-CAN-V-006-02 | A Text Book of Astrology | Condition specifies Cancer only, but summary/detailed text lists 'Cancer, Libra and Capricorn' -- mismatch between condition and interpretation scope. |

## Rejected Rules (structural failures)

| rule_id | reason |
|---|---|
| R-ATEXTB-SUN-3H-DEB-V-003-01 | interpretation_too_short |
| R-ATEXTB-SUN-7H-EXA-V-007-04 | interpretation_too_short |
| R-ATEXTB-SUN-10H-DEB-V-010-05 | interpretation_too_short |
| R-ATEXTB-MOO-1H-LIB-V-013-06 | interpretation_too_short |
| R-ATEXTB-MOO-1H-EXA-V-013-11 | interpretation_too_short |
| R-ATEXTB-MOO-2H-TAU-V-014-05 | interpretation_too_short |
| R-ATEXTB-MOO-2H-DEB-V-014-06 | interpretation_too_short |
| R-ATEXTB-MOO-3H-DEB-V-015-01 | interpretation_too_short |
| R-ATEXTB-MOO-3H-EXA-V-015-02 | interpretation_too_short |
| R-ATEXTB-MOO-6H-DEB-V-017-08 | interpretation_too_short |
| R-ATEXTB-MOO-6H-EXA-V-017-09 | interpretation_too_short |
| R-ATEXTB-MOO-10H-EXA-V-021-06 | interpretation_too_short |
| R-ATEXTB-MAR-2H-SCO-V-025-01 | interpretation_too_short |
| R-ATEXTB-MAR-2H-DEB-V-025-03 | interpretation_too_short |
| R-ATEXTB-MAR-4H-LIB-V-027-05 | interpretation_too_short |
| R-ATEXTB-MAR-7H-PIS-V-030-04 | interpretation_too_short |
| R-ATEXTB-MAR-9H-EXA-V-032-10 | interpretation_too_short |
| R-ATEXTB-MER-4H-PIS-V-039-01 | interpretation_too_short |
| R-ATEXTB-MER-5H-CAN-V-040-01 | interpretation_too_short |
| R-ATEXTB-MER-5H-VIR-V-040-03 | interpretation_too_short |
| R-ATEXTB-MER-7H-PIS-V-042-02 | interpretation_too_short |
| R-ATEXTB-MER-7H-VIR-V-042-04 | interpretation_too_short |
| R-ATEXTB-MER-10H-VIR-V-045-01 | interpretation_too_short |
| R-ATEXTB-JUP-1H-EXA-V-048-10 | interpretation_too_short |
| R-ATEXTB-JUP-3H-GEM-V-050-05 | interpretation_too_short |
| R-ATEXTB-JUP-4H-TAU-V-051-02 | interpretation_too_short |
| R-ATEXTB-JUP-4H-EXA-V-051-03 | interpretation_too_short |
| R-ATEXTB-JUP-9H-EXA-V-055-12 | interpretation_too_short |
| R-ATEXTB-JUP-11H-DEB-V-057-02 | interpretation_too_short |
| R-ATEXTB-JUP-12H-EXA-V-058-03 | interpretation_too_short |
| R-ATEXTB-VEN-6H-EXA-V-064-03 | interpretation_too_short |
| R-ATEXTB-VEN-7H-LEO-V-065-04 | interpretation_too_short |
| R-ATEXTB-VEN-9H-CAP-V-067-01 | interpretation_too_short |
| R-ATEXTB-VEN-9H-TAU-V-067-02 | interpretation_too_short |
| R-ATEXTB-VEN-11H-LEO-V-069-01 | interpretation_too_short |
| R-ATEXTB-VEN-12H-LIB-V-070-01 | interpretation_too_short |
| R-ATEXTB-SAT-3H-V-073 | truncated_text |
| R-ATEXTB-SAT-3H-ARI-V-073-02 | interpretation_too_short |
| R-ATEXTB-SAT-4H-ARI-V-074-01 | interpretation_too_short |
| R-ATEXTB-SAT-6H-EXA-V-076-10 | interpretation_too_short |
| R-ATEXTB-SAT-8H-EXA-V-078-03 | interpretation_too_short |
| R-ATEXTB-SAT-10H-PIS-V-080-01 | interpretation_too_short |
| R-ATEXTB-SAT-12H-EXA-V-081-01 | interpretation_too_short |
| R-ATEXTB-RAH-2H-LIB-V-083-01 | interpretation_too_short |
| R-ATEXTB-RAH-3H-DEB-V-084-05 | interpretation_too_short |
| R-ATEXTB-KET-3H-PIS-V-095-02 | interpretation_too_short |
| R-ATEXTB-KET-3H-OWN-V-095-05 | interpretation_too_short |
| R-ATEXTB-KET-9H-SAG-V-101-03 | interpretation_too_short |
| R-ATEXTB-KET-11H-V-103 | truncated_text |
| R-ATEXTB-KET-11H-SAG-V-103-02 | interpretation_too_short |
