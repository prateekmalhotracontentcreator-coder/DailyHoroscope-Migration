#!/usr/bin/env python3
"""
patch_mundane_v1_flags.py
=========================
Post-validation patch for the mundane_jyotish interpretation rules.

Fixes two categories of validator artefacts from the v19 validation run:

  A) 35 false-flagged rules:
     Rules that Claude Haiku incorrectly flagged as problematic.
     Patched from  approval_status='flagged'  →  'pending_human_review'
     with a typed patch_reason added to review_notes.

  B) 10 false contradiction pairs (across 5 sub_types):
     Complementary rule pairs where mutually-exclusive conditions were
     misread as contradictions (e.g. Fixed+Fixed vs Moving+Moving Jaimini).
     Already at pending_human_review; patch adds resolution note so
     human reviewers know the contradiction was a false positive.

Usage:
    # Dry-run (default) — prints what would change, no writes:
    python3 backend/scripts/patch_mundane_v1_flags.py \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db

    # Apply patch:
    python3 backend/scripts/patch_mundane_v1_flags.py \\
        --mongo-url "$MONGO_URL" --db-name horoscope_db --patch

Generated: 2026-05-07
"""

import argparse
import sys
from datetime import datetime, timezone

from pymongo import MongoClient

# ── Patch timestamp ───────────────────────────────────────────────────────────
_NOW = datetime.now(timezone.utc).isoformat()

# ── A) False-flag rule registry ───────────────────────────────────────────────
# Each entry: (rule_id, patch_reason_code, human_note)
#
# Reason codes
#   truncated_result_validator_bug   — validator sent only 400 chars to Claude;
#                                      result appeared truncated but is complete in DB
#   complementary_condition_pair     — rule is one side of a mutually-exclusive
#                                      condition pair; valid by design
#   non_standard_terminology         — Claude flagged non-classical terminology but
#                                      source text uses same terms; stylistic, not factual
#   extraordinary_claim_no_citation  — AI over-applied scepticism; rule has source
#                                      chapter citation; classical basis exists
#   internal_logic_misread           — AI misread multi-clause condition as contradiction;
#                                      condition is internally consistent
#   absolute_claim_reviewer_bias     — AI disliked strong/absolute phrasing; classical
#                                      mundane texts routinely use absolute language
#   copy_paste_error_fixed           — condition had a copy-paste error; fixed in ingest
#                                      script and re-upserted; flag no longer applies

FALSE_FLAGS: list[tuple[str, str, str]] = [

    # ── Raphael truncation false flags ([:400] validator bug) ─────────────────
    (
        "mundane-raphael-ch8-malefic-1st-national-troubles",
        "truncated_result_validator_bug",
        "Result text was complete in DB; validator [:400] clip made it appear truncated to Claude. "
        "Full text confirmed in ingest script. No factual issue."
    ),
    (
        "mundane-raphael-ch26-eclipse-on-meridian-nadir-earthquake",
        "truncated_result_validator_bug",
        "Result text was complete in DB; validator [:400] clip made it appear truncated to Claude. "
        "Full text confirmed in ingest script. No factual issue."
    ),
    (
        "mundane-raphael-ch27-comet-sign-type-effects",
        "truncated_result_validator_bug",
        "Result text was complete in DB; validator [:400] clip made it appear truncated to Claude. "
        "Full text confirmed in ingest script. No factual issue."
    ),
    (
        "mundane-raphael-ch28-mars-transit-country-sign-fires",
        "truncated_result_validator_bug",
        "Result text was complete in DB; validator [:400] clip made it appear truncated to Claude. "
        "Full text confirmed in ingest script. No factual issue."
    ),
    (
        "mehta-ch7-koorma-triple-directional-audit",
        "truncated_result_validator_bug",
        "Condition text was complete in DB; validator [:400] clip truncated the directional mapping "
        "mid-sentence. Full directional table confirmed in ingest script. No factual issue."
    ),

    # ── Gaur Chapter 1 — Samvatsar rules ─────────────────────────────────────
    (
        "gaur-ch1-samvatsar-ketu-lord-plentiful-rains-loose-morals",
        "non_standard_terminology",
        "Parabhav Samvatsar (#40) placement in Ketu-lord group follows Gaur Ch1 source text directly. "
        "Classical grouping varies by commentary tradition; Gaur's grouping is internally consistent."
    ),
    (
        "gaur-ch1-samvatsar-venus-year-earthquake-calamity-specific",
        "non_standard_terminology",
        "Shobhan Samvatsar listing follows Gaur Ch1 source text numbering. "
        "Minor numbering variation exists across Samvatsar traditions; Gaur uses his own canonical list. "
        "Faithfully transcribed from source chapter — human reviewer to verify against original text."
    ),

    # ── Gaur Chapter 10 — Ingress/Transit rules ───────────────────────────────
    (
        "gaur-ch10-45-muhurti-ingress-overrides-drought",
        "absolute_claim_reviewer_bias",
        "Classical mundane texts routinely use absolute override language for strong configurations. "
        "Gaur Ch10 states this condition directly; faithfully transcribed. "
        "Co-founder to verify exact phrasing against original."
    ),
    (
        "gaur-ch10-jupiter-cancer-sun-aspect-supremacy",
        "non_standard_terminology",
        "Conjunction listed alongside trine follows Gaur Ch10 source usage where 'aspect' includes "
        "conjunction in the classical Indian sense (drishti can include conjunction in some texts). "
        "Faithfully transcribed from source; terminology note added for human reviewer."
    ),
    (
        "gaur-ch10-mars-12th-lord-afflicted-military-insubordination",
        "extraordinary_claim_no_citation",
        "Natal-transit conflation follows Gaur Ch10 methodology where yearly chart Mars as 12th lord "
        "is assessed by transit affliction. Non-standard in Western mundane but valid Jyotish approach. "
        "Source chapter cited; human reviewer to confirm methodology against original."
    ),
    (
        "gaur-ch10-mercury-retrograde-gemini-education-scandal",
        "internal_logic_misread",
        "The two outcomes (cheap vegetables + education scandal) both derive from Mercury retrograde "
        "weakening Gemini's significations simultaneously. Classical texts often list multiple domain "
        "effects for a single planetary condition; not logically contradictory."
    ),
    (
        "gaur-ch10-saturn-retrograde-uttarashadh-poorvashadh-famine",
        "extraordinary_claim_no_citation",
        "12-year duration and Rohini Gate comparison are cited from Gaur Ch10. Duration claims are "
        "extraordinary but faithfully transcribed from source. Human reviewer to verify against "
        "original text before promoting to approved."
    ),

    # ── Gaur Chapter 8 ────────────────────────────────────────────────────────
    (
        "gaur-ch8-gold-reserve-banking-crisis-veto",
        "non_standard_terminology",
        "Sanghatta Vedha grid usage follows Gaur Ch8 terminology; 'Sanghatta grid' is Gaur's own "
        "framework term, not standard AIFAS terminology. Faithfully transcribed from source. "
        "No factual error — terminological variation only."
    ),

    # ── Mehta Chapter 2 ───────────────────────────────────────────────────────
    (
        "mehta-ch2-mars-retrograde-jyeshtha-anuradha-fall-of-kings",
        "non_standard_terminology",
        "Retrograde-to-direct transition across Jyeshtha→Anuradha in reverse order is geometrically "
        "possible during retrograde motion (backward traversal). Mehta Ch2 explicitly describes this "
        "motion pattern. No error — AI misunderstood retrograde direction."
    ),
    (
        "mehta-ch2-sat-jup-conjunction-us-president-mortality",
        "extraordinary_claim_no_citation",
        "Historical pattern (1840-1960 presidential deaths) is accurately cited in Mehta Ch2. "
        "Pattern is a statistical observation in source text, not a universal claim. "
        "Faithfully transcribed; human reviewer to verify historical accuracy against Mehta original."
    ),

    # ── Mehta Chapter 10 ─────────────────────────────────────────────────────
    (
        "mehta-ch10-saturn-jupiter-us-president-mortality-veto",
        "complementary_condition_pair",
        "This is the veto/exception rule paired with mehta-ch2-sat-jup-conjunction-us-president-mortality. "
        "The condition (afflicted Saturn-Jupiter) explicitly inverts the base rule. "
        "Complementary pair by design — not a standalone contradiction."
    ),

    # ── Gaur Chapter 6 ────────────────────────────────────────────────────────
    (
        "mundane-gaur-ch6-mars-venus-jupiter-catastrophic",
        "internal_logic_misread",
        "The two 7th-house relationships (Mars from Venus AND Jupiter from Saturn) are conjunctive "
        "conditions — both must be present simultaneously. AI read them as independent triggers. "
        "AND-logic is explicit in source condition text."
    ),
    (
        "mundane-gaur-ch6-trinadi-no-rain-veto",
        "complementary_condition_pair",
        "Malefics in Patal Nadi AND benefics in Heaven Nadi describes a specific dual-axis alignment "
        "in the Trinadi system. This is one distinct configuration, not two opposing rules. "
        "AI misread the conjunctive condition as a contradiction with the complementary Trinadi rule."
    ),

    # ── Gaur Chapter 8 ────────────────────────────────────────────────────────
    (
        "mundane-gaur-ch8-gold-silver-bullion-gate",
        "internal_logic_misread",
        "Nakshatra ownership and planetary Sun-sign ownership are two parallel assessment systems "
        "applied conjunctively in Gaur Ch8. Using both systems together is Gaur's own methodology; "
        "AI flagged the dual-system approach as logically inconsistent, which it is not."
    ),

    # ── Gaur Chapter 9 ────────────────────────────────────────────────────────
    (
        "mundane-gaur-ch9-sarvatobhadra-currency-spike",
        "internal_logic_misread",
        "Three OR-linked triggers (Saturn in Dhanishtha / Rahu in Dhanishtha / Mars Vedha on Krittika) "
        "are independently sufficient conditions, not required simultaneously. OR-logic in classical "
        "texts is common. AI incorrectly required logical linkage between disjunct triggers."
    ),

    # ── Gopal Chapter 3 ───────────────────────────────────────────────────────
    (
        "mundane-gopal-ch3-widow-pm-multiplier",
        "extraordinary_claim_no_citation",
        "The +0.2 multiplier reflects Gopal Ch3's statistical pattern observation across Indian PMs. "
        "Gopal applies this as an empirical weighting, not a classical Vedic doctrine claim. "
        "Human reviewer to verify weighting rationale against original Gopal text."
    ),

    # ── Gopal Chapter 4 ───────────────────────────────────────────────────────
    (
        "mundane-gopal-ch4-indian-pm-widowhood-rule",
        "extraordinary_claim_no_citation",
        "Saturn as 10th lord + marital-status correlation is Gopal Ch4's empirical observation "
        "from historical Indian PM data. Presented as pattern, not universal doctrine. "
        "Human reviewer to confirm against Gopal original."
    ),

    # ── Gopal Chapter 5 ───────────────────────────────────────────────────────
    (
        "mundane-gopal-ch5-hora-lagna-fixed-veto",
        "absolute_claim_reviewer_bias",
        "0.10 survival coefficient for double-fixed Lagna+Hora Lagna is Gopal Ch5's explicit scoring. "
        "Severe survival coefficient reflects Gopal's own empirical calibration, not validator invention. "
        "Extraordinary claim — human reviewer to verify coefficient against original Gopal text."
    ),

    # ── Gopal Chapter 14 ─────────────────────────────────────────────────────
    (
        "mundane-gopal-ch14-mars-perigee-south-cm",
        "extraordinary_claim_no_citation",
        "Mars perigee + Fixed Sign → South India leadership pattern is Gopal Ch14's regional "
        "calibration. Gopal applies directional specificity to planetary phenomena; regional "
        "scope is explicit in source. Human reviewer to verify against Gopal Ch14 original."
    ),
    (
        "mundane-gopal-ch14-mars-proximity-children",
        "extraordinary_claim_no_citation",
        "Mars proximity (60M km threshold) → child casualty risk is Gopal Ch14's extraordinary claim. "
        "Faithfully transcribed from source. Requires co-founder review before promotion to approved; "
        "kept at pending_human_review for that reason."
    ),
    (
        "mundane-gopal-ch14-regional-direction-leadership",
        "non_standard_terminology",
        "Directional mapping (Sun→East, Venus→SE, Mars→South, etc.) follows Gopal Ch14's own "
        "directional system, which differs from some classical schemes. Gopal's scheme is internally "
        "consistent and cited from source. Non-standard vs generic classical, not incorrect."
    ),
    (
        "mundane-gopal-ch14-saturn-3rd-it-backbone",
        "extraordinary_claim_no_citation",
        "Saturn in 3rd → IT/BPO expansion is Gopal Ch14's modern calibration (communications house). "
        "Saturn's delay/contraction does apply to 3rd house but Gopal's empirical IT-sector result "
        "is his own modern interpretation. Human reviewer to verify calibration rationale."
    ),
    (
        "mundane-gopal-ch14-saturn-leo-real-estate",
        "extraordinary_claim_no_citation",
        "Saturn in Leo → 100% property gains is Gopal Ch14's counter-intuitive empirical finding "
        "from Indian real-estate cycles. Extraordinary claim faithfully transcribed; human reviewer "
        "to verify pattern basis against Gopal original before promotion to approved."
    ),
    (
        "mundane-gopal-ch14-saturn-pushya-bull-run",
        "extraordinary_claim_no_citation",
        "Saturn in Pushya → 50–100% stock index growth is Gopal Ch14's empirical market-cycle finding. "
        "Counter-intuitive (Saturn restrictive) but Gopal's own observation from historical data. "
        "Human reviewer to verify against Gopal Ch14 before promotion to approved."
    ),

    # ── Mehta Chapter 18 ─────────────────────────────────────────────────────
    (
        "mundane-mehta-ch18-8th-house-vacancy-rule",
        "internal_logic_misread",
        "The rule states 8th MUST be empty for primary result, then discusses the modified outcome "
        "when malefics vs benefics are present as a secondary exception clause. This is a conditional "
        "structure (base rule + exception), not a self-contradiction."
    ),
    (
        "mundane-mehta-ch18-sandhi-bharani-lethality",
        "extraordinary_claim_no_citation",
        "Bharani's Yama association (god of death) is classical — Bharani is ruled by Yama in "
        "nakshatra mythology (presiding deity, not planetary lord). Mehta Ch18 uses 'Yama-associated' "
        "correctly in mythological sense. AI confused planetary lord with presiding deity."
    ),
    (
        "mundane-mehta-ch18-simha-moon-rahu-dasha",
        "non_standard_terminology",
        "Mehta Ch18 nakshatra grouping for Simhasan follows his own classification system. "
        "Not all classical systems agree on nakshatra groupings; Mehta's grouping is internally "
        "consistent within his framework. Human reviewer to verify against Mehta Ch18 original."
    ),
    (
        "mundane-mehta-ch18-simhasan-martial-king",
        "non_standard_terminology",
        "Simhasan nakshatra list (Mrigshira/Chitra/Dhanishtha) follows Mehta Ch18's own grouping. "
        "Planetary lords differ by classification tradition; Mehta uses his own scheme. "
        "Human reviewer to verify against Mehta Ch18 original."
    ),
    (
        "mundane-mehta-ch18-simhasan-moon-absolute-power",
        "non_standard_terminology",
        "Claim of 'all Mars-governed' for Simhasan nakshatras is Mehta Ch18's own classification. "
        "Factual accuracy vs standard schemes is a source-fidelity question, not a validator finding. "
        "Human reviewer to verify nakshatra lord scheme against Mehta Ch18 original."
    ),

    # ── Mehta Chapter 22 ─────────────────────────────────────────────────────
    (
        "mundane-mehta-ch22-jupiter-raja-golden-year",
        "copy_paste_error_fixed",
        "Condition originally read 'IF Mars is the Raja' — copy-paste error from Mars-Raja rule. "
        "Fixed in ingest_mundane_interpretation_v19.py and re-upserted to MongoDB. "
        "Condition now correctly reads 'IF Jupiter is the Raja for the year'. Flag resolved."
    ),
    (
        "mundane-mehta-ch22-raja-mantri-enemy-deadlock",
        "non_standard_terminology",
        "Planetary enemy pairings (Sun-Saturn, Moon-Rahu, etc.) follow Mehta Ch22's own enemy "
        "classification. Classical enemy tables vary by text; Mehta's list is his own system. "
        "Human reviewer to verify pairings against Mehta Ch22 original."
    ),
]

# Verify count
assert len(FALSE_FLAGS) == 36, f"Expected 36 false flags, got {len(FALSE_FLAGS)}"

# ── B) False contradiction pairs — sub_types affected ────────────────────────
# These rules were downgraded from 'approve' → 'spot_check' (pending_human_review)
# by the contradiction detector. The pairs have mutually-exclusive conditions
# by design — not genuine contradictions.
# The rules are already at pending_human_review; we just add a resolution note.

FALSE_CONTRADICTION_SUB_TYPES = {
    "eclipse": (
        "2 apparent contradiction pair(s) detected by validator. "
        "Pairs have mutually-exclusive conditions (e.g. solar vs lunar eclipse, "
        "different degree orbs) — complementary by design. Not genuine contradictions."
    ),
    "weather_forecast": (
        "2 apparent contradiction pair(s) detected by validator. "
        "Pairs cover opposite seasonal/moisture conditions — complementary by design. "
        "Not genuine contradictions."
    ),
    "commodity_price_forecast": (
        "2 apparent contradiction pair(s) detected by validator. "
        "Pairs cover bullion-up vs bullion-down configurations — complementary by design. "
        "Not genuine contradictions."
    ),
    "oath_chart_tenure": (
        "2 apparent contradiction pair(s) detected by validator. "
        "Pairs cover auspicious vs inauspicious oath configurations — complementary by design. "
        "Not genuine contradictions."
    ),
    "yearly_governance": (
        "2 apparent contradiction pair(s) detected by validator. "
        "Pairs cover benefic-Raja vs malefic-Raja conditions — complementary by design. "
        "Not genuine contradictions."
    ),
}


# ── Patch logic ───────────────────────────────────────────────────────────────

def patch_false_flags(coll, dry_run: bool) -> tuple[int, int, list[str]]:
    """Patch 35 false-flagged rules to pending_human_review."""
    patched = 0
    skipped = 0
    not_found = []

    for rule_id, reason_code, note in FALSE_FLAGS:
        doc = coll.find_one(
            {"rule_id": rule_id},
            {"approval_status": 1, "review_notes": 1}
        )
        if not doc:
            not_found.append(rule_id)
            print(f"  ⚠  NOT FOUND: {rule_id}")
            continue

        current_status = doc.get("approval_status", "")
        if current_status != "flagged":
            skipped += 1
            print(f"  SKIP  {rule_id:<60}  (status={current_status}, not flagged)")
            continue

        existing_notes = doc.get("review_notes", "") or ""
        new_notes = (
            f"{existing_notes}\n\n"
            f"[PATCH {_NOW}] FALSE FLAG — {reason_code}\n{note}"
        ).strip()

        if not dry_run:
            coll.update_one(
                {"rule_id": rule_id},
                {"$set": {
                    "approval_status": "pending_human_review",
                    "review_notes":    new_notes,
                    "patch_reason":    reason_code,
                    "patched_at":      _NOW,
                }}
            )
            print(f"  PATCH {rule_id:<60}  flagged → pending_human_review  [{reason_code}]")
        else:
            print(f"  [DRY] {rule_id:<60}  flagged → pending_human_review  [{reason_code}]")

        patched += 1

    return patched, skipped, not_found


def patch_false_contradictions(coll, dry_run: bool) -> int:
    """
    Add resolution notes to rules in sub_types that had false contradiction pairs.
    These rules are already at pending_human_review — we only annotate them.
    """
    annotated = 0
    for sub_type, resolution_note in FALSE_CONTRADICTION_SUB_TYPES.items():
        # Find rules in this sub_type that have a contradiction note
        # (validator sets review_notes containing 'contradiction' when downgrading)
        cursor = coll.find(
            {
                "science_id":      "mundane_jyotish",
                "sub_type":        sub_type,
                "approval_status": "pending_human_review",
                "review_notes":    {"$regex": "contradict", "$options": "i"},
            },
            {"rule_id": 1, "review_notes": 1}
        )
        docs = list(cursor)
        if not docs:
            print(f"  sub_type={sub_type:<30}  no contradiction-annotated rules found (may already be clean)")
            continue

        for doc in docs:
            rid = doc["rule_id"]
            existing = doc.get("review_notes", "") or ""
            # Skip if already patched
            if "FALSE CONTRADICTION" in existing:
                print(f"  SKIP  {rid}  (already patched)")
                continue

            new_notes = (
                f"{existing}\n\n"
                f"[PATCH {_NOW}] FALSE CONTRADICTION — {resolution_note}"
            ).strip()

            if not dry_run:
                coll.update_one(
                    {"rule_id": rid},
                    {"$set": {
                        "review_notes":            new_notes,
                        "contradiction_resolved":  True,
                        "patched_at":              _NOW,
                    }}
                )
                print(f"  ANNOTATE {rid:<55}  [false_contradiction / {sub_type}]")
            else:
                print(f"  [DRY] ANNOTATE {rid:<50}  [false_contradiction / {sub_type}]")

            annotated += 1

    return annotated


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        description="Patch mundane_jyotish false flags and false contradiction pairs"
    )
    p.add_argument("--mongo-url", required=True)
    p.add_argument("--db-name",   required=True)
    p.add_argument("--patch",     action="store_true",
                   help="Apply changes (default: dry-run only)")
    return p.parse_args()


def main():
    args   = parse_args()
    dry_run = not args.patch

    client = MongoClient(args.mongo_url)
    try:
        db   = client[args.db_name]
        coll = db["interpretation_rules"]

        mode = "DRY RUN" if dry_run else "LIVE PATCH"
        print(f"\n{'=' * 60}")
        print(f"  MUNDANE V1 PATCH  [{mode}]")
        print(f"{'=' * 60}")

        # ── A: False flags ────────────────────────────────────────
        print(f"\n── A) Patching {len(FALSE_FLAGS)} false-flagged rules ──")
        patched, skipped, not_found = patch_false_flags(coll, dry_run)

        print(f"\n  Patched  : {patched}")
        print(f"  Skipped  : {skipped}  (already at correct status)")
        if not_found:
            print(f"  Not found: {len(not_found)}")
            for r in not_found:
                print(f"    - {r}")

        # ── B: False contradiction pairs ──────────────────────────
        print(f"\n── B) Annotating false contradiction pairs ({len(FALSE_CONTRADICTION_SUB_TYPES)} sub_types) ──")
        annotated = patch_false_contradictions(coll, dry_run)
        print(f"\n  Annotated: {annotated} rule(s)")

        # ── Final counts ──────────────────────────────────────────
        print(f"\n{'=' * 60}")
        print(f"  PATCH COMPLETE  [{mode}]")
        print(f"{'=' * 60}")

        # Show post-patch status breakdown
        pipeline = [
            {"$match": {"science_id": "mundane_jyotish"}},
            {"$group": {"_id": "$approval_status", "count": {"$sum": 1}}},
            {"$sort":  {"count": -1}},
        ]
        results = list(coll.aggregate(pipeline))
        total   = sum(r["count"] for r in results)
        print(f"\n  Post-patch status breakdown (mundane_jyotish):")
        for r in results:
            pct = 100 * r["count"] / total if total else 0
            print(f"    {r['_id']:<30}  {r['count']:>4}  ({pct:.0f}%)")
        print(f"    {'Total':<30}  {total:>4}")

        if dry_run:
            print(f"\n  ℹ️  DRY RUN — no changes written.")
            print(f"  Run with --patch to apply.")

    finally:
        client.close()


if __name__ == "__main__":
    main()
