#!/usr/bin/env python3
"""
patch_bphs_vol2_phase1_deferred.py

Patches 49 deferred rules from BPHS Vol 2 Phase 1 triage (2026-06-03).

These are the remaining Bucket C rules (31 genuine_issue + 18 uncertain)
after the API validator pass. All require PDF read of BPHS Vol 2 Santhanam
(Ch.47, 53-58) before final disposition.

Treatment:
  flagged → pending_human_review
  validation.triage_bucket = "deferred"
  validation.api_verdict   = genuine_issue | uncertain
  validation.api_confidence = <float>
  validation.cc_review_note = combined API reasoning + original flag context

Flags count: 56 → 0 after this script + patch_bphs_vol2_phase1_api_bucket_b.py

Dry run by default. Pass --live to apply.

Usage:
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_deferred.py
  MONGO_URL=<url> python3 backend/scripts/patch_bphs_vol2_phase1_deferred.py --live
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR        = Path("KE_TEXTBOOK_DECODE/Dedup_Reports")
TRIAGE_DATE    = "2026-06-03"
TRIAGE_SESSION = "bphs-vol2-ph1-triage-20260603"

# ── 49 deferred rules ─────────────────────────────────────────────────────────
# Format: (rule_id, api_verdict, api_confidence, cc_review_note)
DEFERRED = [
    # ── Ch47 (2) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS47-PATCH-CC30B7", "uncertain", 0.35,
        "BPHS Ch.47 slokas 49-51 context re: Jupiter in 8th during Dasha "
        "cannot be verified without physical source text. Effects (loss of "
        "residential premises, distress to children, loss of cattle) may match "
        "combust Jupiter rule -- needs sloka-level comparison. "
        "Original flag: identical effects to combust Jupiter rule; "
        "lacks 8th house positional nuance.",
    ),
    (
        "R-BPHS47-PATCH-E5CAC4", "genuine_issue", 0.82,
        "API (haiku): Rule conflates natal conjunctional placement (Sun with "
        "5th lord at birth) with dasha-triggered effects. BPHS Ch.47 "
        "addresses natal combinations, not dasha timing -- Sun MD/SD has no "
        "special doctrine for this natal configuration alone. "
        "Original flag: conflates natal chart placement with dasha interpretation.",
    ),
    # ── Ch53 (8) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS53-025", "genuine_issue", 0.85,
        "API (haiku): BPHS maraka doctrine (Ch.49-50) establishes 2nd/7th "
        "lords as death-inflicting based on natal lordship, not dasha timing. "
        "Condition's dasha/antardasha specifications introduce temporal "
        "constraints absent from foundational maraka teaching -- conflates "
        "natal maraka lordship with dasha-period application. "
        "Original flag: conflates Jupiter as maraka lord with Jupiter as "
        "antardasha planet; these are distinct conditions.",
    ),
    (
        "R-BPHS53-PATCH-094A74", "genuine_issue", 0.85,
        "API (haiku): Condition specifies Venus Mahadasha + Moon Antardasha "
        "but rule body claims 'Moon Mahadasha' -- fundamental period mismatch. "
        "BPHS Ch.53 requires dasha-antardasha combination to match exactly. "
        "Note: Ch.53 batch had dasha_lord forced to Venus (batch encoding bug); "
        "this rule may also be affected. "
        "Original flag: antardasha_planet=Moon but summary states Moon MD; "
        "redundant or unclear condition.",
    ),
    (
        "R-BPHS53-PATCH-16C7C5", "uncertain", 0.35,
        "Dasha condition (Venus MD, Moon AD) contradicts summary statement; "
        "apparent mixing of malefic 8th house Saturn with remedial outcomes "
        "(pilgrimages, bathing in holy rivers) requires source confirmation "
        "from BPHS Ch.53 sloka 35. Cannot validate without physical text. "
        "Original flag: Saturn in 8th should produce severe adverse effects, "
        "not spiritual pilgrimages.",
    ),
    (
        "R-BPHS53-PATCH-37CB8C", "genuine_issue", 0.85,
        "API (haiku): Summary and condition specification omit the 2nd house "
        "alternative explicitly stated in detailed text ('2nd or 7th'). "
        "Material inconsistency with source doctrine -- houses_involved should "
        "include [2, 7] not just [7]. "
        "Original flag: summary and condition specify 7th house only; "
        "detailed text says '2nd or 7th'.",
    ),
    (
        "R-BPHS53-PATCH-5E3A16", "uncertain", 0.45,
        "Cannot verify from BPHS Ch.53 slokas 25-28 whether Jupiter in 8th "
        "from Moon assigned identical effects to 12th house placement reflects "
        "authentic BPHS doctrine or KE compilation error. Direct text access "
        "required. "
        "Original flag: identical effects for Jupiter 8th vs 12th from Moon "
        "contradicts classical differentiation of these houses.",
    ),
    (
        "R-BPHS53-PATCH-A460E9", "uncertain", 0.45,
        "Core teaching (Saturn in 7th from Moon → physical distress) plausible "
        "per BPHS doctrine, but structured condition conflates dasha-lord "
        "interpretation with antardasha timing. Cannot verify exact sloka "
        "36-38 without Ch.53 source text. "
        "Original flag: dasha context unclear; potentially misaligned with "
        "classical BPHS phrasing for Saturn 7th from dasha lord.",
    ),
    (
        "R-BPHS53-PATCH-BF3DC0", "genuine_issue", 0.92,
        "API (haiku): BPHS Ch.53 covers dasha phala (results), not remedies. "
        "Mrityunjaya Japa prescriptions are not characteristic Ch.53 doctrine "
        "and appear sourced outside classical BPHS framework. "
        "Original flag: BPHS Ch.53 is dasha phala chapter; Mrityunjaya Japa "
        "appears to be later interpolation or from different source text.",
    ),
    (
        "R-BPHS53-PATCH-E77E96", "genuine_issue", 0.85,
        "API (haiku): Rule conflates Saturn's malefic 2nd house placement "
        "(maraka) with spiritually meritorious outcomes (holy places, bathing). "
        "Dasha condition specifies Venus MD + Moon AD but rule body only "
        "references Saturn in 2nd without integrating dasha lords as required "
        "for predictive synthesis. "
        "Original flag: Saturn in 2nd (maraka) should be inauspicious; "
        "pilgrimages contradict classical maraka doctrine.",
    ),
    # ── Ch54 (7) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS54-061", "uncertain", 0.35,
        "Specific combination (Mercury AD in Mars MD + Mercury as 2nd/7th "
        "lord → critical illness) cannot be verified without direct BPHS Ch.54 "
        "sloka 46-47 text access. Two conditions appear conflated: Mercury as "
        "antardasha lord vs Mercury ruling those houses. "
        "Original flag: Mercury as antardasha lord and Mercury as 2nd/7th house "
        "lord are distinct conditions; rule conflates them without clarification.",
    ),
    (
        "R-BPHS54-PATCH-116D9B", "uncertain", 0.35,
        "Cannot verify from BPHS Ch.54 sloka 67 context whether Sun in 6th vs "
        "12th house effects are intentionally identical or represent "
        "compilation error. Identical effects across 6th and 12th (distinct "
        "dusthanas) is suspicious. "
        "Original flag: Sun 6th effects identical to Sun 12th effects; "
        "6th and 12th have distinct significations in classical Vedic astrology.",
    ),
    (
        "R-BPHS54-PATCH-26A25A", "genuine_issue", 0.85,
        "API (haiku): Ketu in 3rd house traditionally causes obstacles, "
        "separation, and loss in BPHS doctrine. Attributing royal beneficence, "
        "wealth gains, birth of son, government authority directly contradicts "
        "established Ketu malefic principles -- appears fabricated or severely "
        "distorted. "
        "Original flag: Ketu in 3rd → wealth/authority/son contradicts "
        "classical teaching that Ketu in 3rd brings obstacles and separation.",
    ),
    (
        "R-BPHS54-PATCH-3E2164", "genuine_issue", 0.75,
        "API (haiku): Internal condition contradiction -- antardasha_planet is "
        "'Mars' but rule text specifies 'Antardasha of Moon in Dasha of Mars' "
        "(should be antardasha=Moon). Additionally appears nearly identical to "
        "R-BPHS54-PATCH-36FCE5 with minor condition text difference. "
        "Condition encoding error + possible duplicate. "
        "Original flag: nearly identical to R-BPHS54-PATCH-36FCE5; only "
        "'with lord of 4th' added to condition.",
    ),
    (
        "R-BPHS54-PATCH-3E8999", "uncertain", 0.35,
        "Core claim (Rahu in 9th with benefics → government recognition, "
        "property, profits, pilgrimages, foreign travel) plausible for BPHS "
        "Ch.54, but dasha_lord Mars/Mars + static house placement appears "
        "mismatched; benefic association requirement omitted from summary. "
        "Cannot verify sloka 9-10 without source. "
        "Original flag: summary omits 'associated with benefics' qualifier; "
        "condition structure mismatched to static house placement rule.",
    ),
    (
        "R-BPHS54-PATCH-6592D5", "genuine_issue", 0.92,
        "API (haiku): Rule claims Shiva Sahasranam remedies Jupiter's "
        "unfavourable effects, but condition specifies Mars dasha/antardasha "
        "with no Jupiter involvement -- documented logical mismatch between "
        "remedy purpose and planetary condition. "
        "Original flag: Shiva Sahasranam targets Jupiter but condition context "
        "is Mars MD with no Jupiter mentioned anywhere.",
    ),
    (
        "R-BPHS54-PATCH-F1FDFB", "genuine_issue", 0.85,
        "API (haiku): Condition conflates Saturn in 12th house effects with "
        "Mars-Mars period. Flagged duplication of effects between Saturn 8th "
        "and 12th placements suggests fabrication or severe transcription "
        "error not consistent with classical BPHS differentiation. "
        "Original flag: Saturn 12th effects identical to Saturn 8th "
        "(R-BPHS54-PATCH-E84594) -- data integrity violation.",
    ),
    # ── Ch55 (7) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS55-085", "uncertain", 0.35,
        "Cannot verify from BPHS Ch.55 slokas 78-79 whether identical effect "
        "language for Mars in different houses from Rahu (3rd, 9th, 11th) "
        "reflects authentic doctrine or transcription error. All four rules "
        "(R-BPHS55-084 through 087) point to same sloka range. "
        "Original flag: identical effects to R-BPHS55-084 despite Mars in "
        "9th (vs 5th) -- classical sources differentiate by house position.",
    ),
    (
        "R-BPHS55-086", "uncertain", 0.35,
        "Cannot verify from BPHS Ch.55 slokas 78-79 whether identical effect "
        "language for Mars in 3rd from Rahu reflects authentic doctrine. "
        "Identical phrasing across four house positions (084/085/086/087) "
        "is structurally suspicious. "
        "Original flag: identical effects to R-BPHS55-084/085 despite Mars "
        "in 3rd -- suggests possible copy-paste error.",
    ),
    (
        "R-BPHS55-087", "uncertain", 0.35,
        "Cannot verify from BPHS Ch.55 slokas 78-79 whether identical effect "
        "language for Mars in 11th from Rahu reflects authentic doctrine. "
        "Systematic duplication pattern across all four rules in this group. "
        "Original flag: systematic duplication across R-BPHS55-084/085/086/087; "
        "pattern indicates systematic duplication error.",
    ),
    (
        "R-BPHS55-PATCH-3B702B", "genuine_issue", 0.85,
        "API (haiku): Rule condition (Venus-Mars association during Rahu MD) "
        "is mechanically misaligned with its effects text, which appears "
        "copied from a Venus-in-6th-house rule (R-BPHS55-PATCH-330111). "
        "BPHS Ch.55 slokas 51-53 address planetary associations but this "
        "specific conflation lacks coherent textual basis. "
        "Original flag: effect text identical to Venus-in-6th-house rule -- "
        "confirmed copy-paste error.",
    ),
    (
        "R-BPHS55-PATCH-49AF69", "genuine_issue", 0.85,
        "API (haiku): BPHS Ch.55 addresses dashas and planetary periods, not "
        "mantra remedies like Vishnu Sahasranam recitation. Rule conflates "
        "unrelated remedial practices with dasha doctrine and lacks textual "
        "grounding in classical BPHS. "
        "Original flag: Vishnu Sahasranam remedy in Ch.55 dasha phala -- "
        "not characteristic of classical BPHS Chapter 55.",
    ),
    (
        "R-BPHS55-PATCH-4EBC18", "genuine_issue", 0.82,
        "API (haiku): Jupiter in 12th is standard BPHS for losses/expenditure, "
        "but attributing heart disease as specific medical outcome during Rahu "
        "MD appears to be unsupported interpolation not found in BPHS Ch.55 "
        "Santhanam text. "
        "Original flag: heart disease from Jupiter 12th + Rahu MD lacks "
        "clear textual support; medical specificity not characteristic of BPHS.",
    ),
    (
        "R-BPHS55-PATCH-65706D", "genuine_issue", 0.85,
        "API (haiku): Summary overstates a basic maraka principle as a "
        "standalone rule without mandatory Rahu Mahadasha context. BPHS "
        "maraka effects are dasha-dependent, not unconditional. Condition "
        "metadata specifies Rahu MD + Rahu AD but summary omits this entirely. "
        "Original flag: generic maraka principle stated unconditionally; "
        "condition metadata contradicts summary.",
    ),
    (
        "R-BPHS55-PATCH-6AC96A", "genuine_issue", 0.72,
        "API (haiku): BPHS Ch.55 Rahu dasha, but measuring kendra from Rahu "
        "(a shadow/chaya graha) contradicts foundational BPHS doctrine that "
        "kendras are computed from Lagna or Moon. Rule conflates dasha-lordship "
        "with positional geometry. "
        "Original flag: kendra from Rahu (shadow planet) is conceptually "
        "problematic; classical texts measure kendras from Lagna or Moon.",
    ),
    # ── Ch56 (6) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS56-051", "uncertain", 0.35,
        "BPHS Ch.56 sloka 29 cannot be verified without Santhanam Vol 2 text. "
        "Whether this specific Mercury antardasha-end rule is authentic or "
        "mis-extracted requires source confirmation. "
        "Original flag: 'At the end of the Dasha' condition is vague and does "
        "not clearly specify which dasha period is meant.",
    ),
    (
        "R-BPHS56-052", "uncertain", 0.35,
        "BPHS Ch.56 slokas 30-31 require physical text for verification. "
        "Whether Mercury as 2nd/7th lord during Jupiter MD → premature death "
        "is authentic BPHS doctrine or a validator over-statement of severity "
        "requires source confirmation. "
        "Original flag: 'premature death' is extreme outcome; needs sloka "
        "verification to confirm BPHS prescribes death vs severe hardship.",
    ),
    (
        "R-BPHS56-055", "genuine_issue", 0.85,
        "API (haiku): Logical contradiction -- benefic association/aspect on "
        "Ketu should mitigate negative effects per BPHS principle, yet outcome "
        "(coarse food at death ceremonies) remains decidedly negative despite "
        "the 'favourable' condition. Suggests misinterpretation of source "
        "sloka 32 or fabrication. "
        "Original flag: Ketu with benefic aspect yet negative effect -- "
        "contradicts classical principle that benefic aspects reduce malefic results.",
    ),
    (
        "R-BPHS56-056", "genuine_issue", 0.85,
        "API (haiku): Benefic association on Ketu should mitigate negative "
        "outcomes; marking as 'dasha_unfavourable' with negative effect "
        "contradicts stated favourable condition. Same structural contradiction "
        "as R-BPHS56-055 (same sloka 32). "
        "Original flag: condition states Ketu associated with benefics; "
        "effect is adverse -- condition-effect contradiction.",
    ),
    (
        "R-BPHS56-PATCH-AEBB42", "genuine_issue", 0.92,
        "API (haiku): Ketu (shadow planet/node) cannot be a house lord in "
        "BPHS Saptarishi doctrine -- only the 7 classical planets (Sun-Saturn) "
        "rule houses under Parasara's scheme. Condition 'Ketu is 2nd house "
        "lord' is impossible within the BPHS doctrinal framework. "
        "Note: modern KP tradition assigns Ketu as Scorpio co-ruler (e.g., "
        "Libra Ascendant 2nd lord) but this post-Parasara addition is NOT "
        "part of classical BPHS. Condition needs re-encoding to 'Ketu placed "
        "in 2nd house'. "
        "Original flag: Ketu cannot be lord of any house in classical "
        "Vedic astrology.",
    ),
    (
        "R-BPHS56-PATCH-D0BAEB", "genuine_issue", 0.85,
        "API (haiku): Rule conflates Sun in 6th house effects (nervous disorder, "
        "fever, laziness, sins, antagonism) with Sun in 12th house placement. "
        "BPHS 56:54-55 treats these distinctly -- 12th house Sun produces "
        "losses, isolation, and expenditure rather than fever/nervous disorders. "
        "Original flag: Sun 12th rule reuses Sun 6th house effects text -- "
        "textually incorrect per BPHS Ch.56 sloka 54-55.",
    ),
    # ── Ch57 (9) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS57-029", "uncertain", 0.35,
        "Cannot verify BPHS Ch.57 sloka 20-21 content or exact Santhanam "
        "translation wording without physical text. Translation anomalies "
        "'Coarse fool' (likely 'Coarse food' -- a standard classical hardship) "
        "and 'dysentry' (misspelling of 'dysentery') warrant PDF verification. "
        "Content may be valid with text correction. "
        "Original flag: 'Coarse fool' archaic/unclear; 'dysentry' misspelling; "
        "phrasing suggests OCR or translation error.",
    ),
    (
        "R-BPHS57-033", "uncertain", 0.35,
        "Cannot verify BPHS Ch.57 sloka 20-21 Ketu-12th effects without "
        "physical text. Same translation anomalies as R-BPHS57-029: 'Coarse "
        "fool' and 'dysentry' need PDF confirmation. Content may be valid "
        "with text correction. "
        "Original flag: same OCR/translation issues as R-BPHS57-029; "
        "Ketu 8th and 12th both point to same sloka range.",
    ),
    (
        "R-BPHS57-098", "uncertain", 0.35,
        "Cannot confirm from BPHS Ch.57 slokas 61-62 whether rule describes "
        "Mars in 2nd house (occupant), Mars as 2nd lord, or combined condition "
        "without source text access. "
        "Original flag: 'Mars in 2nd house' and 'Mars as 2nd lord' are "
        "distinct conditions; rule summary conflates them.",
    ),
    (
        "R-BPHS57-PATCH-0727F5", "uncertain", 0.35,
        "Cannot verify from BPHS Ch.57 slokas 28-29 whether Venus in 8th "
        "from Ascendant (not from Saturn) is the correct reference frame or "
        "if the flag applies. Some BPHS chapters do use Ascendant-based "
        "house positions for dasha result rules. "
        "Original flag: should be '8th from Saturn dasha lord' not '8th from "
        "Ascendant' -- reference frame inconsistency in dasha context.",
    ),
    (
        "R-BPHS57-PATCH-37B401", "uncertain", 0.35,
        "Cannot verify from BPHS Ch.57 slokas 81-82 whether Saturn AD + "
        "Jupiter lordship + Shiva Sahasranama remedy combination is "
        "authentically sourced. Summary omits Jupiter lord qualifier. "
        "Original flag: remedy lacks specificity; 'above evil effects' is "
        "vague; condition omits Jupiter 2nd/7th lord requirement in summary.",
    ),
    (
        "R-BPHS57-PATCH-562548", "genuine_issue", 0.78,
        "API (haiku): Rule conflates natal Venus placement with dasha effects "
        "without clarifying whether Venus functions as antardasha lord, natal "
        "significator, or transit point. BPHS Ch.57 dasha effects require "
        "explicit planetary period hierarchy. "
        "Original flag: Venus role in Saturn MD unclear -- antardasha planet, "
        "natal house placement, or transit point?",
    ),
    (
        "R-BPHS57-PATCH-5C3BA0", "genuine_issue", 0.85,
        "API (haiku): Mercury in 6th house (dusthana) yielding 'kingdom' and "
        "'village headship' contradicts core BPHS doctrine on dusthana effects. "
        "Saturn-Saturn dasha/antardasha specification appears inconsistent. "
        "Flagged contradiction with R-BPHS57-PATCH-55C3E1 suggests conflation "
        "or source misattribution. "
        "Original flag: Mercury 6th → kingdom contradicts inauspicious house "
        "doctrine; duplicates 12th house effects from another rule.",
    ),
    (
        "R-BPHS57-PATCH-7C33F5", "genuine_issue", 0.78,
        "API (haiku): Benefic aspect on Ketu producing evil effects (loss of "
        "position, poverty, distress) contradicts BPHS principle that benefic "
        "aspects mitigate malefic planetary results. Logical inconsistency "
        "suggests fabrication or misinterpretation of source text. "
        "Note: Ketu in Saturn MD is inherently malefic, but BPHS states "
        "benefic aspect softens (does not reverse) results. Needs Ch.57 "
        "sloka 16-18 PDF verification. "
        "Original flag: Ketu aspected by benefics yet 'evil effects' stated -- "
        "contradicts classical mitigation principle.",
    ),
    (
        "R-BPHS57-PATCH-AA4529", "genuine_issue", 0.72,
        "API (haiku): Rule conflates Ketu's intrinsic malefic nature with sign "
        "dignity. BPHS teaches Ketu as inherently inauspicious regardless of "
        "benefic placement; using 'friendly_sign' as a meaningful modifier "
        "implies sign matters for Ketu -- the doctrine does not hinge on sign "
        "beneficence. Needs Ch.57 sloka 16-18 PDF verification. "
        "Original flag: 'Ketu in benefic sign' condition label conflicts with "
        "adverse outcome -- condition and effect contradictory.",
    ),
    (
        "R-BPHS57-PATCH-B89C62", "genuine_issue", 0.92,
        "API (haiku): Rahu has no own sign rulership in classical BPHS "
        "Saptarishi doctrine. Shadow planets are evaluated by exaltation/"
        "debilitation and placement, not sign ownership. "
        "'dignity_state: own_sign' is inapplicable to Rahu. "
        "Note: modern tradition assigns Aquarius to Rahu -- not Parasara's "
        "system. If the underlying BPHS sloka 65-67 describes auspicious "
        "Rahu results, re-encode condition using 'exaltation' or "
        "'friendly_sign' dignity state instead of 'own_sign'. "
        "Original flag: Rahu does not have own sign in classical Vedic "
        "astrology; condition encoding is inapplicable to shadow planets.",
    ),
    (
        "R-BPHS57-PATCH-C5E9B2", "genuine_issue", 0.82,
        "API (haiku): Ketu associated with benefics producing only malefic "
        "results contradicts BPHS principle that benefic influences mitigate "
        "malefic planetary effects. Condition-effect mapping is logically "
        "incoherent. Same structural issue as R-BPHS57-PATCH-7C33F5 and "
        "AA4529 -- all three reference Ch.57 sloka 16-18. "
        "Original flag: benefic association with Ketu still produces evil "
        "effects -- contradicts mitigation principle.",
    ),
    # ── Ch58 (7) ──────────────────────────────────────────────────────────────
    (
        "R-BPHS58-PATCH-313295", "genuine_issue", 0.85,
        "API (haiku): Jupiter (natural benefic) in 2nd house producing "
        "'physical distress' during Mercury MD contradicts BPHS doctrine that "
        "2nd house maraka effects derive from malefics or debilitated planets, "
        "not benefics. Condition conflates Jupiter placement with Mercury dasha "
        "without clear BPHS Ch.58 textual basis. "
        "Original flag: Jupiter in 2nd → distress contradicts benefic nature; "
        "maraka effects attributed to malefics, not Jupiter.",
    ),
    (
        "R-BPHS58-PATCH-36ADF5", "genuine_issue", 0.85,
        "API (haiku): Jupiter in 7th house producing 'physical distress' during "
        "Mercury MD contradicts classical BPHS -- Jupiter's 7th placement yields "
        "marriage/partnership effects, not distress. Maraka principles apply "
        "to malefics or specific yogas, not Jupiter alone. "
        "Original flag: Jupiter in 7th causing distress contradicts benefic "
        "nature; 7th maraka effects are attributed to malefics.",
    ),
    (
        "R-BPHS58-PATCH-3B1F8A", "genuine_issue", 0.85,
        "API (haiku): Internal logical contradiction -- detailed description "
        "references 'Mars is maraka lord' while condition JSON specifies only "
        "Mercury dasha/antardasha with no Mars involvement. Remedy application "
        "is incoherent and not traceable to standard BPHS Ch.58 doctrine. "
        "Original flag: remedy references 'Mars is maraka lord' but condition "
        "context specifies Mercury MD/AD only -- no Mars anywhere in condition.",
    ),
    (
        "R-BPHS58-PATCH-6DAB01", "genuine_issue", 0.82,
        "API (haiku): BPHS Ch.58 (Jupiter effects) documents Jupiter as 7th "
        "lord producing marital discord, spouse loss, or death -- not vague "
        "'physical distress'. Rule conflates maraka dignity with a non-standard "
        "outcome; lacks specificity on partner/mortality outcomes expected "
        "in classical doctrine. "
        "Original flag: Jupiter as 7th lord = 'physical distress' too vague; "
        "BPHS specifies marital/death effects for maraka Jupiter.",
    ),
    (
        "R-BPHS58-PATCH-707AC3", "genuine_issue", 0.72,
        "API (haiku): Moon as 7th lord (maraka) in BPHS Ch.58 typically "
        "produces marital/death effects, not vague 'physical distress'. "
        "Rule conflates symptom with cause and lacks specificity on "
        "partner/mortality outcomes. Structurally identical to "
        "R-BPHS58-PATCH-60DC91 but different house. "
        "Original flag: Moon as 7th lord = 'physical distress' too vague; "
        "identical structure to R-BPHS58-PATCH-60DC91.",
    ),
    (
        "R-BPHS58-PATCH-9B332B", "genuine_issue", 0.85,
        "API (haiku): Rahu in 8th house is classically malefic (longevity, "
        "hidden matters, sudden loss). Attributing positive 'meeting "
        "dignitaries' outcomes during Mercury AD lacks textual support in "
        "BPHS Ch.58 and contradicts established 8th house principles. "
        "Original flag: Rahu in 8th yielding 'opportunity to meet king/high "
        "dignitaries' contradicts classical malefic 8th house doctrine.",
    ),
    (
        "R-BPHS58-PATCH-D5766C", "uncertain", 0.35,
        "Positive effects from Ketu-Ascendant lord conjunction cannot be "
        "verified without BPHS Ch.58 slokas 6-8. Condition metadata references "
        "Mercury dasha/antardasha (unrelated to the stated Ketu-Ascendant "
        "conjunction) -- suggests possible data corruption in encoding. "
        "Original flag: Ketu conjunction with Ascendant lord → positive "
        "results contradicts classical Ketu malefic doctrine; BPHS Ch.58 "
        "does not attribute such results.",
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
    log_path = LOG_DIR / f"patch_bphs_vol2_phase1_deferred_{ts}_{mode}.log"
    tee      = _Tee(log_path)
    sys.stdout = tee

    print("=" * 70)
    print(f"  LOG FILE: {log_path}")
    print("=" * 70)
    print()
    print("BPHS Vol 2 Phase 1 -- Deferred Rules Patch")
    print(f"Mode    : {'🔴 LIVE -- WRITING TO DB' if args.live else '🟡 DRY RUN -- no changes'}")
    print(f"Rules   : {len(DEFERRED)}")
    print(f"Action  : flagged → pending_human_review + triage_bucket 'deferred'")
    print(f"Notes   : API verdict + original flag reason embedded per rule")
    print(f"Next    : PDF read of BPHS Vol 2 Santhanam Ch.47, 53-58")
    print()

    # Chapter distribution
    ch_counts = {}
    for (rule_id, _, _, _) in DEFERRED:
        parts = rule_id.split("-")
        if len(parts) >= 3:
            ch = parts[1]  # e.g. BPHS47, BPHS53, etc.
            ch_counts[ch] = ch_counts.get(ch, 0) + 1
    print("Chapter distribution:")
    for ch, cnt in sorted(ch_counts.items()):
        print(f"  {ch}: {cnt} rules")
    print()

    from pymongo import MongoClient
    col = MongoClient(args.mongo_url, serverSelectionTimeoutMS=10_000)[
        args.db_name]["interpretation_rules"]

    now     = datetime.now(timezone.utc)
    patched = 0
    skipped = 0
    errors  = []

    genuine_count   = sum(1 for _, v, _, _ in DEFERRED if v == "genuine_issue")
    uncertain_count = sum(1 for _, v, _, _ in DEFERRED if v == "uncertain")
    print(f"  genuine_issue : {genuine_count}")
    print(f"  uncertain     : {uncertain_count}")
    print()
    print(f"{'#':<4} {'Rule ID':<45} {'Pre-status':<22} Result")
    print("─" * 90)

    for i, (rule_id, verdict, confidence, note) in enumerate(DEFERRED, 1):
        existing = col.find_one({"rule_id": rule_id},
                                {"approval_status": 1, "_id": 1})
        if not existing:
            print(f"  {i:<4} {rule_id:<45} {'NOT FOUND':<22} ⚠️  SKIP")
            errors.append(f"{rule_id}: not found in DB")
            skipped += 1
            continue

        pre_status = existing.get("approval_status", "?")
        if pre_status != "flagged":
            print(f"  {i:<4} {rule_id:<45} {pre_status:<22} ⏭  SKIP (not flagged)")
            skipped += 1
            continue

        update_doc = {
            "$set": {
                "approval_status":              "pending_human_review",
                "validation.triage_bucket":     "deferred",
                "validation.api_verdict":       verdict,
                "validation.api_confidence":    confidence,
                "validation.api_model":         "claude-haiku-4-5",
                "validation.cc_review_note":    note,
                "validation.triage_date":       TRIAGE_DATE,
                "validation.triage_session":    TRIAGE_SESSION,
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

        print(f"  {i:<4} {rule_id:<45} {pre_status:<22} {status}")

    print()
    print("=" * 70)
    print("Summary")
    print(f"  Mode    : {'LIVE' if args.live else 'DRY RUN'}")
    print(f"  Patched : {patched} / {len(DEFERRED)}")
    print(f"  Skipped : {skipped}")
    if errors:
        print(f"  Errors  : {len(errors)}")
        for e in errors:
            print(f"    {e}")
    print()
    print("NEXT STEPS:")
    print("  1. Run patch_bphs_vol2_phase1_api_bucket_b.py --live (if not done)")
    print("  2. Vol 2 Phase 1 flagged count = 0 after both scripts run")
    print("  3. PDF read BPHS Vol 2 Santhanam Ch.47, 53-58 to resolve these 49")
    if not args.live:
        print()
        print("  Re-run with --live to apply.")
    print()
    print(f"Log saved: {log_path}")
    tee.close()


if __name__ == "__main__":
    main()
