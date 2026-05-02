#!/usr/bin/env python3
"""
ingest_bphs_ch41_v1.py — BPHS Chapter 41: Yogas for Wealth (Combinations for Wealth)

49 rules total across 6 groups:
   7  Wealth Axis Yogas       (Slokas 2–8)   — 5th/11th lord in own sign axis
   7  Own-Sign Lagna Yogas    (Slokas 9–15)  — planet in own sign in 1st + activation
   2  General Principles      (Slokas 16–17) — 5th/9th lords as Lakshmi; strength validation
   8  Angular Lord Varga      (Slokas 18–19) — 8 Amsa tiers × angular lord
   8  5th Lord Varga          (Slokas 20–22) — 8 Amsa tiers × 5th lord
   8  9th Lord Varga          (Slokas 23–27) — 8 Amsa tiers × 9th lord
   9  Rajayoga Varga          (Slokas 28–34) — relationship framework + 8 Amsa tiers

Hard-coded from PDF + Notebook LM decode — zero AI extraction cost.
Checkable: 14 / 49 (29%) — Slokas 2–15 are pure positional checks.
  Slokas 2–15  → checkable: True  (planetary_combination; no Jaimini, no Varga)
  Slokas 16–17 → checkable: False (general interpretive principles)
  Slokas 18–34 → checkable: False (Varga/divisional chart computation required)

Blocker legend:
  V = Divisional chart (Varga) computation required (D-9 Navamsa, D-10 Dashamsa etc.)
  L = House lord identification required
  A = Aspect detection required (Parashari aspects)
  D = Dignity / strength check required

Standard --save / --upload workflow:
  Step 1 — Dry run:
    python3 scripts/ingest_bphs_ch41_v1.py --dry-run --save scripts/bphs_ch41_rules.json

  Step 2 — Review bphs_ch41_rules.json; amend as needed.

  Step 3 — Upload (zero API calls):
    python3 scripts/ingest_bphs_ch41_v1.py \\
      --upload scripts/bphs_ch41_rules.json \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db

  Step 4 — Validate:
    python3 scripts/validate_rules.py \\
      --mongo-url "$MONGO_URL" --db-name horoscope_db \\
      --batch-id bphs-ch41-v1-20260502
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────

SCIENCE   = "jyotish"
BOOK      = "Brihat Parashara Hora Shastra"
BOOK_ID   = "bphs"
CHAPTER   = 41
CHAP_NAME = "Yogas for Wealth"
BATCH_ID  = "bphs-ch41-v1-20260502"

# ── Yoga source data ──────────────────────────────────────────────────────────

YOGA_DATA: list[dict] = [

    # ═══════════════════════════════════════════════════════════════════════════
    # 1. WEALTH AXIS YOGAS — 5th/11th house lords in own signs (Slokas 2–8)
    #
    # Core pattern: the 5th lord must be in the 5th in its own sign, while the
    # 11th lord (or specific planets) must be in the 11th. For Sloka 3 the 11th
    # additionally requires Moon, Mars AND Jupiter. These are ascendant-specific:
    # the 5th and 11th lords in own sign is only possible for certain ascendants.
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Venus-Mars Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-02",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "A sign of Venus is the 5th house (Taurus or Libra is the 5th), "
            "Venus is in that 5th house (own sign), and Mars is in the 11th house. "
            "Applicable ascendants: Capricorn (5th = Taurus, 11th = Scorpio; "
            "both Venus and Mars are in their own signs) and Gemini (5th = Libra, "
            "11th = Aries; both again in own signs). The formula: 5th lord and "
            "11th lord are both in their own houses."
        ),
        "effect":         (
            "The native will obtain great riches. The mutual own-sign occupation "
            "of the 5th (Purva Punya, intelligence, speculative gains) and 11th "
            "(income, fulfilment of desires) by their respective lords is the "
            "strongest wealth indicator in this chapter."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Ascendant-specific positional check: Venus in 5th house + Mars "
                "in 11th house. Valid for Capricorn and Gemini ascendants where "
                "both planets are automatically in own signs. Pure house position "
                "verification — no Jaimini or Varga required."
            ),
        },
    },
    {
        "yoga_name":      "Mercury-Jupiter-Moon-Mars Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-03",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "A sign of Mercury is the 5th house (Gemini or Virgo is the 5th), "
            "Mercury is in that 5th house (own sign), AND the 11th house is "
            "simultaneously occupied by the Moon, Mars AND Jupiter — all three "
            "must be in the 11th. Applicable ascendants: Aquarius (5th = Gemini, "
            "11th = Sagittarius — Jupiter in own sign there, with Moon and Mars) "
            "and Taurus (5th = Virgo, 11th = Pisces — Jupiter in own sign there, "
            "with Moon and Mars). The Taurus case is described as 'quite superior'."
        ),
        "effect":         (
            "The native will be very affluent. This yoga is exceptional because "
            "the 11th house requires three occupants (Moon, Mars, Jupiter) in "
            "addition to Mercury's own-sign placement in the 5th — a rare and "
            "highly specific combination."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Mercury in 5th house + Moon, Mars, and Jupiter "
                "all in 11th house. Valid for Aquarius and Taurus ascendants. "
                "All four planet positions are standard house checks — no Jaimini "
                "or Varga required."
            ),
        },
    },
    {
        "yoga_name":      "Sun-Saturn-Moon-Jupiter Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-04",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Leo is the 5th house (Aries ascendant) and the Sun (lord of Leo) "
            "is placed in the 5th in his own sign, while Saturn, the Moon and "
            "Jupiter are all in the 11th house. For Aries ascendant: 5th = Leo "
            "(Sun's own), 11th = Aquarius (Saturn's own sign — Saturn occupies "
            "11th as its owner along with Moon and Jupiter)."
        ),
        "effect":         (
            "The native will be very affluent. The Sun in its own royal sign in "
            "the 5th, combined with Saturn in its own sign in the 11th (along "
            "with Moon and Jupiter), creates a powerful wealth axis."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income", "leadership"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Sun in 5th house + Saturn, Moon, and Jupiter "
                "all in 11th house. Valid for Aries ascendant where 5th = Leo "
                "and 11th = Aquarius. Pure house position check — no Jaimini "
                "or Varga required."
            ),
        },
    },
    {
        "yoga_name":      "Saturn-Sun-Moon Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-05",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Saturn is in the 5th in its own sign (Capricorn or Aquarius is the "
            "5th house), and the Sun and Moon are both in the 11th house. "
            "Applicable ascendants: Virgo (5th = Capricorn, Saturn's own; 11th = "
            "Cancer, Sun and Moon there) and Libra (5th = Aquarius, Saturn's own; "
            "11th = Leo, Sun and Moon there). Both the Sun and Moon must jointly "
            "occupy the 11th."
        ),
        "effect":         (
            "The native will be very affluent. Saturn — a natural malefic — in "
            "its own sign in the 5th becomes a powerful wealth-giver when paired "
            "with the Sun (authority) and Moon (prosperity) in the 11th."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Saturn in 5th house + Sun and Moon in 11th "
                "house. Valid for Virgo ascendant (5th=Capricorn, 11th=Cancer) "
                "and Libra ascendant (5th=Aquarius, 11th=Leo). Pure house "
                "position checks — no Jaimini or Varga required."
            ),
        },
    },
    {
        "yoga_name":      "Jupiter-Mercury Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-06",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Jupiter is in the 5th in its own sign (Sagittarius or Pisces is "
            "the 5th house), and Mercury is in the 11th house. Applicable "
            "ascendants: Leo (5th = Sagittarius — Jupiter's own; 11th = Gemini "
            "— Mercury's own sign, so Mercury is also in own sign) and Scorpio "
            "(5th = Pisces — Jupiter's own; 11th = Virgo — Mercury's own, again "
            "mutual own-sign occupation). The 5th and 11th lords are both in "
            "their own houses."
        ),
        "effect":         (
            "The native will be very affluent. Jupiter (great benefic, wisdom, "
            "expansion) in its own 5th and Mercury (intelligence, commerce, "
            "communication) in its own 11th creates a potent material-intellectual "
            "wealth axis."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Jupiter in 5th house + Mercury in 11th house. "
                "Valid for Leo ascendant (5th=Sagittarius, 11th=Gemini) and "
                "Scorpio ascendant (5th=Pisces, 11th=Virgo). Pure house position "
                "checks — no Jaimini or Varga required."
            ),
        },
    },
    {
        "yoga_name":      "Mars-Venus Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-07",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "A sign of Mars is the 5th house (Aries or Scorpio is the 5th), "
            "Mars is in the 5th in its own sign, and Venus is in the 11th house. "
            "Applicable ascendants: Cancer (5th = Scorpio — Mars's own; 11th = "
            "Taurus — Venus's own, so Venus also in own sign) and Sagittarius "
            "(5th = Aries — Mars's own; 11th = Libra — Venus's own). Both lords "
            "occupy their own houses."
        ),
        "effect":         (
            "The native will become very affluent. Mars (drive, courage, action) "
            "in own sign in the 5th and Venus (wealth, luxury, beauty) in own "
            "sign in the 11th creates a complementary axis of desire and "
            "fulfilment."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Mars in 5th house + Venus in 11th house. "
                "Valid for Cancer ascendant (5th=Scorpio, 11th=Taurus) and "
                "Sagittarius ascendant (5th=Aries, 11th=Libra). Pure house "
                "position checks — no Jaimini or Varga required."
            ),
        },
    },
    {
        "yoga_name":      "Moon-Saturn Wealth Axis — 5th/11th Own-Sign",
        "sloka":          "ch41-sloka-08",
        "group":          "wealth_axis_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Cancer is the 5th house (Pisces ascendant), the Moon is placed in "
            "the 5th in Cancer (her own sign), and Saturn is in the 11th house. "
            "For Pisces ascendant: 5th = Cancer (Moon's own); 11th = Capricorn "
            "(Saturn's own sign, so Saturn is in own sign in 11th). The Moon "
            "in 5th and Saturn in 11th complete the symmetric own-sign axis."
        ),
        "effect":         (
            "The native will become very affluent. The Moon (nourishment, "
            "prosperity, mind) in her own Cancer in the 5th and Saturn (discipline, "
            "endurance, karma) in its own Capricorn in the 11th form the final "
            "wealth axis in this set — applicable to Pisces ascendant."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "income"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Moon in 5th house + Saturn in 11th house. "
                "Valid for Pisces ascendant (5th=Cancer, 11th=Capricorn). "
                "Pure house position checks — no Jaimini or Varga required."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 2. OWN-SIGN LAGNA YOGAS — planet in own sign in 1st + activation (Slokas 9–15)
    #
    # Core pattern: the planet that rules the ascendant sign is placed in the
    # ascendant itself (own sign in 1st house) AND is conjunct or aspected by
    # specific activating planets. The combination produces wealth of varying
    # degrees (great riches → wealthy → rich).
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Sun Wealth Engine — Leo Ascendant Own-Sign",
        "sloka":          "ch41-sloka-09",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "The Sun is in Leo, and Leo is the ascendant (i.e., the Sun is in "
            "the 1st house in its own sign). The Sun must be conjunct or aspected "
            "by both Mars and Jupiter simultaneously. All three — Sun in Leo "
            "Lagna, Mars's influence, and Jupiter's influence — must hold."
        ),
        "effect":         (
            "The native will be wealthy. The Sun in its own royal sign Leo in "
            "the ascendant, energised by Mars (action, initiative) and Jupiter "
            "(expansion, fortune), combines authority with enterprise and wisdom "
            "to produce lasting wealth."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "status"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Sun in 1st house (Leo ascendant) + Mars and "
                "Jupiter conjunct or aspecting the Sun. Conjunction branch is a "
                "same-house check. Full aspect detection enhances precision. "
                "Valid for Leo ascendant only."
            ),
        },
    },
    {
        "yoga_name":      "Moon Wealth Engine — Cancer Ascendant Own-Sign",
        "sloka":          "ch41-sloka-10",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "The Moon is in Cancer, and Cancer is the ascendant (Moon in 1st "
            "house in own sign). The Moon must be conjunct or aspected by both "
            "Mercury and Jupiter simultaneously. All three influences must hold."
        ),
        "effect":         (
            "The native will be wealthy. The Moon in her own Cancer ascendant, "
            "activated by Mercury (intelligence, commerce) and Jupiter (wisdom, "
            "fortune), blends emotional intelligence with discernment and "
            "philosophical prosperity."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Moon in 1st house (Cancer ascendant) + "
                "Mercury and Jupiter conjunct or aspecting the Moon. "
                "Conjunction branch is same-house check. Valid for Cancer "
                "ascendant only."
            ),
        },
    },
    {
        "yoga_name":      "Mars Wealth Engine — Aries/Scorpio Ascendant Own-Sign",
        "sloka":          "ch41-sloka-11",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Mars is in the ascendant in its own sign (Aries or Scorpio is the "
            "ascendant and Mars is placed there). Mars must be conjunct or "
            "aspected by Mercury, Venus AND Saturn — all three activating planets "
            "must influence Mars."
        ),
        "effect":         (
            "The native will be rich. Mars in its own forceful sign in the "
            "ascendant, receiving the combined influence of Mercury (skill, "
            "intellect), Venus (wealth, art) and Saturn (industry, discipline), "
            "channels fiery energy into productive material enterprise."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Mars in 1st house (Aries or Scorpio ascendant) "
                "+ Mercury, Venus, and Saturn all conjunct or aspecting Mars. "
                "Conjunction branch is same-house check. Valid for Aries and "
                "Scorpio ascendants."
            ),
        },
    },
    {
        "yoga_name":      "Mercury Wealth Engine — Gemini/Virgo Ascendant Own-Sign",
        "sloka":          "ch41-sloka-12",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Mercury is in the ascendant in its own sign (Gemini or Virgo is "
            "the ascendant and Mercury is placed there). Mercury must be conjunct "
            "or aspected by both Saturn and Jupiter simultaneously."
        ),
        "effect":         (
            "The native will be rich. Mercury in its own analytical or communicative "
            "sign in the ascendant, activated by Saturn (discipline, longevity) "
            "and Jupiter (wisdom, expansion), produces wealth through intellectual "
            "and commercial enterprise."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Mercury in 1st house (Gemini or Virgo ascendant) "
                "+ Saturn and Jupiter conjunct or aspecting Mercury. Conjunction "
                "branch is same-house check. Valid for Gemini and Virgo ascendants."
            ),
        },
    },
    {
        "yoga_name":      "Jupiter Wealth Engine — Sagittarius/Pisces Ascendant Own-Sign",
        "sloka":          "ch41-sloka-13",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Jupiter is in the ascendant in its own sign (Sagittarius or Pisces "
            "is the ascendant and Jupiter is placed there). Jupiter must be "
            "conjunct or aspected by both Mercury and Mars simultaneously."
        ),
        "effect":         (
            "The native will be rich. Jupiter in its own expansive sign in the "
            "ascendant, energised by Mercury (wit, commerce) and Mars (initiative, "
            "drive), combines philosophical wisdom with practical action to generate "
            "wealth."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Jupiter in 1st house (Sagittarius or Pisces "
                "ascendant) + Mercury and Mars conjunct or aspecting Jupiter. "
                "Conjunction branch is same-house check. Valid for Sagittarius "
                "and Pisces ascendants."
            ),
        },
    },
    {
        "yoga_name":      "Venus Wealth Engine — Taurus/Libra Ascendant Own-Sign",
        "sloka":          "ch41-sloka-14",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Venus is in the ascendant in its own sign (Taurus or Libra is the "
            "ascendant and Venus is placed there). Venus must be conjunct or "
            "aspected by both Saturn and Mercury simultaneously."
        ),
        "effect":         (
            "The native will be wealthy. Venus in its own sign of beauty or "
            "balance in the ascendant, refined by Saturn (industry, structure) "
            "and Mercury (intelligence, trade), creates wealth through artistic, "
            "diplomatic or commercial channels."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "luxury"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Venus in 1st house (Taurus or Libra ascendant) "
                "+ Saturn and Mercury conjunct or aspecting Venus. Conjunction "
                "branch is same-house check. Valid for Taurus and Libra ascendants."
            ),
        },
    },
    {
        "yoga_name":      "Saturn Wealth Engine — Capricorn/Aquarius Ascendant Own-Sign",
        "sloka":          "ch41-sloka-15",
        "group":          "own_sign_lagna_yoga",
        "condition_type": "yoga_combination",
        "formation":      (
            "Saturn is in the ascendant in its own sign (Capricorn or Aquarius "
            "is the ascendant and Saturn is placed there). Saturn must be conjunct "
            "or aspected by both Mars and Jupiter simultaneously. Despite Mars "
            "being a natural malefic and Jupiter being a natural benefic and "
            "Jupiter being Saturn's adversary by natural disposition, both are "
            "required as activating planets for this specific combination."
        ),
        "effect":         (
            "The native will be wealthy. Saturn in its own disciplined or idealistic "
            "sign in the ascendant, energised by Mars (action, courage) and Jupiter "
            "(wisdom, fortune), produces wealth through sustained effort and "
            "structural discipline."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "karma"],
        "yoga_check": {
            "type":        "planetary_combination",
            "checkable":   True,
            "description": (
                "Positional check: Saturn in 1st house (Capricorn or Aquarius "
                "ascendant) + Mars and Jupiter conjunct or aspecting Saturn. "
                "Conjunction branch is same-house check. Noteworthy: Mars+Jupiter "
                "required despite natural enmity with Saturn — exact as stated "
                "in text. Valid for Capricorn and Aquarius ascendants."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 3. GENERAL PRINCIPLES (Slokas 16–17)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "5th and 9th Lords as Primary Wealth Significators",
        "sloka":          "ch41-sloka-16",
        "group":          "general_principle",
        "condition_type": "general_principle",
        "formation":      (
            "The 9th lord and the 5th lord are capable of bestowing wealth — "
            "they are the primary Lakshmi significators in any chart. Furthermore, "
            "any planet that conjoins the 5th lord or the 9th lord effectively "
            "'borrows' their wealth-giving status. Such a conjoining planet will "
            "also bestow wealth during its own Dasa (major planetary period)."
        ),
        "effect":         (
            "The 5th and 9th lords are the principal givers of wealth in any "
            "horoscope. Planets conjoining them become secondary wealth significators "
            "and give material prosperity during their Dasa periods. This principle "
            "extends the reach of wealth yogas beyond the primary lord pairs — "
            "any well-placed planet in conjunction with these lords participates "
            "in wealth delivery. Lakshmi is said to reside in the 5th and 9th "
            "houses."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "prosperity", "fortune", "dharma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["L"],
            "description": (
                "General interpretive principle requiring 5th and 9th lord "
                "identification. Applied as a Dasa-timing and conjunction-context "
                "rule during chart reading, not a single-configuration check. "
                "Phase 2: flagging planets conjunct 5th/9th lord as secondary "
                "Dasa wealth triggers becomes automatable once lord identification "
                "is available."
            ),
        },
    },
    {
        "yoga_name":      "Strength Validation — All Wealth Yogas Require Planetary Dignity",
        "sloka":          "ch41-sloka-17",
        "group":          "general_principle",
        "condition_type": "general_principle",
        "formation":      (
            "All the yogas mentioned in this chapter (slokas 2–16) must be "
            "delineated only after knowing the favourable and unfavourable "
            "dispositions of the participating planets and their strength and "
            "weakness. A yoga may exist technically in the chart but will not "
            "manifest if the participant planets are afflicted, debilitated, "
            "combust or otherwise weakened."
        ),
        "effect":         (
            "A yoga exists in the chart but only manifests if the participant "
            "planets possess adequate strength. If any key planet is weak — "
            "debilitated, combust, in enemy sign, or heavily aspected by malefics "
            "— the wealth yoga is diminished or denied despite the positional "
            "configuration being present. Strength evaluation is the mandatory "
            "final gate before any wealth yoga is confirmed."
        ),
        "is_benefic":     True,
        "life_domains":   ["wealth", "general"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["D"],
            "description": (
                "Meta-rule: applies as a validation gate over all Ch 41 yogas. "
                "Requires planetary strength assessment (dignity, combustion, "
                "aspect state) — a compound dignity check (D blocker). Phase 2: "
                "integrate as a post-yoga-detection strength modifier that "
                "reduces confidence score when participant planets are debilitated "
                "or combust."
            ),
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 4. ANGULAR LORD VARGA DIGNITIES (Slokas 18–19)
    #
    # The lord of any angular house (1st, 4th, 7th, 10th) placed in one of the
    # 8 Amsa dignity tiers produces the corresponding outcome. The 4 angular
    # lords are powerful in ascending order: 1st < 4th < 7th < 10th, so the
    # same dignity level produces stronger effects for the 10th lord than for
    # the 1st lord. Treatment is based on Dasa Varga (10-divisional chart set).
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Angular Lord in Parijatamsa — Liberal",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th house) is in "
            "Parijatamsa — the first tier of the Dasa Varga dignity scale, "
            "indicating placement in own sign or exaltation in at least one of "
            "the divisional charts. The 10th lord at this dignity is more powerful "
            "than the 1st lord at the same level."
        ),
        "effect":         "The native will be liberal (generous, magnanimous in giving).",
        "is_benefic":     True,
        "life_domains":   ["character", "status", "wealth"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": (
                "Requires: (1) identifying all four angular lords, (2) computing "
                "the Dasa Varga (D1 through D10 divisional chart set), (3) "
                "assessing Varga dignity (Parijatamsa = own/exaltation in specific "
                "divisional chart count). Both Varga computation (V) and lord "
                "identification (L) are outside current engine scope."
            ),
        },
    },
    {
        "yoga_name":      "Angular Lord in Uttamamsa — Highly Liberal",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Uttamamsa — the second tier of the Dasa Varga scale, indicating "
            "a higher density of own/exaltation placements across divisional "
            "charts than Parijatamsa."
        ),
        "effect":         "The native will be highly liberal — more so than the Parijatamsa level.",
        "is_benefic":     True,
        "life_domains":   ["character", "status", "wealth"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },
    {
        "yoga_name":      "Angular Lord in Gopuramsa — Prowess and Manliness",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Gopuramsa — the third tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be endowed with prowess and manliness (valour, physical distinction).",
        "is_benefic":     True,
        "life_domains":   ["character", "status", "strength"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },
    {
        "yoga_name":      "Angular Lord in Simhasanamsa — Honourable and Prominent",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Simhasanamsa — the fourth tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be honourable and prominent (distinguished, held in high regard by society).",
        "is_benefic":     True,
        "life_domains":   ["status", "honor", "leadership"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },
    {
        "yoga_name":      "Angular Lord in Paravatamsa — Valorous",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Paravatamsa — the fifth tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be valorous (courageous, brave, and victorious in contests).",
        "is_benefic":     True,
        "life_domains":   ["character", "strength", "status"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },
    {
        "yoga_name":      "Angular Lord in Devalokamsa — Head of Men, Leadership",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Devalokamsa — the sixth tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be head of an assembly, attain leadership and a "
            "high social position — commanding authority over others."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "leadership", "power"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },
    {
        "yoga_name":      "Angular Lord in Brahmalokamsa — Sagely and Spiritual",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Brahmalokamsa — the seventh tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be sagely and attain spiritual achievements — a man of wisdom.",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "wisdom", "character"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },
    {
        "yoga_name":      "Angular Lord in Iravatamsa — Delighted and Celebrated",
        "sloka":          "ch41-sloka-18-19",
        "group":          "angular_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The lord of an angular house (1st, 4th, 7th, or 10th) is in "
            "Iravatamsa — the eighth and highest tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be delighted, ever happy, and a celebrated personality "
            "from all viewpoints — the pinnacle of the angular lord dignity scale."
        ),
        "is_benefic":     True,
        "life_domains":   ["happiness", "fame", "status"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires Dasa Varga computation (V) and angular lord identification (L).",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 5. 5th LORD VARGA DIGNITIES (Slokas 20–22)
    #
    # The 5th lord's Dasa Varga dignity governs both material achievements
    # (learning, status) and spiritual ones. Unlike the 9th lord which is
    # solely spiritual, the 5th lord operates across both planes.
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "5th Lord in Parijatamsa — Learning Befitting One's Race",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord (the planet ruling the 5th house sign) is in Parijatamsa "
            "— the first tier of the Dasa Varga dignity scale."
        ),
        "effect":         "The native will take to the branch of learning befitting his race and tradition.",
        "is_benefic":     True,
        "life_domains":   ["education", "intellect", "family"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Uttamamsa — Excellent Learning",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Uttamamsa — the second tier of the Dasa Varga scale."
        ),
        "effect":         "The native will have excellent learning — scholarship of a high order.",
        "is_benefic":     True,
        "life_domains":   ["education", "intellect"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Gopuramsa — World-Wide Honours",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Gopuramsa — the third tier of the Dasa Varga scale."
        ),
        "effect":         "The native will receive world-wide honours and recognition across countries.",
        "is_benefic":     True,
        "life_domains":   ["fame", "status", "honor"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Simhasanamsa — Endowed with Ministership",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Simhasanamsa — the fourth tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be endowed with ministership — governmental authority and counsel.",
        "is_benefic":     True,
        "life_domains":   ["status", "government", "leadership"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Paravatamsa — Knowledge of Supreme Spirit",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Paravatamsa — the fifth tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be endowed with knowledge of the Supreme Spirit (Brahma Jnana, self-realisation).",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "wisdom"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Devalokamsa — Karma Yogi",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Devalokamsa — the sixth tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be a Karma Yogi — a performer of both worldly actions "
            "and religious rites with equal dedication and devotion."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "dharma", "karma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Brahmalokamsa — Devoted to the Lord",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Brahmalokamsa — the seventh tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be devoted to the Lord — deep bhakti (devotion) and surrender to the Divine.",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "devotion"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "5th Lord in Iravatamsa — Pious",
        "sloka":          "ch41-sloka-20-22",
        "group":          "fifth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 5th lord is in Iravatamsa — the eighth and highest tier of "
            "the Dasa Varga scale."
        ),
        "effect":         "The native will be pious — of pure character, righteous conduct, and deep religious merit.",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "character", "dharma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 5th lord identification (L) and Dasa Varga computation (V).",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 6. 9th LORD VARGA DIGNITIES (Slokas 23–27)
    #
    # The 9th lord is solely related to spiritual achievements (unlike the 5th
    # which covers both material and spiritual). Its Varga dignity progression
    # traces the path from pilgrimage to the status of Dharma itself. The
    # highest level (Iravatamsa) is described as synonymous with Dharma — like
    # Lord Rama and Yudhishtira. The word 'Tridandi' (command over mind, speech,
    # and deed = Trikarana Suddhi) appears at the Devalokamsa level.
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "9th Lord in Parijatamsa — Visits Holy Places",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord (planet ruling the 9th house sign) is in Parijatamsa "
            "— the first tier of the Dasa Varga dignity scale."
        ),
        "effect":         "The native will visit holy places (pilgrimage, tirtha yatra, sacred sites).",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "pilgrimage", "dharma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Uttamamsa — Visited Holy Places in Past Births",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Uttamamsa — the second tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native had visited holy places in past births — indicating "
            "accumulated spiritual merit (purva punya) from previous incarnations."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "karma", "dharma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Gopuramsa — Performs Sacrificial Rites",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Gopuramsa — the third tier of the Dasa Varga scale."
        ),
        "effect":         "The native will perform sacrificial rites (Yajnas, Homas, Vedic ceremonies).",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "dharma", "ritual"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Simhasanamsa — Mighty, Truthful, Conqueror of Senses",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Simhasanamsa — the fourth tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be mighty, truthful, a conqueror of his senses, "
            "and will concentrate solely on the Supreme Spirit giving up all "
            "religions — a state of pure, non-sectarian spiritual seeking."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "character", "strength"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Paravatamsa — Greatest of Ascetics",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Paravatamsa — the fifth tier of the Dasa Varga scale."
        ),
        "effect":         "The native will be the greatest of ascetics — a supreme Tapasvi of the highest order.",
        "is_benefic":     True,
        "life_domains":   ["spirituality", "renunciation"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Devalokamsa — Tridandi Religious Mendicant",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Devalokamsa — the sixth tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be an ascetic holding a cudgel (Lagudi) or a "
            "religious mendicant (Tridandi — one who has mastered Trikarana Suddhi: "
            "purity of mind, speech, and deed) that has renounced all mundane "
            "attachments and carries three long staves tied together."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "renunciation", "dharma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Brahmalokamsa — Performs Aswamedha Yaga",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Brahmalokamsa — the seventh tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will perform the Aswamedha Yaga (Horse Sacrifice — the "
            "highest Vedic sacrificial rite) and will attain the state of Lord "
            "Indra (the king of gods)."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "dharma", "status"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "9th Lord in Iravatamsa — Synonym of Dharma",
        "sloka":          "ch41-sloka-23-27",
        "group":          "ninth_lord_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The 9th lord is in Iravatamsa — the eighth and highest tier of "
            "the Dasa Varga scale."
        ),
        "effect":         (
            "The native will themselves be a synonym of Dharma and virtues — "
            "a living embodiment of righteousness, just as Lord Sri Rama and "
            "Yudhishtira (Dharma Raja of Maha Bharata) personify Dharma."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "dharma", "fame"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L"],
            "description": "Requires 9th lord identification (L) and Dasa Varga computation (V).",
        },
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # 7. RAJAYOGA VARGA YOGAS (Slokas 28–34)
    #
    # When an angular lord (Vishnusthana: 1st/4th/7th/10th) establishes one of
    # six qualifying relationships with a trinal lord (Lakshmisthana: 1st/5th/9th),
    # a Rajayoga obtains. Their combined Varga dignity then determines the
    # magnitude of status. Both planets must be in the same Amsa tier; if one is
    # higher the result is intelligently scaled upward from the base level.
    #
    # Relationship types (Sloka 28):
    #   1. Exchange of signs (Parivartana)     — High potency
    #   2. Mutual aspects                       — High potency
    #   3. Conjunction                          — High potency
    #   4. Mutual angular placement             — Lower potency
    #   5. Mutual trinal placement              — Lower potency
    #   6. Navamsa exchange (extension)         — High potency (equivalent to 1–3)
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "yoga_name":      "Angular-Trinal Lord Rajayoga — Relationship Framework",
        "sloka":          "ch41-sloka-28",
        "group":          "rajayoga_varga",
        "condition_type": "general_principle",
        "formation":      (
            "The angles (1st, 4th, 7th, 10th houses) are the Vishnusthanas "
            "(abodes of Lord Vishnu) and the trines (1st, 5th, 9th houses) are "
            "the Lakshmistanas (abodes of Goddess Lakshmi). When the lord of an "
            "angle establishes a qualifying relationship with the lord of a trine, "
            "a Rajayoga is formed. Six types of relationship qualify: "
            "(1) Exchange of signs (Parivartana — highest potency); "
            "(2) Mutual aspects between the two lords (high potency); "
            "(3) Conjunction (same house) of the two lords (high potency); "
            "(4) Mutual angular placement (one in angle from the other — lower potency); "
            "(5) Mutual trinal placement (lower potency); "
            "(6) Navamsa exchange (Mars in Venus Navamsa and Venus in Mars Navamsa, "
            "as an example for Capricorn ascendant) — this extension is equally "
            "superior to the first three types. After confirming the relationship, "
            "the Varga dignity of both planets determines the grade of the yoga "
            "(see slokas 29–34)."
        ),
        "effect":         (
            "A Rajayoga is formed when the Vishnu and Lakshmi house lords connect. "
            "The magnitude — from 'king and protector of men' up to 'Swayambhu Manu' "
            "— is governed by their combined Dasa Varga dignity (see the 8-tier "
            "mapping in slokas 29–34). The first three relationship types and the "
            "Navamsa exchange are more powerful than the last two."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "power", "leadership", "spirituality"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": (
                "Requires: (1) identifying all angular and trinal lords (L), "
                "(2) detecting exchange/aspect/conjunction/mutual placement "
                "relationships between each pair (A + L), (3) computing Navamsa "
                "(D-9) positions for extension rule (V). Complex multi-step "
                "check spanning both natal and Navamsa charts."
            ),
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Parijatamsa — King and Protector of Men",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "An angular lord and a trinal lord have established a qualifying "
            "Rajayoga relationship (see sloka 28), AND both planets are in "
            "Parijatamsa — the first tier of the Dasa Varga scale. If one is "
            "in Parijatamsa and the other in a higher Amsa, the result is "
            "intelligently scaled upward from the base Parijatamsa outcome."
        ),
        "effect":         "The native will be a king and protector of men.",
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "leadership", "power"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": (
                "Requires angular-trinal lord identification (L), relationship "
                "detection (A), and Dasa Varga dignity assessment (V). All three "
                "blockers active."
            ),
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Uttamamsa — Excellent King with Royal Cavalry",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair (angular + trinal lord in relationship) "
            "are both in Uttamamsa — the second tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be an excellent king endowed with elephants, horses "
            "and chariots — a ruler with full ceremonial and military resources."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "leadership", "wealth"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Gopuramsa — Tiger of Kings",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair are both in Gopuramsa — the third tier "
            "of the Dasa Varga scale."
        ),
        "effect":         "The native will be a tiger of kings — a supreme ruler honoured by other kings.",
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "power"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Simhasanamsa — Emperor of the Entire Earth",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair are both in Simhasanamsa — the fourth "
            "tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be an emperor ruling over the entire earth. Historical "
            "archetypes born with this yoga in the present Yuga: Harishchandra, "
            "Manu, Bali (Chakravarthi), the Fire god Agni Deva, Yudhishtira "
            "(Dharma Raja of Maha Bharata), and Salivahana among others."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "power", "leadership"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Paravatamsa — Status of Secondary Manus",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair are both in Paravatamsa — the fifth "
            "tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be of the stature of the Manus (secondary Manus "
            "among the 14) — a divine law-giver and cosmic ruler of a manvantara "
            "period."
        ),
        "is_benefic":     True,
        "life_domains":   ["status", "royalty", "spirituality"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Devalokamsa — Incarnation of Lord Vishnu",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair are both in Devalokamsa — the sixth "
            "tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be an Incarnation (Avatar) of Lord Vishnu — the "
            "highest divine embodiment within the Vaishnava cosmological framework."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "divinity", "dharma"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Brahmalokamsa — Status of Lord Brahma",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair are both in Brahmalokamsa — the seventh "
            "tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will attain the status of Lord Brahma — the Creator "
            "in the Hindu Trinity, responsible for the generation of the universe."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "divinity", "creation"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
    {
        "yoga_name":      "Rajayoga Pair in Iravatamsa — Status of Swayambhu Manu",
        "sloka":          "ch41-sloka-29-34",
        "group":          "rajayoga_varga",
        "condition_type": "varga_dignity",
        "formation":      (
            "The qualifying Rajayoga pair are both in Iravatamsa — the eighth "
            "and highest tier of the Dasa Varga scale."
        ),
        "effect":         (
            "The native will be of the stature of Swayambhu Manu — the first "
            "of the 14 Manus, identified as the second creator who produced the "
            "Prajapatis and to whom the Manusmriti (code of cosmic law) is "
            "ascribed. The pinnacle of the Rajayoga Varga scale."
        ),
        "is_benefic":     True,
        "life_domains":   ["spirituality", "divinity", "dharma", "leadership"],
        "yoga_check": {
            "type":        "manual",
            "checkable":   False,
            "blockers":    ["V", "L", "A"],
            "description": "Requires Rajayoga relationship (L, A) and Dasa Varga computation (V).",
        },
    },
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_summary(effect: str, max_chars: int = 250) -> str:
    """Truncate effect text at the first sentence boundary within max_chars.
    Prevents mid-word/mid-sentence cuts that cause validator flags."""
    if not effect:
        return ""
    if len(effect) <= max_chars:
        return effect
    chunk = effect[:max_chars]
    last_dot = chunk.rfind(". ")
    if last_dot > 60:
        return effect[:last_dot + 1]
    return chunk


# ── Rule builder ──────────────────────────────────────────────────────────────

def build_rule(yoga: dict, index: int) -> dict:
    rule_id      = f"bphs-ch41-{index:03d}"
    yoga_name    = yoga["yoga_name"]
    sloka        = yoga.get("sloka", "")
    group        = yoga.get("group", "wealth_axis_yoga")
    is_benefic   = yoga.get("is_benefic", True)
    life_domains = yoga.get("life_domains", [])
    formation    = yoga.get("formation", "")
    effect       = yoga.get("effect", "")
    yoga_check   = yoga.get("yoga_check", {})
    cond_type    = yoga.get("condition_type", "yoga_combination")
    checkable    = yoga_check.get("checkable", False)

    group_lbl = {
        "wealth_axis_yoga":    "Wealth Axis Yoga",
        "own_sign_lagna_yoga": "Own-Sign Lagna Yoga",
        "general_principle":   "General Principle",
        "angular_lord_varga":  "Angular Lord Varga Dignity",
        "fifth_lord_varga":    "5th Lord Varga Dignity",
        "ninth_lord_varga":    "9th Lord Varga Dignity",
        "rajayoga_varga":      "Rajayoga Varga Dignity",
    }.get(group, "Wealth Yoga")

    detailed = f"Formation: {formation}\n\nEffect: {effect}".strip()
    tags = ["wealth_yoga", f"group:{group}"]
    if checkable:
        tags.append("yoga_checkable")

    return {
        "rule_id":         rule_id,
        "science_id":      SCIENCE,
        "source": {
            "book":           BOOK,
            "book_id":        BOOK_ID,
            "chapter":        CHAPTER,
            "chapter_name":   CHAP_NAME,
            "sloka":          sloka,
            "batch_id":       BATCH_ID,
            "primary":        BOOK,
            "page_ref":       None,
            "passage_ref_id": None,
        },
        "condition": {
            "type":               cond_type,
            "sub_type":           "yoga_formation",
            "yoga_name":          yoga_name,
            "yoga_group":         group,
            "yoga_group_label":   group_lbl,
            "planets_involved":   [],
            "houses_involved":    [],
            "sub_conditions":     [],
            "operator":           "and",
            "gender_context":     "neutral",
            "condition_group_id": f"bphs-ch41-{group}",
            "is_group_summary":   False,
            "is_benefic":         is_benefic,
            "yoga_check":         yoga_check,
        },
        "interpretation": {
            "summary":            _make_summary(effect),
            "detailed":           detailed,
            "full_text_passages": [{"text": detailed, "confidence": "HIGH"}],
            "remedies":           [],
            "life_domain":        life_domains[0] if life_domains else "general",
            "life_domains":       life_domains,
            "tags":               tags,
            "physical_markers":   [],
        },
        "metadata": {
            "planets_involved":     [],
            "houses_involved":      [],
            "signs_involved":       [],
            "condition_count":      1,
            "gender_context":       "neutral",
            "condition_group_id":   f"bphs-ch41-{group}",
            "is_group_summary":     False,
            "has_physical_markers": False,
            "physical_categories":  [],
            "yoga_checkable":       checkable,
        },
        "confidence": {
            "source_confidence":  "HIGH",
            "extraction_method":  "hard_coded",
            "validated":          False,
        },
        "approval_status": "pending_review",
        "created_at":      datetime.now(timezone.utc).isoformat(),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest BPHS Ch 41 Yogas for Wealth"
    )
    parser.add_argument("--dry-run",  action="store_true",
                        help="Build rules and print summary without writing")
    parser.add_argument("--save",     metavar="PATH",
                        help="Save dry-run JSON to file")
    parser.add_argument("--upload",   metavar="PATH",
                        help="Upload rules from saved JSON (zero API calls)")
    parser.add_argument("--mongo-url", default="mongodb://localhost:27017")
    parser.add_argument("--db-name",   default="horoscope_db")
    args = parser.parse_args()

    # ── Upload path ──────────────────────────────────────────────────────────
    if args.upload:
        from pymongo import MongoClient
        path = Path(args.upload)
        if not path.exists():
            print(f"ERROR: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        with open(path) as f:
            rules = json.load(f)
        client = MongoClient(args.mongo_url)
        coll = client[args.db_name]["interpretation_rules"]
        result = coll.insert_many(rules)
        print(f"✅ Uploaded {len(result.inserted_ids)} rules to "
              f"{args.db_name}.interpretation_rules")
        print(f"   Batch ID: {BATCH_ID}")
        print(f"\nNext step — validate:")
        print(f"   python3 scripts/validate_rules.py "
              f"--mongo-url $MONGO_URL --db-name {args.db_name} "
              f"--batch-id {BATCH_ID}")
        client.close()
        return

    # ── Build rules ──────────────────────────────────────────────────────────
    rules = [build_rule(y, i + 1) for i, y in enumerate(YOGA_DATA)]

    # ── Summary ──────────────────────────────────────────────────────────────
    checkable_rules = [r for r in rules if r["metadata"]["yoga_checkable"]]
    total = len(rules)

    print(f"\nBPHS Ch {CHAPTER} — {CHAP_NAME}")
    print(f"  Total rules  : {total}")
    print(f"  Checkable    : {len(checkable_rules)} / {total} "
          f"({100 * len(checkable_rules) // total if total else 0}%)")
    print(f"  Batch ID     : {BATCH_ID}")

    groups: dict[str, int] = {}
    for r in rules:
        g = r["condition"]["yoga_group"]
        groups[g] = groups.get(g, 0) + 1
    print("\n  Groups:")
    for g, n in groups.items():
        lbl = {
            "wealth_axis_yoga":    "Wealth Axis Yoga",
            "own_sign_lagna_yoga": "Own-Sign Lagna Yoga",
            "general_principle":   "General Principle",
            "angular_lord_varga":  "Angular Lord Varga Dignity",
            "fifth_lord_varga":    "5th Lord Varga Dignity",
            "ninth_lord_varga":    "9th Lord Varga Dignity",
            "rajayoga_varga":      "Rajayoga Varga Dignity",
        }.get(g, g)
        print(f"    {lbl:<40} {n} rules")

    print("\n  All rules (checkable status):")
    for r in rules:
        yc = r["condition"]["yoga_check"]
        mark = "✅" if yc.get("checkable") else "❌"
        blockers = yc.get("blockers", [])
        print(f"    {r['rule_id']}  [{mark}]  "
              f"{r['condition']['yoga_name'][:55]}"
              f"  blockers={blockers}")

    if args.dry_run and not args.save:
        print("\n  [dry-run only — use --save to write JSON]")
        return

    # ── Save ─────────────────────────────────────────────────────────────────
    out_path = Path(args.save) if args.save else None
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\n✅ Saved {total} rules → {out_path}")
        print(f"\nNext step — review {out_path}, then upload:")
        print(f"   python3 scripts/ingest_bphs_ch41_v1.py \\")
        print(f"     --upload {out_path} --mongo-url $MONGO_URL --db-name {args.db_name}")

    if args.dry_run:
        print("\n  [dry-run complete]")


if __name__ == "__main__":
    main()
