#!/usr/bin/env python3
"""
patch_bphs_vol2_phase1_pdf_confirmed.py

Patches 47 rules confirmed authentic against Santhanam BPHS Vol 2 PDF
during triage session 2026-06-03. One additional rule (R-BPHS55-086) is
patched to 'deferred_further_eval' status.

All 47 confirmed rules: flagged → pending_human_review + validator_error:true
  triage_bucket = "C_pdf_confirmed"

One deferred rule: flagged → pending_human_review + validator_error:false
  triage_bucket = "deferred_further_eval"

Supersedes patch_bphs_vol2_phase1_deferred.py (now obsolete).
Companion to patch_bphs_vol2_phase1_api_bucket_b.py (7 Bucket B rules).

PDF source: BPHS - 2 RSanthanam.pdf
  /Users/apple/Documents/Knowledge Engine_eBooks/BPHS Vol 2/

Key validator errors corrected:
  - BPHS dusthana grouping (6th/8th/12th identical effects = authentic doctrine)
  - Ketu/Rahu with benefics can still yield negative effects (BPHS "even if" clauses)
  - Ketu/Rahu in auspicious positions CAN give positive effects per explicit slokas
  - "dysentry" is Santhanam's authentic transliteration, NOT an OCR error
  - Remedies confirmed where validator claimed none existed
  - Commencement-vs-later pattern (good start, difficult end in dusthana placements)
  - BPHS uses Rahu/Ketu as maraka lords in antardasha chapters

Encoding errors noted in cc_review_note (require separate data correction):
  - R-BPHS53-PATCH-094A74/A460E9/E77E96: dasha_lord=Venus, should be Moon (Ch.53 batch bug)
  - R-BPHS54-PATCH-3E2164: antardasha_planet=Mars, should be Moon
  - R-BPHS54-PATCH-3E8999: antardasha_planet=Mars, should be Rahu
  - R-BPHS54-PATCH-6592D5: antardasha_planet=Mars, should be Jupiter
  - R-BPHS53-PATCH-37CB8C: houses_involved=[7], should be [2,7] (sloka 51: "2nd or 7th")
  - R-BPHS47-PATCH-CC30B7: dasha_lord=Sun, should be Jupiter (Jupiter MD chapter)
  - R-BPHS57-PATCH-0727F5: reference point "from Ascendant" should be "from Dasa lord (Saturn)"

Dry run by default. Pass --live to apply.

Usage:
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_pdf_confirmed.py
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_pdf_confirmed.py --live
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR        = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-vol2-ph1-triage-20260603"

# ── 47 PDF-confirmed validator-error rules ─────────────────────────────────────
# Format: (rule_id, sloka_ref, cc_review_note)
# All → approval_status=pending_human_review, validator_error=True,
#        triage_bucket="C_pdf_confirmed"
PDF_CONFIRMED = [

    # ── Chapter 47 (Jupiter Mahadasha) ──────────────────────────────────────
    (
        "R-BPHS47-PATCH-CC30B7",
        "Ch.47 slokas 49-51",
        "PDF CONFIRMED (slokas 49-51): Content is authentic BPHS Ch.47 doctrine -- "
        "effects in the Antardasa of Jupiter when Jupiter is the Mahadasha lord. "
        "ENCODING ERROR: dasha_lord field is set to 'Sun' but should be 'Jupiter' -- "
        "this chapter covers Jupiter Mahadasha, not Jupiter AD in Sun MD. Requires "
        "field correction. Validator incorrectly flagged as conflation; the natal "
        "associations → dasha results format is standard BPHS Ch.47 methodology.",
    ),
    (
        "R-BPHS47-PATCH-E5CAC4",
        "Ch.47 slokas 7-11",
        "PDF CONFIRMED (slokas 7-11): BPHS standard format -- natal house associations "
        "and planetary conditions modify dasha-period results. Slokas explicitly link "
        "natal placements (Jupiter in various houses, dignity states) to the effects "
        "experienced during the dasha period. Not a conflation of natal and dasha "
        "charts; this is the authentic BPHS methodology for dasha interpretation. "
        "Validator error.",
    ),

    # ── Chapter 53 (Moon Mahadasha / Antardasa effects) ─────────────────────
    (
        "R-BPHS53-025",
        "Ch.53 sloka 31",
        "PDF CONFIRMED (sloka 31): Verbatim BPHS text -- 'premature death if Jupiter "
        "be the lord of the 2nd or the 7th.' Authentic maraka-lord doctrine in Moon "
        "MD context. Validator questioned extreme outcome; BPHS is explicit. "
        "No encoding error.",
    ),
    (
        "R-BPHS53-PATCH-094A74",
        "Ch.53 slokas 1-2",
        "PDF CONFIRMED (slokas 1-2): Moon MD / Moon AD content confirmed authentic. "
        "ENCODING ERROR (Ch.53 batch bug): dasha_lord field is set to 'Venus' for "
        "all Ch.53 rules; should be 'Moon' throughout -- Ch.53 is 'Effects of "
        "Antardasas in the Dasa of the Moon.' Validator correctly identified "
        "dasha_lord as wrong but the content itself is authentic.",
    ),
    (
        "R-BPHS53-PATCH-16C7C5",
        "Ch.53 sloka 35",
        "PDF CONFIRMED (sloka 35): Saturn in 8th → pilgrimages confirmed. In BPHS "
        "context these are difficult forced journeys, not auspicious pilgrimages -- "
        "consistent with Saturn's malefic nature. Validator incorrectly applied "
        "modern positive connotation of 'pilgrimages.' Authentic doctrine. "
        "Note: dasha_lord=Venus is the Ch.53 batch bug; should be Moon.",
    ),
    (
        "R-BPHS53-PATCH-37CB8C",
        "Ch.53 sloka 51",
        "PDF CONFIRMED (sloka 51): Content authentic. Sloka 51 explicitly states "
        "'premature death if Jupiter be the lord of the 2nd or the 7th' -- "
        "ENCODING ERROR: condition field houses_involved=[7] only; should be [2,7] "
        "to correctly represent 'lord of 2nd or 7th.' Requires houses_involved "
        "field correction. Also: dasha_lord=Venus is Ch.53 batch bug; should be Moon.",
    ),
    (
        "R-BPHS53-PATCH-5E3A16",
        "Ch.53 slokas 25-28",
        "PDF CONFIRMED (slokas 25-28): Slokas 25-28 explicitly group the 6th, 8th, "
        "and 12th together with identical effects -- this is authentic BPHS dusthana "
        "grouping doctrine, confirmed across all Vol 2 antardasa chapters. Having "
        "identical effects for 6th/8th/12th house placements is NOT a copy-paste "
        "error; it is Parasara's intentional methodology. Validator error.",
    ),
    (
        "R-BPHS53-PATCH-A460E9",
        "Ch.53 slokas 36-38",
        "PDF CONFIRMED (slokas 36-38): Content confirmed authentic -- Moon MD context "
        "with specified planetary placements. ENCODING ERROR (Ch.53 batch bug): "
        "dasha_lord=Venus; should be Moon. Content is valid; metadata correction "
        "required.",
    ),
    (
        "R-BPHS53-PATCH-BF3DC0",
        "Ch.53 slokas 50-52",
        "PDF CONFIRMED (slokas 50-52): Mrityunjaya Japa remedy IS explicitly "
        "prescribed in Ch.53 slokas 50-52. Validator claimed no remedy existed "
        "in Ch.53 -- completely wrong. Slokas 50-52 are the remedy slokas for "
        "difficult planetary positions in Moon MD. Note: dasha_lord=Venus is "
        "Ch.53 batch bug; should be Moon.",
    ),
    (
        "R-BPHS53-PATCH-E77E96",
        "Ch.53 sloka 35",
        "PDF CONFIRMED (sloka 35): Sloka 35 explicitly includes the 2nd house in "
        "the condition -- houses_involved covers 2nd house effects. ENCODING ERROR "
        "(Ch.53 batch bug): dasha_lord=Venus; should be Moon. Validator flagged "
        "the 2nd house inclusion but it is explicitly in the sloka text.",
    ),

    # ── Chapter 54 (Mars Mahadasha / Antardasa effects) ─────────────────────
    (
        "R-BPHS54-061",
        "Ch.54 slokas 46-47",
        "PDF CONFIRMED (slokas 46-47): Verbatim BPHS text -- 'possibility of critical "
        "illness in the Antardasa of Mercury if he be the lord of the 2nd or the 7th.' "
        "Authentic maraka-lord doctrine for Mercury AD in Mars MD. Validator incorrectly "
        "flagged compound condition (Mercury AD + Mercury as maraka) as conflation. "
        "This is standard BPHS methodology.",
    ),
    (
        "R-BPHS54-PATCH-116D9B",
        "Ch.54 sloka 67",
        "PDF CONFIRMED (sloka 67): Sloka 67 groups Sun in 6th, 8th, OR 12th from "
        "Mars Dasa lord with IDENTICAL effects (fever, dysentry, etc.) -- authentic "
        "BPHS dusthana grouping. 'dysentry' is Santhanam's authentic transliteration "
        "of the Sanskrit term, confirmed across Ch.53, Ch.54, Ch.57, Ch.58. "
        "Validator error on both the dusthana grouping and the 'dysentry' spelling.",
    ),
    (
        "R-BPHS54-PATCH-26A25A",
        "Ch.54 slokas 48-49",
        "PDF CONFIRMED (slokas 48-49): BPHS explicitly -- 'Ketu in kendra, trikona, "
        "the 3rd or the 11th (from the Ascendant) or be associated or aspected by "
        "benefics → beneficence of king, gain of wealth, birth of son, conferment of "
        "authority by government, gain of cattle.' Ketu in 3rd giving positive effects "
        "is AUTHENTIC Ch.54 doctrine. Validator completely wrong to call this a "
        "contradiction of BPHS -- the sloka is verbatim and unambiguous.",
    ),
    (
        "R-BPHS54-PATCH-3E2164",
        "Ch.54 slokas 70-73",
        "PDF CONFIRMED (slokas 70-73): Moon AD in Mars MD with Moon in 4th house "
        "along with lord of 4th → auspicious effects confirmed authentic. "
        "ENCODING ERROR: antardasha_planet=Mars; should be Moon. This is a "
        "Ch.54 batch-level bug where antardasha_planet was set to Mars for multiple "
        "rules. Content is valid; field correction required.",
    ),
    (
        "R-BPHS54-PATCH-3E8999",
        "Ch.54 slokas 9-10",
        "PDF CONFIRMED (slokas 9-10): Rahu in 9th with benefics → positive effects "
        "confirmed authentic. ENCODING ERROR: antardasha_planet=Mars; should be "
        "Rahu. Ch.54 batch bug affecting multiple rules. Content is valid; "
        "antardasha_planet field correction required.",
    ),
    (
        "R-BPHS54-PATCH-6592D5",
        "Ch.54 slokas 20-22",
        "PDF CONFIRMED (slokas 20-22): 'Shiva Sahasranam' IS the prescribed remedy "
        "for Jupiter's malefic placement in Mars MD context -- slokas 20-22 are "
        "explicit. ENCODING ERROR: antardasha_planet=Mars; should be Jupiter (this "
        "is Jupiter AD in Mars MD content). Ch.54 batch bug. Content confirmed; "
        "antardasha_planet field correction required.",
    ),
    (
        "R-BPHS54-PATCH-F1FDFB",
        "Ch.54 sloka 26",
        "PDF CONFIRMED (sloka 26): Sloka 26 groups Saturn in 8th AND 12th together "
        "with identical effects (danger from foreign dignitaries, loss of wealth, "
        "imprisonment, disease). Identical effects for 8th and 12th = authentic BPHS "
        "dusthana grouping doctrine. Validator error.",
    ),

    # ── Chapter 55 (Rahu Mahadasha / Antardasa effects) ─────────────────────
    (
        "R-BPHS55-085",
        "Ch.55 slokas 78-79",
        "PDF CONFIRMED (slokas 78-79): Mars in the 3rd from Rahu Dasa lord → "
        "acquisition of garments, audience with king, commander position, wealth "
        "through kinsmen. Sloka 78-79 explicitly groups Mars in {kendra, 5th, 3rd, "
        "11th} with identical effects. Three rules (085/086/087) for different "
        "positions in this group having identical effects is authentic BPHS doctrine. "
        "Validator error on the 'duplicate' objection.",
    ),
    (
        "R-BPHS55-087",
        "Ch.55 slokas 78-79",
        "PDF CONFIRMED (slokas 78-79): Mars in the 11th from Rahu Dasa lord → "
        "same positive effects as Mars in 3rd (acquisition of garments, audience with "
        "king, etc.). Sloka 78-79 explicitly groups 11th with kendra, 5th, 3rd. "
        "Identical effects across grouped positions = authentic BPHS dusthana/grouping "
        "doctrine. Validator error.",
    ),
    (
        "R-BPHS55-PATCH-3B702B",
        "Ch.55 slokas 51-53",
        "PDF CONFIRMED (slokas 51-53): Venus associated with Saturn, Mars or Rahu → "
        "separation, distress, danger of death to self or employer, stomach pain. "
        "Verbatim: 'if Venus be... associated with Saturn, Mars or Rahu.' Standard "
        "BPHS association-based affliction rule. Validator error.",
    ),
    (
        "R-BPHS55-PATCH-49AF69",
        "Ch.55 sloka 39",
        "PDF CONFIRMED (sloka 39): Verbatim -- 'Remedial measure to obtain relief "
        "from the above evil effects is recitation of Vishnu Sahasranam.' Sloka 39 "
        "explicitly prescribes this remedy for Mercury as lord of 2nd or 7th in "
        "Rahu MD. Validator claimed no remedy was prescribed here -- completely wrong.",
    ),
    (
        "R-BPHS55-PATCH-4EBC18",
        "Ch.55 slokas 13-14",
        "PDF CONFIRMED (slokas 13-14): Jupiter in 12th from Ascendant → loss of "
        "wealth, obstacles, defamation, distress, heart disease. Explicitly confirmed. "
        "Even Santhanam's translator note acknowledges the apparent paradox in the "
        "sloka (entrustment of authority alongside evil effects) but confirms the "
        "text as authentic Parasara. Validator error.",
    ),
    (
        "R-BPHS55-PATCH-65706D",
        "Ch.55 sloka 39",
        "PDF CONFIRMED (sloka 39): Verbatim -- 'If Mercury be the lord of the 2nd or "
        "the 7th, there will be fear of premature death.' Authentic maraka-lord "
        "doctrine for Mercury AD in Rahu MD. Validator error.",
    ),
    (
        "R-BPHS55-PATCH-6AC96A",
        "Ch.55 slokas 15-17",
        "PDF CONFIRMED (slokas 15-17): Jupiter in kendra, trikona, 11th, 2nd or 3rd "
        "from Rahu Dasa lord (not from Ascendant) → gains of land, food, cattle, "
        "charitable inclination. This is a DIFFERENT condition from slokas 8-12 "
        "(kendra from Ascendant). Both conditions exist in Ch.55 and are authentic. "
        "Validator failed to distinguish the two reference points. Validator error.",
    ),

    # ── Chapter 56 (Jupiter Mahadasha / Antardasa effects) ──────────────────
    (
        "R-BPHS56-051",
        "Ch.56 sloka 29",
        "PDF CONFIRMED (sloka 29): Verbatim -- 'At the end of the Dasa, however, "
        "there will be loss of wealth and bodily distress.' Sloka 29 explicitly "
        "describes a commencement-vs-later pattern for Mercury AD in Jupiter MD: "
        "good effects at the start even if afflicted, negative at the end. "
        "Rule captures the end-of-antardasa effects. Validator was uncertain -- "
        "text is explicit.",
    ),
    (
        "R-BPHS56-052",
        "Ch.56 slokas 30-31",
        "PDF CONFIRMED (slokas 30-31): Verbatim -- 'Premature death may be expected "
        "if Mercury be the lord of the 2nd or the 7th.' Validator thought the "
        "extreme outcome was suspicious but BPHS is explicit. Authentic maraka-lord "
        "doctrine for Mercury AD in Jupiter MD. Validator error.",
    ),
    (
        "R-BPHS56-055",
        "Ch.56 slokas 32-32.5",
        "PDF CONFIRMED (slokas 32-32½): BPHS explicitly -- Ketu associated with or "
        "aspected by benefics in Jupiter MD gives: 'moderate gain of wealth, coarse "
        "food or food given by others, food given at the time of death ceremonies, "
        "acquisition of wealth through undesirable means.' Benefic aspect on Ketu "
        "modifies but does NOT make effects fully positive -- Ketu retains malefic "
        "nature. Validator applied generic benefic=positive logic incorrectly. "
        "Authentic doctrine.",
    ),
    (
        "R-BPHS56-056",
        "Ch.56 slokas 32-32.5",
        "PDF CONFIRMED (slokas 32-32½): Same context as R-BPHS56-055. BPHS gives "
        "mixed/negative effects for Ketu even when aspected by benefics in Jupiter "
        "MD. The dasha_unfavourable tagging reflects this mixed nature. Content "
        "is authentic per the explicit sloka text. Validator error.",
    ),
    (
        "R-BPHS56-PATCH-AEBB42",
        "Ch.56 slokas 37-38",
        "PDF CONFIRMED (slokas 37-38): Santhanam's translation explicitly states "
        "'if Ketu be the lord of the 2nd or the 7th (or in the 2nd or the 7th).' "
        "The BPHS text uses this formulation for Ketu as house lord/occupant in the "
        "maraka context, consistent with Rahu's equivalent treatment in the same "
        "chapter (slokas 79-80). Whether this reflects KP co-rulership or occupancy "
        "is a secondary interpretive question -- the rule faithfully represents "
        "Santhanam's translation. Validator error on the 'Ketu cannot be house lord' "
        "objection; classical vs KP distinction is doctrinal, not a rule defect.",
    ),
    (
        "R-BPHS56-PATCH-D0BAEB",
        "Ch.56 slokas 54-55",
        "PDF CONFIRMED (slokas 54-55): BPHS explicitly groups Sun in 6th, 8th, AND "
        "12th with identical effects -- fever, nervous disorder, laziness, antagonism, "
        "separation from kinsmen. Sloka 54: 'if the Sun be in the 6th, the 8th or "
        "the 12th from the Ascendant or the lord of the Dasa (Jupiter).' Classic "
        "dusthana grouping -- confirmed as authentic across every Vol 2 antardasa "
        "chapter. Validator error.",
    ),

    # ── Chapter 57 (Saturn Mahadasha / Antardasa effects) ───────────────────
    (
        "R-BPHS57-029",
        "Ch.57 slokas 20-21.5",
        "PDF CONFIRMED (slokas 20-21½): Verbatim -- 'Fear of premature death, coarse "
        "food, cold fever, dysentry, wounds, danger from thieves, separation from "
        "wife and children... if Ketu be in the 8th or the 12th from the Ascendant "
        "or the lord of the Dasa (Saturn).' 'dysentry' is Santhanam's own spelling "
        "in the source text -- confirmed in Ch.53, Ch.54, Ch.56, Ch.57, Ch.58. Not "
        "OCR error. NOTE: 'coarse fool' in KE database summary should read 'coarse "
        "food' -- minor summary field typo, not a doctrinal issue.",
    ),
    (
        "R-BPHS57-033",
        "Ch.57 slokas 20-21.5",
        "PDF CONFIRMED (slokas 20-21½): Ketu in 12th from Ascendant/Dasa lord → "
        "same effects as Ketu in 8th per the same sloka ('8th or the 12th'). "
        "Classic BPHS dusthana grouping (8th and 12th identical effects). "
        "'dysentry' is authentic Santhanam transliteration. Validator errors on both "
        "the 'OCR' concern and the dusthana grouping objection.",
    ),
    (
        "R-BPHS57-098",
        "Ch.57 slokas 61-62",
        "PDF CONFIRMED (slokas 61-62): Verbatim -- 'Great distress, dependence on "
        "others and fear of premature death, may be expected if Mars be in the 2nd "
        "or be the lord of the 7th or the 8th from the Ascendant.' Mars in 2nd house "
        "(PLACEMENT, not lordship) explicitly causes this outcome. Validator confused "
        "house placement with house lordship. Rule is correct -- Mars in 2nd house "
        "during Saturn MD → distress and premature death risk.",
    ),
    (
        "R-BPHS57-PATCH-0727F5",
        "Ch.57 slokas 32-34",
        "PDF CONFIRMED (slokas 32-34): Content authentic -- Venus in 6th/8th/12th → "
        "eye trouble, fevers, dental problems, heart disease, danger from "
        "drowning/falling. ENCODING ERROR: condition reference point is 'from "
        "Ascendant' but the sloka explicitly says 'from the lord of the Dasa "
        "(Saturn).' These are different house measurements. Content is valid; "
        "condition reference point requires correction to 'from Dasa lord (Saturn).'",
    ),
    (
        "R-BPHS57-PATCH-37B401",
        "Ch.57 slokas 81-82",
        "PDF CONFIRMED (slokas 81-82): Verbatim -- 'Remedial measures to obtain "
        "relief from the above evil effects are recitation of Shiva Sahasranama and "
        "giving gold in charity.' Explicitly for Jupiter as lord of 2nd or 7th in "
        "Saturn MD. Validator error (claimed the remedy lacked Jupiter-specificity; "
        "it is directly tied to Jupiter in slokas 81-82).",
    ),
    (
        "R-BPHS57-PATCH-562548",
        "Ch.57 slokas 28-29",
        "PDF CONFIRMED (slokas 28-29): Venus in 6th (from the Ascendant) → "
        "distress to wife, loss of position, mental agony, quarrels. The text "
        "parenthetically says '(from the Ascendant)' -- reference point IS confirmed "
        "in the sloka. Standard BPHS dusthana grouping (6th, 8th, 12th from "
        "Ascendant). Validator error.",
    ),
    (
        "R-BPHS57-PATCH-5C3BA0",
        "Ch.57 slokas 12-13.5",
        "PDF CONFIRMED (slokas 12-13½): BPHS explicitly -- Mercury in 6th/8th/12th "
        "from Ascendant/Dasa lord → 'Acquisition of a kingdom, gain of wealth, "
        "headship of a village, will be the effects at the COMMENCEMENT of the "
        "Dasa.' Followed by affliction with diseases in the middle and end. This "
        "is the BPHS commencement-vs-later pattern. Even Santhanam's translator "
        "noted the paradox but wrote 'we dare not question Parasara.' Rule captures "
        "the initial-phase positive effects. Confirmed authentic.",
    ),
    (
        "R-BPHS57-PATCH-7C33F5",
        "Ch.57 slokas 16-18",
        "PDF CONFIRMED (slokas 16-18): BPHS explicitly -- 'Evil effects like loss of "
        "position, dangers, poverty, distress, foreign journeys... will be derived in "
        "the Antardasa of Ketu in the Dasa of Saturn EVEN IF Ketu be in his sign of "
        "exaltation, in his own sign, in a benefic sign or in kendra or trikona or "
        "be associated with or aspected by benefics.' 'Even if aspected by benefics' "
        "is verbatim in the sloka -- BPHS makes a strong doctrinal statement that "
        "Ketu in Saturn MD is fundamentally malefic regardless of positive placement. "
        "Validator error.",
    ),
    (
        "R-BPHS57-PATCH-AA4529",
        "Ch.57 slokas 16-18",
        "PDF CONFIRMED (slokas 16-18): Same slokas as R-BPHS57-PATCH-7C33F5. BPHS "
        "explicitly lists 'in a benefic sign' as one of the conditions that does NOT "
        "override evil effects for Ketu in Saturn MD. This rule correctly captures "
        "the 'benefic sign' aspect of the same doctrine. Validator error.",
    ),
    (
        "R-BPHS57-PATCH-B89C62",
        "Ch.57 slokas 68-68.5",
        "PDF CONFIRMED (slokas 68-68½): BPHS names specific signs favorable for "
        "Rahu in Saturn MD: Aries, Virgo, Cancer, Taurus, Pisces, or Sagittarius → "
        "acquisition of elephants, opulence, cordial relations with king, valuable "
        "clothes. The KE database encodes these as 'own_sign' which is a simplification "
        "of the specific sign list. The CONTENT is authentic per the sloka. Translator "
        "note confirms validity with caveats about Ascendant/dasa lord reference. "
        "NOTE: Ideally the condition should list the 6 specific signs rather than use "
        "'own_sign' encoding, but this is a future data enrichment, not a rejection.",
    ),
    (
        "R-BPHS57-PATCH-C5E9B2",
        "Ch.57 slokas 16-18",
        "PDF CONFIRMED (slokas 16-18): Same slokas as R-BPHS57-PATCH-7C33F5 and "
        "R-BPHS57-PATCH-AA4529. Ketu associated with benefics → malefic results is "
        "explicit: 'even if... be associated with or aspected by benefics.' Three "
        "separate rules (7C33F5, AA4529, C5E9B2) correctly represent different "
        "condition variations of the same authentic slokas 16-18. Validator error.",
    ),

    # ── Chapter 58 (Mercury Mahadasha / Antardasa effects) ──────────────────
    (
        "R-BPHS58-PATCH-313295",
        "Ch.58 sloka 65",
        "PDF CONFIRMED (sloka 65): Verbatim -- 'There will be physical distress if "
        "Jupiter be the lord of the 2nd or the 7th OR BE IN THE 2ND OR THE 7TH.' "
        "BPHS explicitly covers both Jupiter's PLACEMENT and LORDSHIP as maraka "
        "conditions. Jupiter in 2nd house → physical distress is authentic per sloka. "
        "Validator incorrectly applied 'Jupiter is always benefic' logic; in Mercury "
        "MD, Jupiter in maraka houses activates distress regardless of its benefic "
        "nature. Validator error.",
    ),
    (
        "R-BPHS58-PATCH-36ADF5",
        "Ch.58 sloka 65",
        "PDF CONFIRMED (sloka 65): Same as R-BPHS58-PATCH-313295. Jupiter in 7th "
        "house → physical distress is explicitly covered by 'or be in the 2nd or "
        "the 7th' in sloka 65. Validator error.",
    ),
    (
        "R-BPHS58-PATCH-3B1F8A",
        "Ch.58 slokas 45-46",
        "PDF CONFIRMED (slokas 45-46): Verbatim -- 'The remedial measures to be "
        "adopted to obtain relief from the above evil effects are Mrityunjaya Japa "
        "and giving a cow in charity.' This is for Mars as maraka lord (lord of 2nd "
        "or 7th) in Mercury MD context. Mars AD in Mercury MD is the dasha context "
        "of Ch.58 slokas 45-46. Content is authentic; validator confused the context "
        "reference. Validator error.",
    ),
    (
        "R-BPHS58-PATCH-6DAB01",
        "Ch.58 sloka 65",
        "PDF CONFIRMED (sloka 65): Jupiter as lord of 7th → physical distress is "
        "explicitly covered by 'if Jupiter be the lord of the 2nd or the 7th.' "
        "Authentic maraka-lord doctrine for Jupiter AD in Mercury MD. Validator "
        "flagged it as 'vague and incomplete' -- the sloka is straightforward. "
        "Validator error.",
    ),
    (
        "R-BPHS58-PATCH-707AC3",
        "Ch.58 slokas 34-35",
        "PDF CONFIRMED (slokas 34-35): Verbatim -- 'There will be physical distress "
        "if the Moon be the lord of the 2nd or the 7th (from the Ascendant).' "
        "Moon as lord of 7th specifically is one part of this sloka. Authentic "
        "maraka-lord doctrine for Moon AD in Mercury MD. Validator error.",
    ),
    (
        "R-BPHS58-PATCH-9B332B",
        "Ch.58 sloka 51",
        "PDF CONFIRMED (sloka 51): Verbatim -- 'There will be an opportunity to have "
        "conversation or a meeting with the king (high dignitaries), if Rahu be in "
        "the 3rd, the 8TH, the 10th or the 11th from the Ascendant.' BPHS explicitly "
        "groups the 8th with 3rd/10th/11th for this positive effect. Rahu in 8th is "
        "NOT universally negative in BPHS -- this chapter explicitly gives positive "
        "effects for Rahu in 8th in Rahu AD Mercury MD context. Validator error.",
    ),
    (
        "R-BPHS58-PATCH-D5766C",
        "Ch.58 slokas 6-8.5",
        "PDF CONFIRMED (slokas 6-8½): Verbatim -- 'if Ketu be associated with benefics "
        "in kendra or trikona from the Ascendant or be in conjunction with the lord "
        "of the Ascendant or a yogakaraka' → physical fitness, wealth gain, affectionate "
        "relations, name and fame, audience with king. Ketu conjunct Ascendant lord "
        "IS explicitly an auspicious condition in Ch.58. Validator wrong to claim "
        "BPHS does not attribute positive effects to this. Authentic doctrine.",
    ),
]

# ── 1 deferred rule ────────────────────────────────────────────────────────────
# Content not verifiable with zero ambiguity from available slokas.
# Keep in pending_human_review; validator_error=False; bucket=deferred_further_eval.
DEFERRED = [
    (
        "R-BPHS55-086",
        "Ch.55 slokas 78-82 (partial)",
        "DEFERRED for further evaluation. Slokas 78-79 group Mars in {kendra, 5th, "
        "3rd, 11th} from Rahu Dasa lord with identical positive effects. Mars in 9th "
        "is NOT explicitly in this grouping -- the 9th is a trikona alongside the 5th, "
        "but only the 5th trikona is mentioned in slokas 78-79. If this rule assigns "
        "the same positive effects as R-BPHS55-085/087, the 9th house is unconfirmed "
        "from the sloka text. The negative grouping (slokas 80-82) covers 6th/8th/12th. "
        "The 9th may have been derived by analogy with the trikona pattern from other "
        "chapters. Defer: confirm against full Vol 2 re-read and Vol 1 parallels. "
        "Do not reject -- uncertain, not disproved.",
    ),
]


class _Tee:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._log    = open(path, "w", encoding="utf-8")
        self._stdout = sys.__stdout__
    def write(self, data: str) -> None:
        self._stdout.write(data); self._stdout.flush()
        self._log.write(data);   self._log.flush()
    def flush(self) -> None:
        self._stdout.flush(); self._log.flush()
    def close(self) -> None:
        self._log.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo-url", default=os.environ.get("MONGO_URL", ""))
    parser.add_argument("--db-name",   default="horoscope_db")
    parser.add_argument("--live",      action="store_true",
                        help="Apply patches (default: dry run)")
    args = parser.parse_args()

    if not args.mongo_url:
        print("ERROR: MONGO_URL env var not set."); sys.exit(1)

    ts       = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode     = "live" if args.live else "dryrun"
    log_path = LOG_DIR / f"patch_bphs_vol2_phase1_pdf_confirmed_{ts}_{mode}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 75)
    print(f"  LOG FILE: {log_path}")
    print("=" * 75)
    print()
    print("BPHS Vol 2 Phase 1 -- PDF-Confirmed Patch")
    print(f"Mode        : {'🔴 LIVE -- WRITING TO DB' if args.live else '🟡 DRY RUN -- no changes'}")
    print(f"Confirmed   : {len(PDF_CONFIRMED)} rules → PHR + validator_error:True + C_pdf_confirmed")
    print(f"Deferred    : {len(DEFERRED)} rule  → PHR + validator_error:False + deferred_further_eval")
    print(f"Source      : Santhanam BPHS Vol 2 PDF, triage session 2026-06-03")
    print()

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)[
        args.db_name]["interpretation_rules"]

    now        = datetime.now(timezone.utc)
    patched    = 0
    skipped    = 0
    errors     = []

    # ── Section 1: PDF-confirmed (validator_error=True) ──────────────────────
    print("─" * 75)
    print("SECTION 1 -- PDF CONFIRMED (validator_error=True, bucket=C_pdf_confirmed)")
    print("─" * 75)
    print(f"{'#':<5} {'Rule ID':<42} {'Pre-status':<24} Result")
    print("─" * 75)

    for i, (rule_id, sloka_ref, note) in enumerate(PDF_CONFIRMED, 1):
        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<42} {'NOT FOUND':<24} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status != "flagged":
            print(f"  {i:<4} {rule_id:<42} {pre_status:<24} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":              "pending_human_review",
                "validation.validator_error":   True,
                "validation.api_verdict":       "validator_error",
                "validation.pdf_verified":      True,
                "validation.pdf_sloka_ref":     sloka_ref,
                "validation.cc_review_note":    note,
                "validation.triage_date":       TRIAGE_DATE,
                "validation.triage_session":    TRIAGE_SESSION,
                "validation.triage_bucket":     "C_pdf_confirmed",
                "updated_at":                   now,
            }
        }

        if args.live:
            result = col.update_one({"rule_id": rule_id}, update_doc)
            ok = result.modified_count == 1
            status = "✅ PATCHED" if ok else "❌ FAILED"
            if ok:
                patched += 1
            else:
                errors.append(f"{rule_id}: update returned modified_count=0")
        else:
            status = "🟡 DRY RUN"
            patched += 1

        print(f"  {i:<4} {rule_id:<42} {pre_status:<24} {status}  [{sloka_ref}]")

    # ── Section 2: Deferred (validator_error=False) ───────────────────────────
    print()
    print("─" * 75)
    print("SECTION 2 -- DEFERRED (validator_error:False, bucket=deferred_further_eval)")
    print("─" * 75)
    print(f"{'#':<5} {'Rule ID':<42} {'Pre-status':<24} Result")
    print("─" * 75)

    for i, (rule_id, sloka_ref, note) in enumerate(DEFERRED, 1):
        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<42} {'NOT FOUND':<24} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status != "flagged":
            print(f"  {i:<4} {rule_id:<42} {pre_status:<24} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":              "pending_human_review",
                "validation.validator_error":   False,
                "validation.pdf_verified":      False,
                "validation.pdf_sloka_ref":     sloka_ref,
                "validation.cc_review_note":    note,
                "validation.triage_date":       TRIAGE_DATE,
                "validation.triage_session":    TRIAGE_SESSION,
                "validation.triage_bucket":     "deferred_further_eval",
                "updated_at":                   now,
            }
        }

        if args.live:
            result = col.update_one({"rule_id": rule_id}, update_doc)
            ok = result.modified_count == 1
            status = "✅ PATCHED" if ok else "❌ FAILED"
            if ok:
                patched += 1
            else:
                errors.append(f"{rule_id}: update returned modified_count=0")
        else:
            status = "🟡 DRY RUN"
            patched += 1

        print(f"  {i:<4} {rule_id:<42} {pre_status:<24} {status}  [deferred]")

    # ── Summary ───────────────────────────────────────────────────────────────
    total_rules = len(PDF_CONFIRMED) + len(DEFERRED)
    print()
    print("=" * 75)
    print("SUMMARY")
    print(f"  Mode        : {'LIVE' if args.live else 'DRY RUN'}")
    print(f"  Total rules : {total_rules}")
    print(f"  Patched     : {patched} / {total_rules}")
    print(f"  Skipped     : {skipped}")
    if errors:
        print(f"  Errors      : {len(errors)}")
        for e in errors:
            print(f"    {e}")
    if not args.live:
        print()
        print("  Re-run with --live to apply.")
    print()
    print("ENCODING ERRORS NOTED (separate data correction task, not rejections):")
    print("  R-BPHS53-PATCH-094A74/A460E9/E77E96 : dasha_lord=Venus → should be Moon")
    print("  R-BPHS53-PATCH-37CB8C               : houses_involved=[7] → should be [2,7]")
    print("  R-BPHS47-PATCH-CC30B7               : dasha_lord=Sun → should be Jupiter")
    print("  R-BPHS54-PATCH-3E2164               : antardasha_planet=Mars → should be Moon")
    print("  R-BPHS54-PATCH-3E8999               : antardasha_planet=Mars → should be Rahu")
    print("  R-BPHS54-PATCH-6592D5               : antardasha_planet=Mars → should be Jupiter")
    print("  R-BPHS57-PATCH-0727F5               : ref point 'Ascendant' → should be 'Dasa lord (Saturn)'")
    print()
    print(f"Log saved: {log_path}")
    tee.close()


if __name__ == "__main__":
    main()
