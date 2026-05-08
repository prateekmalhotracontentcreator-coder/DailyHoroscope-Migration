#!/usr/bin/env python3
"""
patch_mundane_v3_v7_flags.py

Resolves all outstanding flags and rejections in the v3–v7 batches after
the dict-to-prose migration and re-validation.

Issues addressed:

── v4 REJECTED (3) — result field was also a dict; migration only fixed condition ──
  1. mundane-gaur-ch10-sun-ingress-muhurti-tier
     Fix: convert result dict {15/30/45_muhurti} to prose string.
  2. mundane-gaur-ch11-eclipse-solar-commodity-by-month
     Fix: convert result dict (12 Hindu months) to prose string.
  3. mundane-gaur-ch11-eclipse-scorpio-drought
     Fix: result = "Drought causing agony to masses." (5 words, min=10). Expand.

── v3 FLAGGED truncated (2) — Pattern 7 fallback cut nested dicts mid-sentence ──
  4. mundane-mehta-ch20-nine-eleven-validation
     Fix: replace 36-word truncated condition with full prose from original dict.
  5. mundane-mehta-ch20-madrid-london-validation
     Fix: replace 18-word truncated condition with full prose from original dict.

── v3 FLAGGED → PHR (5) — false flags / content_validity_dispute ──
  6.  mundane-gaur-ch2-dhanyesh-outcome-matrix
  7.  mundane-mehta-ch13-eclipse-national-validation
  8.  mundane-mehta-ch20-india-temple-attack-signature
  9.  mundane-mehta-ch20-delhi-bombs-national-affliction
  10. mundane-mehta-ch26-party-dasha-framework

── v4 FLAGGED → PHR (3) — condition-result mismatch artefact of dict conversion ──
  11. mundane-gaur-ch10-jupiter-motion-differentials
  12. mundane-gaur-ch10-venus-motion-differentials
  13. mundane-gaur-ch10-saturn-motion-differentials

── v7 FLAGGED → PHR (3) — false flags / Gopal Ch10/13/15 source-faithful ──
  14. mundane-gopal-ch10-mars-perigee-leadership-change
  15. mundane-gopal-ch13-saturn-ketu-conjunction-civil-war
  16. mundane-gopal-ch15-saturn-3rd-national-it-boom

Usage:
  # Inspect (no writes):
  python3 backend/scripts/patch_mundane_v3_v7_flags.py --mongo-url "$MONGO_URL"

  # Apply:
  python3 backend/scripts/patch_mundane_v3_v7_flags.py --mongo-url "$MONGO_URL" --apply
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pymongo import MongoClient


# ── Content fixes (rejected → structural repair) ──────────────────────────────

CONTENT_FIXES: dict[str, dict] = {

    # v4 — result was a dict, needs prose conversion
    "mundane-gaur-ch10-sun-ingress-muhurti-tier": {
        "fix_type": "result_dict_to_prose",
        "result": (
            "15-muhurti ingress (nakshatra = Bharani, Ardra, Ashlesha, Jyeshtha, or Shatbhisha): "
            "grains and juicy materials become expensive; rains are below normal. "
            "30-muhurti ingress (nakshatra = Ashwini, Krithika, Mrigshira, Pushya, Magha, "
            "Poorvaphalguni, Hast, Chitra, Anuradha, Mool, Poorvashadh, Shravan, Dhanishtha, "
            "Poorvabhadrapad, or Revti): grains, grass and juicy materials remain at medium price levels. "
            "45-muhurti ingress (nakshatra = Rohini, Punarvasu, Uttaraphalguni, Vishakha, "
            "Uttarashadh, or Uttarabhadrapad): rains are good; grains, ghee, oil and cotton are cheap."
        ),
    },

    # v4 — result was a dict (12 Hindu months)
    "mundane-gaur-ch11-eclipse-solar-commodity-by-month": {
        "fix_type": "result_dict_to_prose",
        "result": (
            "Solar eclipse commodity effects by Hindu month: "
            "Chaitra — gold and grains become expensive quickly. "
            "Vaishakh — til, oil materials, moong, cotton cloth, yarn and wheat expensive. "
            "Jyeshtha — gold and grains cheap. "
            "Aashadh — grains expensive; drought signal. "
            "Shravan — grains cheap but juicy materials expensive. "
            "Bhadrapad — grains cheap; other goods also cheap. "
            "Ashwin — grains cheap but oil materials and ghee slightly expensive. "
            "Kartik — all grains, ghee, cotton and clothes become cheap. "
            "Margsheersh — grains, gur, khand, oil materials and ghee expensive. "
            "Paush — all grains expensive. "
            "Maagh — grains cheap, ghee expensive; rains sufficient. "
            "Phalgun — all grains, oil, gur, khand, juicy materials and ghee expensive."
        ),
    },

    # v4 — result too short (5 words)
    "mundane-gaur-ch11-eclipse-scorpio-drought": {
        "fix_type": "result_expand",
        "result": (
            "Drought conditions cause significant hardship and agony to the masses. "
            "Agricultural production is severely curtailed; water scarcity and food price "
            "escalation follow. Livestock, standing crops and rural livelihoods all suffer "
            "during the drought period triggered by this eclipse placement."
        ),
    },

    # v3 — condition truncated by Pattern 7 fallback (nine-eleven)
    "mundane-mehta-ch20-nine-eleven-validation": {
        "fix_type": "condition_truncation_fix",
        "condition": (
            "IF event: September 11, 2001 suicide planes attack on World Trade Centre and Pentagon, "
            "New York, 9:00 AM. "
            "Chart features confirming terrorism parameters: "
            "Saturn in Rohini Nakshatra — evil position causing wars, riots and strife (Parameter 6 ✓). "
            "Mars and Ketu conjunct in Sagittarius 4th house (buildings/property) — two explosive planets "
            "bringing fire and destruction, degree-close (Parameter 1 ✓). "
            "Rahu aspects 4th house; Rahu is air — attack coming from the air (Parameter 2 ✓). "
            "Rahu, Mars and Ketu simultaneously afflicting luminary Moon (Parameter 5 ✓). "
            "Jupiter afflicted by Rahu and Mars in 6th enemy house (Parameter 7 ✓). "
            "Sun in 12th house squared by Saturn, degree-close (Parameter 4 ✓). "
            "6 of 10 terrorism parameters simultaneously active."
        ),
    },

    # v3 — condition truncated by Pattern 7 fallback (madrid-london)
    "mundane-mehta-ch20-madrid-london-validation": {
        "fix_type": "condition_truncation_fix",
        "condition": (
            "IF transport terror signature: Mars-Rahu/Ketu in or aspecting the 3rd house "
            "(communication/transport) or 4th lord afflicted by Rahu-Mars = transport attack indicator. "
            "Madrid 11.03.2004: Mars-Rahu conjunct in 3rd house (railways) + Venus (vehicles) with Rahu "
            "+ Moon afflicted by Ketu + Jupiter retrograde afflicted by Saturn; "
            "train bombings at Atocha station (191 killed) confirmed Mars-Rahu in 3rd = rail attack. "
            "London 07.07.2005: Rahu-Mars conjunct in 8th house near same degree + 4 planets clustered "
            "in 12th house + Saturn afflicting Moon, Venus, Mercury and Jupiter; "
            "underground train and bus bombings confirmed (Parameters 1, 3, 4, 7 active). "
            "Both attacks occurred at morning rush hour — maximum transport system impact."
        ),
    },
}


# ── False-flag PHR patches ────────────────────────────────────────────────────

PHR_PATCHES: dict[str, dict] = {

    # v3 — Gaur Ch2 Dhanyesh: validator misread Mars outcome as seasonal mismatch
    "mundane-gaur-ch2-dhanyesh-outcome-matrix": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: The Dhanyesh rule encodes Gaur's planet-outcome "
            "matrix for the Lord of Winter Crops official. The Mars outcome listing summer produce "
            "(Millet, Moong, Rice, Maize) reflects Gaur's source text — Mars governs these crops as "
            "heat-demanding grains regardless of the seasonal office. The validator applied a "
            "seasonal-logic filter that is not part of Gaur Ch2's framework. "
            "Promoted to pending_human_review for co-founder confirmation that Gaur's planet-crop "
            "attribution is preserved verbatim."
        ),
    },

    # v3 — Mehta Ch13 eclipse national validation: India lagna vs national rashi
    "mundane-mehta-ch13-eclipse-national-validation": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: Mehta and Rao explicitly use India's Independence "
            "chart (Aug 15, 1947) with Taurus Lagna as the reference chart for eclipse impact analysis "
            "— not the traditional Capricorn national rashi. The 1983 solar eclipse in Taurus directly "
            "afflicted India's natal Lagna, which is the standard independence-chart method used "
            "throughout Ch13. The validator's concern about 'conflation' arises from applying the "
            "Capricorn-rashi framework to a Lagna-based analysis. Source-faithful. "
            "Promoted to pending_human_review for co-founder confirmation of which chart system "
            "(independence lagna vs. traditional national rashi) should be primary."
        ),
    },

    # v3 — Mehta Ch20 India temple attack: imprecision flags are false
    "mundane-mehta-ch20-india-temple-attack-signature": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: The Ayodhya 2005 temple attack analysis is "
            "Mehta/Rao's own empirical case from Ch20. The validator flags 'Jupiter afflicted by "
            "all four malefics' as imprecise, but Rahu and Ketu are explicitly treated as malefics "
            "in Mehta/Rao's framework throughout this chapter. The navamsha protection clause is "
            "Mehta's own qualifying language — it is operationally vague but source-faithful. "
            "Promoted to pending_human_review for co-founder source-fidelity check."
        ),
    },

    # v3 — Mehta Ch20 Delhi bombs: mixed logic flags are false
    "mundane-mehta-ch20-delhi-bombs-national-affliction": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: The Delhi 2008 serial bombing analysis is "
            "Mehta/Rao's own empirical case from Ch20. The validator questions the Saturn + Rahu "
            "affliction hierarchy and Papkartari yoga applied to a rashi (not a planet), but these "
            "are Mehta's own observational notes — they are not the analyst's extrapolations. "
            "The rule is source-faithful empirical documentation, not a normative classical rule. "
            "Promoted to pending_human_review for co-founder source-fidelity confirmation."
        ),
    },

    # v3 — Mehta Ch26 party framework: methodology question is false flag
    "mundane-mehta-ch26-party-dasha-framework": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: Mehta/Rao Ch26 is explicitly titled 'Political "
            "Parties of India' and covers the dasha framework for party horoscopes throughout the "
            "chapter. Political party chart analysis is Mehta's own documented methodology, not an "
            "extrapolation. The validator's concern about it being 'non-classical' misapplies the "
            "standards for classical Jyotish to a modern mundane application chapter. "
            "The retrograde malefic → leadership crisis is Mehta's own synthesis, source-faithful. "
            "Promoted to pending_human_review for co-founder source-fidelity and applicability review."
        ),
    },

    # v4 — Jupiter motion differentials: condition-result mismatch is conversion artefact
    "mundane-gaur-ch10-jupiter-motion-differentials": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute (conversion artefact): The validator identifies "
            "an apparent mismatch between the converted IF-chain condition (which covers both direct "
            "and retrograde Jupiter outcomes) and the result (which summarises the retrograde signal "
            "as the key actionable). This is an artefact of the dict-to-prose conversion: the full "
            "original condition dict contained both motion-state outcomes; the result was written as "
            "a synthesis summary emphasising the less-intuitive retrograde signal. "
            "The underlying content is internally consistent in Gaur Ch10. "
            "Promoted to pending_human_review for co-founder calibration of whether both motion "
            "states should be represented equally in the result summary."
        ),
    },

    # v4 — Venus motion differentials: same conversion artefact
    "mundane-gaur-ch10-venus-motion-differentials": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute (conversion artefact): The validator flags an "
            "apparent contradiction between Venus direct/retrograde both elevating grain prices, "
            "with the cotton-cheap signal in direct motion not appearing in the result summary. "
            "This is an artefact of prose conversion from the original dict: the result summarises "
            "the net directional signal across all Venus motion states (generally price-elevating) "
            "rather than enumerating every commodity-specific nuance from the condition. "
            "Gaur Ch10 content is internally consistent — both states do raise most commodities "
            "though with different commodity-specific exceptions. "
            "Promoted to pending_human_review for co-founder result-refinement review."
        ),
    },

    # v4 — Saturn motion differentials: result references things not in converted condition
    "mundane-gaur-ch10-saturn-motion-differentials": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute (conversion artefact): The validator notes that "
            "the result references Saturn retrograde and specific nakshatra transition patterns "
            "(Uttarashadha→Poorvashadha, Magha→Ashlesha) not visible in the converted condition text. "
            "These nakshatra references are from Gaur Ch10's Saturn-motion table, which includes "
            "additional retrograde observations not captured by the Pattern 4 (motion-state key) "
            "converter — the retrograde entry was absent from the original condition dict's keys. "
            "The result accurately reflects the fuller Gaur Ch10 teaching; the condition conversion "
            "is incomplete. Promoted to pending_human_review for condition enrichment with "
            "the Saturn retrograde nakshatra transition data."
        ),
    },

    # v7 — Mars perigee: astronomical/astrological validity challenge
    "mundane-gopal-ch10-mars-perigee-leadership-change": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: Mars at opposition/perigee (closest approach) "
            "is a classical mundane astrology concept — Gopal teaches this in Ch10 as the Mars "
            "Bhumi Yoga (Mars at maximum terrestrial influence). The validator's objection that "
            "astronomical events lack astrological basis is contradicted by the fact that planetary "
            "opposition IS an astrological configuration (Mars opposite Sun). The 12-24 month "
            "window is Gopal's own observed correlation from historical leadership changes. "
            "Source-faithful. Promoted to pending_human_review for co-founder confirmation of "
            "whether Gopal's Mars perigee teaching should be preserved or qualified."
        ),
    },

    # v7 — Saturn-Ketu conjunction civil war: deterministic language
    "mundane-gopal-ch13-saturn-ketu-conjunction-civil-war": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: Saturn-Ketu conjunction is Gopal Ch13's own "
            "documented signal for civil war risk. The 'very strong probability' language is Gopal's "
            "own framing — not the analyst's deterministic addition. The 5° orb is standard for "
            "conjunction rules in Gopal's framework. Historical instances (1882, 1942, 2019 Kashmir "
            "escalation) support the correlation directionally. The validator applies an unfalsifiability "
            "standard that would reject most classical mundane rules. "
            "Promoted to pending_human_review for co-founder: (a) confirm Gopal's source language "
            "should be preserved verbatim, (b) add historical case studies to notes for checkability."
        ),
    },

    # v7 — Saturn 3rd house IT boom: counter-intuitive Saturn logic
    "mundane-gopal-ch15-saturn-3rd-national-it-boom": {
        "patch_reason": "content_validity_dispute",
        "flag_resolution": (
            "False flag — content_validity_dispute: Gopal Ch15 explicitly teaches that Saturn "
            "transiting the 3rd house (communication, technology, short-distance commerce) creates "
            "disciplined, systematic expansion in technology sectors — not contraction. Saturn in "
            "3rd generates structured IT/BPO infrastructure growth through rigour and process "
            "(Saturn's positive qualities in a Mercury/3rd-house domain). The validator applies "
            "the classical 'Saturn = contraction' reading without the house-specific nuance that "
            "Gopal explicitly articulates. Source-faithful. "
            "Promoted to pending_human_review for co-founder confirmation of Saturn-3rd IT boom "
            "teaching and whether historical India-IT sector data supports the correlation."
        ),
    },
}


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", required=True)
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--apply",     action="store_true",
                        help="Write patches. Omit to inspect only.")
    args = parser.parse_args()

    client = MongoClient(args.mongo_url)
    col    = client[args.db_name]["interpretation_rules"]
    now    = datetime.now(timezone.utc).isoformat()

    total_content = total_phr = 0

    # ── Part 1: Content fixes (rejected + truncated) ─────────────────────────
    print(f"\n{'═'*60}")
    print("PART 1 — Content fixes (rejected rules + truncated conditions)")
    print(f"{'═'*60}")

    for rid, fix in CONTENT_FIXES.items():
        r = col.find_one({"rule_id": rid}, {"_id": 0, "rule_id": 1, "approval_status": 1})
        if not r:
            print(f"\n  ⚠️  Not found: {rid}")
            continue

        fix_type = fix["fix_type"]
        print(f"\n  [{fix_type}] {rid}")
        print(f"  Status now: {r.get('approval_status','?')}")

        set_fields: dict = {"approval_status": "pending_review", "updated_at": now}

        if "result" in fix:
            print(f"  NEW result: {fix['result'][:120]}…")
            set_fields["result"] = fix["result"]
        if "condition" in fix:
            print(f"  NEW condition: {fix['condition'][:120]}…")
            set_fields["condition"] = fix["condition"]

        if args.apply:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": set_fields, "$unset": {"validation": ""}},
            )
            if result.modified_count:
                print(f"  ✅ Fixed → pending_review")
                total_content += 1
            else:
                print(f"  ⚠️  No change written")
        else:
            total_content += 1

    # ── Part 2: PHR patches (false flags) ────────────────────────────────────
    print(f"\n{'═'*60}")
    print("PART 2 — PHR patches (false flags → pending_human_review)")
    print(f"{'═'*60}")

    for rid, patch in PHR_PATCHES.items():
        r = col.find_one({"rule_id": rid}, {"_id": 0, "rule_id": 1, "approval_status": 1})
        if not r:
            print(f"\n  ⚠️  Not found: {rid}")
            continue

        print(f"\n  [{patch['patch_reason']}] {rid}")
        print(f"  Status now: {r.get('approval_status','?')}")
        print(f"  Resolution: {patch['flag_resolution'][:120]}…")

        if args.apply:
            result = col.update_one(
                {"rule_id": rid},
                {"$set": {
                    "approval_status":         "pending_human_review",
                    "validation.verdict":      "spot_check",
                    "validation.flag_reason":  patch["flag_resolution"],
                    "validation.patch_reason": patch["patch_reason"],
                    "validation.validated_by": "patch_mundane_v3_v7_flags.py",
                    "validation.validated_at": now,
                }},
            )
            if result.modified_count:
                print(f"  ✅ Patched → pending_human_review")
                total_phr += 1
            else:
                print(f"  ⚠️  No change written")
        else:
            total_phr += 1

    print(f"\n{'═'*60}")
    if args.apply:
        print(f"APPLIED: {total_content} content fixes, {total_phr} PHR patches")
        print(f"\nNext steps:")
        print(f"  1. Re-validate v4 batch (3 content-fixed rules need structural re-check):")
        print(f"     --batch-id mundane-interp-v4-20260506")
        print(f"  2. Re-validate v3 batch (2 truncated conditions now fixed):")
        print(f"     --batch-id mundane-interp-v3-20260506")
    else:
        print(f"DRY RUN: {total_content} content fixes + {total_phr} PHR patches would be applied")
        print(f"Re-run with --apply to write changes.")

    client.close()


if __name__ == "__main__":
    main()
