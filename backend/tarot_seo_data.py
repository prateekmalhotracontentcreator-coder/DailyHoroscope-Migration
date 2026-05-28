from __future__ import annotations

import json
from typing import Any

SITE_URL = "https://www.everydayhoroscope.in"

# ── CARD REGISTER (D3 -- GAI Burstiness Classification) ──────────────────────
# Register A: Sharp/Abrupt -- max 9-word sentences, blunt active voice
# Register B: Grounded/Measured -- 12-18 word sentences, practical tone
# Register C: Expansive/Flowing -- 25+ word compound structures, uplifting cadence
CARD_REGISTER: dict[str, str] = {
    # Register A -- Sharp / Abrupt
    "three-of-swords":      "A",
    "the-tower":            "A",
    "five-of-pentacles":    "A",
    "death":                "A",
    "ten-of-swords":        "A",
    "five-of-swords":       "A",
    "five-of-wands":        "A",
    "seven-of-swords":      "A",
    "nine-of-swords":       "A",
    "eight-of-swords":      "A",
    "four-of-swords":       "A",
    "page-of-swords":       "A",
    "knight-of-swords":     "A",
    "queen-of-swords":      "A",
    "king-of-swords":       "A",
    "ace-of-swords":        "A",
    "two-of-swords":        "A",
    "five-of-cups":         "A",
    "eight-of-cups":        "A",
    "the-devil":            "A",
    "judgement":            "A",
    "the-moon":             "A",
    # Register B -- Grounded / Measured
    "the-emperor":          "B",
    "seven-of-pentacles":   "B",
    "four-of-cups":         "B",
    "the-hierophant":       "B",
    "justice":              "B",
    "temperance":           "B",
    "the-hermit":           "B",
    "four-of-pentacles":    "B",
    "two-of-pentacles":     "B",
    "three-of-pentacles":   "B",
    "six-of-pentacles":     "B",
    "eight-of-pentacles":   "B",
    "page-of-pentacles":    "B",
    "knight-of-pentacles":  "B",
    "queen-of-pentacles":   "B",
    "king-of-pentacles":    "B",
    "ace-of-pentacles":     "B",
    "ten-of-pentacles":     "B",
    "two-of-wands":         "B",
    "four-of-wands":        "B",
    "six-of-wands":         "B",
    "nine-of-wands":        "B",
    "king-of-wands":        "B",
    "two-of-cups":          "B",
    "six-of-cups":          "B",
    "seven-of-cups":        "B",
    "king-of-cups":         "B",
    "the-hanged-man":       "B",
    "wheel-of-fortune":     "B",
    # Register C -- Expansive / Flowing
    "the-star":             "C",
    "the-sun":              "C",
    "ace-of-cups":          "C",
    "the-fool":             "C",
    "the-magician":         "C",
    "the-high-priestess":   "C",
    "the-empress":          "C",
    "the-lovers":           "C",
    "the-chariot":          "C",
    "strength":             "C",
    "the-world":            "C",
    "ace-of-wands":         "C",
    "three-of-wands":       "C",
    "three-of-cups":        "C",
    "nine-of-cups":         "C",
    "page-of-cups":         "C",
    "knight-of-cups":       "C",
    "queen-of-cups":        "C",
    "ten-of-cups":          "C",
    "seven-of-wands":       "C",
    "eight-of-wands":       "C",
    "ten-of-wands":         "C",
    "page-of-wands":        "C",
    "knight-of-wands":      "C",
    "queen-of-wands":       "C",
}

# ── POSITION SYNONYMS (D4 -- GAI Rotation Table) ────────────────────────────
# Use: random.choice(POSITION_SYNONYMS["past"]) when rendering position labels
# This breaks structural HTML uniformity across spread pages.
POSITION_SYNONYMS: dict[str, list[str]] = {
    "past":              ["Foundation Roots", "The Retrospective", "Historical Catalyst", "Passed Influences", "Origin Points"],
    "present":           ["Current Matrix", "Present Stance", "Active Reality", "Immediate Energy", "Instant Horizon"],
    "future":            ["Approaching Path", "Emerging Horizon", "Manifest Destiny", "Unfolding Outcome", "Terminal Trajectory"],
    "challenge":         ["Frictional Hurdle", "Blind Spot Area", "Core Resistance", "The Blockage", "Adversary Element"],
    "advice":            ["Strategic Pivot", "Prescribed Path", "Remedial Action", "Higher Directive", "Tactical Alignment"],
    "outcome":           ["Ultimate Harvest", "Resulting State", "Resolution Path", "Terminal Reality", "Closing Synthesis"],
    "hidden_factor":     ["Subconscious Undercurrent", "Hidden Variable", "Unseen Catalyst", "Shadow Element", "Subterranean Reality"],
    "what_to_release":   ["Heavy Baggage", "Outgrown Patterns", "Structural Shedding", "Necessary Exhale", "Surrender Vector"],
    "what_to_embrace":   ["Incoming Flow", "Target Alignment", "Sacred Invitation", "Necessary Inhale", "Emergent Calling"],
    "external_influence":["Environmental Matrix", "Social Echo", "Collective Impact", "Outsider Pressures", "Atmospheric Factor"],
}



SPREADS_JSON = r"""[
  {
    "number": 1,
    "slug": "daily-tarot-reading-insight",
    "title": "Daily Tarot Reading Insight",
    "chapter": "One-Card Spreads",
    "purpose": "A one-card morning practice for grounding awareness before the day begins. One symbol, pulled before the noise arrives, is enough to name the day's underlying energy.",
    "positions": [],
    "use": "A full deck of seventy-eight cards. Choose one card at random from anywhere in the facedown deck.",
    "when": "Come to this spread first thing in the morning, before plans and obligations take over. The insight travels better when it arrives before your mind has already decided what the day means."
  },
  {
    "number": 2,
    "slug": "single-question-tarot-answer",
    "title": "Single Question Tarot Answer",
    "chapter": "One-Card Spreads",
    "purpose": "A single-card draw for moments when the question is already clear and what's needed is one honest answer rather than analysis. Its discipline is simplicity: one focused question, one card, one unambiguous message.",
    "positions": [],
    "use": "A single card from the full deck of seventy-eight cards. Choose one card taken at random from anywhere in the facedown deck. If the answer is not clear, add a second card.",
    "when": "Reach for this when you have already thought the situation through and need a direct signal rather than more reflection. The reading works best when you hold the question with real stillness rather than running through all possible interpretations at once."
  },
  {
    "number": 13,
    "slug": "buying-a-house-vs-vacation-planning-tarot",
    "title": "Buying a House vs Vacation Planning Tarot",
    "chapter": "Two-Card Spreads",
    "purpose": "A two-card layout for moments when two valid but incompatible financial or lifestyle goals need to be directly compared. Each card holds one option and the contrast between them reveals which path carries more genuine alignment right now.",
    "positions": [],
    "use": "The full deck. Choose, before turning the cards over, one card for each option and read left to right.",
    "when": "Use it when you have genuinely weighed both options practically and still cannot feel which one belongs to this season of life. Read the two cards as a direct conversation between the options rather than as separate stand-alone messages."
  },
  {
    "number": 14,
    "slug": "career-promotion-vs-work-life-balance-tarot",
    "title": "Career Promotion vs Work Life Balance Tarot",
    "chapter": "Two-Card Spreads",
    "purpose": "A two-card spread for the specific tension between ambition and sustainability -- when pursuing more professional success and protecting personal wellbeing feel like they cannot coexist. The cards name what each path actually requires rather than what it promises.",
    "positions": [],
    "use": "The full deck.",
    "when": "Come to this spread when you are not just choosing between two outcomes but between two versions of yourself. Read each card as the honest cost and benefit of its path rather than as pure prediction."
  },
  {
    "number": 25,
    "slug": "3-card-clarity-spread-for-any-situation",
    "title": "3 Card Clarity Spread for Any Situation",
    "chapter": "Three-Card Spreads",
    "purpose": "A three-position spread that maps any situation across a clear narrative arc: what is present, what is active beneath the surface, and where the energy is currently moving. The structure is deliberately open so it can hold any question without distorting it.",
    "positions": [
      "Card 2 to act as the"
    ],
    "use": "A full deck of 78 cards.",
    "when": "Use this when the situation feels complex but the core question is essentially singular. Three positions give enough structure to avoid oversimplification without breaking the reading into too many fragments."
  },
  {
    "number": 26,
    "slug": "past-present-future-timeline-reading",
    "title": "Past Present Future Timeline Reading",
    "chapter": "Three-Card Spreads",
    "purpose": "A timeline spread that reads a situation as movement rather than fixed state -- showing where the energy originated, where it has arrived, and what direction it is currently heading. The value is in the trajectory, not just the present card.",
    "positions": [
      "Card 1: What you need to leave behind to make the change or what is already moving out of your life.",
      "Card 2: The present influences and factors already emerging affecting your decision.",
      "Card 3: The results of taking action and what lies over the horizon if you do."
    ],
    "use": "The full seventy-eight-card deck.",
    "when": "Come to this spread when a situation seems stuck and you want to understand it as a process in motion. Reading the three cards as a continuous flow matters more than treating them as separate snapshots."
  },
  {
    "number": 27,
    "slug": "short-term-future-forecast-tarot",
    "title": "Short Term Future Forecast Tarot",
    "chapter": "Three-Card Spreads",
    "purpose": "A compact forecast spread designed for the near window -- the next few days, weeks, or months -- rather than longer arcs. It gives enough coverage to reveal immediate tendencies without overextending the reading's range.",
    "positions": [
      "Card 1: Will represent factors or people who will be helpful.",
      "Card 2: Will signify factors or people who may stand in your way. And the all-important",
      "Card 3 represents what"
    ],
    "use": "The forty Number cards, Ace to Ten, and the sixteen Court or Personality cards.",
    "when": "Use this when you need immediate directional guidance rather than a longer life overview. It works best when the timeframe in mind is concrete rather than vaguely 'the future.'"
  },
  {
    "number": 37,
    "slug": "4-card-intuitive-guidance-layout",
    "title": "4 Card Intuitive Guidance Layout",
    "chapter": "Four-Card Spreads",
    "purpose": "A four-card layout that balances analytical and intuitive information -- using the structure of four positions to hold a complex situation without reducing it to a single verdict. The four cards speak to each other as much as to the question.",
    "positions": [],
    "use": "Any combination of the seventy-eight cards that fits with your question.",
    "when": "Come to this spread when a three-card reading feels too compressed and a larger layout would lose the thread. Read the four cards as a single field rather than four separate answers."
  },
  {
    "number": 38,
    "slug": "overcoming-fear-and-mental-blocks-tarot",
    "title": "Overcoming Fear and Mental Blocks Tarot",
    "chapter": "Four-Card Spreads",
    "purpose": "A spread built specifically for moments when fear is making decisions rather than the person asking. It names the specific nature of the block, its source, and what genuine forward movement would require rather than offering reassurance.",
    "positions": [
      "Card 1: What is the real cause of my fear?",
      "Card 2: Is this bad thing actually likely to happen, or is it just fear?",
      "Card 3: What triggers/makes the fear worse?",
      "Card 4: What action can I take to prevent or overcome my fear?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when fear, not practical obstacles, is what is actually stopping you. Give each position enough time to name the specific fear being shown rather than collapsing them into a general theme."
  },
  {
    "number": 47,
    "slug": "horseshoe-layout-for-complex-decisions",
    "title": "Horseshoe Layout for Complex Decisions",
    "chapter": "Five-Card Spreads",
    "purpose": "A seven-card horseshoe layout for questions that have too many sides to be resolved by simpler spreads. Its arched structure holds past influences, present circumstances, external factors, hopes, and likely outcomes in a single cohesive reading.",
    "positions": [
      "Card 1: Your choice, dilemma or predominant question.",
      "Card 2: Present influences, people, and circumstances that affect your present position.",
      "Card 3: Hidden influences, both the messages in our heads from the past and what is just beyond the horizon.",
      "Card 4: Suggested action, whether to change or preserve the status quo.",
      "Card 5: Likely outcome, of either acting or waiting according to",
      "Card 4 ."
    ],
    "use": "The full deck.",
    "when": "Come to this spread when a question has genuine complexity -- multiple stakeholders, competing priorities, or a timeline that matters. The horseshoe works best when you read its arc as a single narrative rather than seven independent messages."
  },
  {
    "number": 48,
    "slug": "navigating-workplace-cliques-and-bullying",
    "title": "Navigating Workplace Cliques and Bullying",
    "chapter": "Five-Card Spreads",
    "purpose": "A spread designed for the specific dynamics of group-based workplace exclusion -- naming the social forces at play, the role you are in, and the practical move that would most effectively change your position. It is less about feelings and more about strategy.",
    "positions": [
      "Card 1: Who/what is excluding me most.",
      "Card 2: What the motive is.",
      "Card 3: Can or should I ignore it?",
      "Card 4: Should I complain/tackle it head on?",
      "Card 5: Should I cut my losses and leave?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when workplace dynamics feel genuinely entrenched and you need a clearer map of what is happening beneath the surface. Approach each position as information about the system rather than about individual blame."
  },
  {
    "number": 49,
    "slug": "5-year-life-path-long-term-layout",
    "title": "5 Year Life Path Long Term Layout",
    "chapter": "Five-Card Spreads",
    "purpose": "A long-range spread for reading the trajectory of a major life direction over several years rather than months. It is less concerned with specific events than with the quality and direction of the energy as it moves forward through time.",
    "positions": [
      "Card 1: Where I am now.",
      "Card 2: Where I would like to be in five years' time.",
      "Card 3: What extra resources/training/practice do I need?",
      "Card 4: Any possible challenges to overcome?",
      "Card 5: To achieve this long-term goal, do I need to expand/move on now, or stay where I am?"
    ],
    "use": "The full deck.",
    "when": "Use this when you are at a genuine crossroads and want a longer view than seasonal spreads provide. Read each position as a stage rather than a prediction of specific events."
  },
  {
    "number": 56,
    "slug": "6-card-deep-dive-reading-for-any-problem",
    "title": "6 Card Deep Dive Reading for Any Problem",
    "chapter": "Six-Card Spreads",
    "purpose": "A six-position layout for problems that have enough dimensions to require sustained examination. Six cards allow distinct angles of the same question to speak without crowding each other, creating a reading with real depth.",
    "positions": [
      "Card 6 the answer falls into place. Almost always the person shown in each card represents you--or, if not, then the person/people who affect the question."
    ],
    "use": "A full deck of seventy-eight cards.",
    "when": "Come to this spread when a situation has several moving parts and a three-card reading keeps missing something. Move through each position slowly rather than forming a conclusion before all six cards have been heard."
  },
  {
    "number": 57,
    "slug": "mid-term-future-vision-tarot-layout",
    "title": "Mid Term Future Vision Tarot Layout",
    "chapter": "Six-Card Spreads",
    "purpose": "A forecast spread tuned to the medium range -- six weeks to six months ahead -- bridging the gap between immediate guidance and year-long planning. It tracks both what is building and what is winding down in the period.",
    "positions": [
      "Card 1: What do you hope to achieve in the next six weeks/months?",
      "Card 2: What specific opportunities are you seeking?",
      "Card 3: What challenges are you worried about?",
      "Card 4: What would you like to remain unchanged?",
      "Card 5: What/who would you like to change?",
      "Card 6: What do you seek in the longer term?"
    ],
    "use": "The full deck.",
    "when": "Use this when you need guidance for a defined medium-term window, such as a project timeline, a seasonal transition, or a specific goal with a named deadline. The forecast strengthens when the time boundary is held clearly."
  },
  {
    "number": 58,
    "slug": "manifesting-true-love-and-soulmate-tarot",
    "title": "Manifesting True Love and Soulmate Tarot",
    "chapter": "Six-Card Spreads",
    "purpose": "A six-card spread for understanding the current energetic conditions around romantic manifestation -- what is already aligned, what internal pattern may be creating resistance, and what shift would most change the outcome. It reads readiness, not just desire.",
    "positions": [
      "Card 1: Should I give up looking and just wait for it to happen?",
      "Card 2: Should I try an online dating site/friendship group?",
      "Card 3: Should I join a face-to-face/singles group?",
      "Card 4: Should I join new activities?",
      "Card 5: Should I relocate/change my job?",
      "Card 6: Will I meet my Twin Soul, or settle for someone nice?"
    ],
    "use": "The whole deck.",
    "when": "Come to this spread when romantic longing is strong but the situation feels stalled in ways that practical effort hasn't been able to change. Read the internal positions as honestly as the external ones."
  },
  {
    "number": 64,
    "slug": "choosing-between-two-paths-tarot",
    "title": "Choosing Between Two Paths Tarot",
    "chapter": "Seven-Card Spreads",
    "purpose": "A binary decision spread that places two options side by side so the cards can speak to each without interference. The reading is most useful when both options are genuinely viable and the difficulty is in sensing which one is more aligned.",
    "positions": [
      "Card 1: The choice to be made which may be different from the conscious question.",
      "Card 2: (Option 1) The suggested action to carry out",
      "Card 4: Unforeseen consequences, good or challenging, that result from carrying through",
      "Card 6: The likely outcome of following the path of",
      "Card 3: The suggested action.",
      "Card 5: The unforeseen consequences.",
      "Card 7: The likely outcome of"
    ],
    "use": "The whole deck.",
    "when": "Use this when you have already done the rational analysis and still cannot feel which direction belongs to you. Read the two sides as a dialogue rather than a competition."
  },
  {
    "number": 65,
    "slug": "7-card-mystical-chakra-alignment",
    "title": "7 Card Mystical Chakra Alignment",
    "chapter": "Seven-Card Spreads",
    "purpose": "A seven-card spread mapped to the energy centres of the body -- reading each chakra position for what is active, blocked, or in transition there. It is most useful for questions about health, spiritual development, and emotional pattern.",
    "positions": [
      "Card 7, will reveal what is just over the horizon or being hidden and the answer to your dilemma."
    ],
    "use": "The twenty-two Major cards or the full deck.",
    "when": "Come to this spread when you want the reading to speak to the body and energy field rather than only to circumstantial events. Sit with each position long enough to feel its resonance before moving to the next."
  },
  {
    "number": 70,
    "slug": "achieving-big-goals-and-dreams-reading",
    "title": "Achieving Big Goals and Dreams Reading",
    "chapter": "Eight-Card Spreads",
    "purpose": "An eight-card layout for clarifying the internal landscape around a major ambition -- what is genuinely supporting it, what is functioning as resistance, and what specific shift would most move the goal forward. It maps the gap between aspiration and momentum.",
    "positions": [
      "Card 1: Is this the window of opportunity for which I have been waiting?",
      "Card 2: Is this step that I am contemplating realistic?",
      "Card 3: Am I ready--and, if not, when will I be?",
      "Card 4: Who/what will help me?",
      "Card 5: Who/what will oppose me/disapprove?",
      "Card 6: Should I modify/compromise my dream to make the step less disruptive?",
      "Card 7: The short-term outcome of taking the step, the next six months.",
      "Card 8: The longer-term outcome, the next five years."
    ],
    "use": "The full deck.",
    "when": "Use this when a major goal feels consistently out of reach despite real effort and you want to understand why. Work through each position as a specific diagnostic rather than a general overview of the goal."
  },
  {
    "number": 71,
    "slug": "fertility-and-conception-guidance-tarot",
    "title": "Fertility and Conception Guidance Tarot",
    "chapter": "Eight-Card Spreads",
    "purpose": "A spread addressing the emotional, energetic, and practical dimensions of fertility -- reading both the physical and psychological landscape around conception with the care the question deserves. It is designed for the full complexity of the experience, not a simple yes or no.",
    "positions": [
      "Card 1: Do we want a child/children now or in the future?",
      "Card 2: If we try, how soon can we conceive?",
      "Card 3: What will we lose most in terms of freedom/finances if we have a baby?",
      "Card 4: What will we gain most by having a family?",
      "Card 5: Can we/how can we keep the special magic alive between us if we have a baby?",
      "Card 6: How best can I/my partner improve our health to maximize our chances of conceiving?",
      "Card 7: What practical lifestyle changes would a new baby bring about?",
      "Card 8: Should we leave nature to take its course, or will this reduce our chances of having a baby?"
    ],
    "use": "The whole deck.",
    "when": "Come to this spread when fertility is an active concern and you want guidance that addresses the whole experience rather than only timing. Read the emotional positions with as much weight as the practical ones."
  },
  {
    "number": 76,
    "slug": "9-card-spiritual-matrix-breakthrough",
    "title": "9 Card Spiritual Matrix Breakthrough",
    "chapter": "Nine-Card Spreads",
    "purpose": "A nine-card matrix for moments when a spiritual or personal question has reached a genuine impasse and surface-level guidance is no longer enough. The grid structure allows the reading to speak to multiple dimensions simultaneously.",
    "positions": [
      "Card 9 ."
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you want depth rather than direction -- when the question itself needs to be held more than resolved. Lay all nine cards before reading any of them so the pattern can emerge before interpretation begins."
  },
  {
    "number": 77,
    "slug": "resolving-legal-disputes-fairly-tarot",
    "title": "Resolving Legal Disputes Fairly Tarot",
    "chapter": "Nine-Card Spreads",
    "purpose": "A spread for navigating the emotional and strategic complexity of legal conflict -- naming what each party actually needs, where the real obstacle lives, and what approach would most serve a fair resolution. It is as much about clarity as outcome.",
    "positions": [
      "Card 1: What/who is causing the injustice?",
      "Card 2: What/who is in the way of revealing the truth?",
      "Card 3: What is the weakness of your opponent?",
      "Card 4: What is the greatest strength/in your favor?",
      "Card 5: What unexpected new facts/evidence will come to light to benefit you?",
      "Card 6: Can you do more, or should you wait?",
      "Card 7: Are you well represented/need new representation?",
      "Card 8: Can/should you settle out of court/through mediation?",
      "Card 9: What is the ideal outcome?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when a legal situation involves enough emotional weight that rational assessment alone has not been sufficient. Read each position as a distinct piece of the landscape rather than building a single conclusion too early."
  },
  {
    "number": 82,
    "slug": "12-card-comprehensive-life-overview",
    "title": "12 Card Comprehensive Life Overview",
    "chapter": "Multi-Card Spreads",
    "purpose": "A twelve-card overview reading that surveys multiple life areas simultaneously -- relationships, work, wellbeing, and inner development -- giving a broad map of where energy is concentrated, depleted, or in transition across the whole.",
    "positions": [],
    "use": "The full deck.",
    "when": "Come to this spread at a major threshold -- a new year, a significant birthday, or after a major life change -- when you want to understand the full landscape rather than one specific area. Read each position before drawing any single conclusion."
  },
  {
    "number": 83,
    "slug": "12-month-wheel-of-year-forecast",
    "title": "12 Month Wheel of Year Forecast",
    "chapter": "Multi-Card Spreads",
    "purpose": "A twelve-card annual forecast that assigns one card to each month of the year ahead, reading each as the primary energetic quality or theme of that period rather than predicting specific events. The value is in the pattern across the full year.",
    "positions": [
      "Card 1 being the month following the reading. Record the opportunities or challenges each card suggests during a particular month. As a rule, Major Arcana cards indicate major events or where outside circumstances play a big part. Minor cards refer to more ordinary but nevertheless significant happenings occurring in the period you are measuring. Court cards indicate dominant personalities--or a new love or pregnancy. Finally, choose a card to sum up the twelve months ahead and put this in the center of the circle. You can pick two cards for each month if you wish."
    ],
    "use": "One or two full decks.",
    "when": "Use this at the start of a new year or personal cycle when you want a macro view of the months ahead. Lay all twelve cards first and look for the pattern before reading any individual card."
  },
  {
    "number": 87,
    "slug": "past-life-love-and-soul-connection",
    "title": "Past Life Love and Soul Connection",
    "chapter": "Love And Commitment Spreads",
    "purpose": "A spread for exploring the karmic and soul-level dimensions of a significant relationship -- reading what may have drawn these two people together from beyond this lifetime and what pattern from the past is still active in the present dynamic.",
    "positions": [
      "Card 1: Is (name) my Soul mate?",
      "Card 2: When and how were we together in past worlds?",
      "Card 3: What do we share from past worlds that brings us even closer in this life?",
      "Card 4: What or who divides us in this life?",
      "Card 5: What is unfinished from earlier worlds?",
      "Card 6: What is our karmic destiny together?",
      "Card 7: Will we stay forever together in this life?"
    ],
    "use": "The forty Minor cards and the sixteen Court cards.",
    "when": "Come to this spread when a relationship carries an unusual quality of familiarity, intensity, or repetition that ordinary relationship analysis doesn't fully explain. Approach each card as a window into a longer story."
  },
  {
    "number": 88,
    "slug": "twin-flame-recognition-signs-tarot",
    "title": "Twin Flame Recognition Signs Tarot",
    "chapter": "Love And Commitment Spreads",
    "purpose": "A six-card spread for reading whether a specific connection has the quality of a twin flame dynamic -- addressing recognition signs, current phase, and what the connection is activating rather than simply whether it is destined.",
    "positions": [
      "Card 1: Do you feel you have known each other forever?",
      "Card 2: Was there instant recognition/connection at the first meeting?",
      "Card 3: Does s/he fit totally with your family/friends/interests?",
      "Card 4: Is the relationship fast-moving but quite natural-feeling?",
      "Card 5: Is a missing part of your life now complete?",
      "Card 6: Do you have constant déjà vu and telepathic links?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when an intense connection is prompting questions about its nature that go beyond whether the relationship is healthy or compatible. Read each position in sequence so the fuller picture develops before reaching the outcome card."
  },
  {
    "number": 108,
    "slug": "resolving-relationship-conflicts-tarot",
    "title": "Resolving Relationship Conflicts Tarot",
    "chapter": "Spreads For Overcoming Difficulties In Love, Reconciliation, And Ending Destructive Relationships",
    "purpose": "A six-card spread for understanding what is genuinely driving a recurring relationship conflict -- naming each person's unspoken need, the dynamic between them, and what shift would most change the pattern rather than the episode.",
    "positions": [
      "Card 2: What is the underlying issue for you?",
      "Card 3: What is the underlying issue for your partner?",
      "Card 5: Are there principles on which you cannot/will not back down?",
      "Card 6: Are there issues on which your partner cannot/will not back down?",
      "Card 8: Is anyone outside fueling the fire?",
      "Card 9: What is the best outcome?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when the same conflict keeps returning in different clothing and you want to understand its root rather than manage its surface. Read each person's position before looking at the cards that address the dynamic between them."
  },
  {
    "number": 109,
    "slug": "dealing-with-emotional-immaturity-in-love",
    "title": "Dealing with Emotional Immaturity in Love",
    "chapter": "Spreads For Overcoming Difficulties In Love, Reconciliation, And Ending Destructive Relationships",
    "purpose": "A spread for reading the specific emotional dynamic in a relationship where one or both people are struggling to respond from their adult self -- naming the pattern, its source, and what genuine growth in the relationship would require.",
    "positions": [
      "Card 1: How is this most adversely affecting the relationship?",
      "Card 2: Will s/he change, given time?",
      "Card 3: How can change come about?",
      "Card 4: If s/he doesn't grow up, should I stick with the relationship?",
      "Card 5: What can I do to make things better?",
      "Card 6: Who/what bad influences need to be removed from his/her life?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread when emotional reactions in the relationship consistently feel disproportionate to the situation, or when one person's fear response is consistently driving the dynamic. Read the shadow position honestly."
  },
  {
    "number": 129,
    "slug": "manifesting-urgent-financial-abundance",
    "title": "Manifesting Urgent Financial Abundance",
    "chapter": "Prosperity And Money-Making Spreads",
    "purpose": "A spread for moments when financial need is pressing and clarity about the fastest genuine path forward -- rather than long-term planning -- is what the situation requires. It reads immediate opportunity and internal obstruction simultaneously.",
    "positions": [
      "Card 1: Who will/can help; what are the strings?",
      "Card 2: What existing assets/resources can you release?",
      "Card 3: What talents/skills can generate more income fast?",
      "Card 4: What will temporarily stop/reverse the outflow?",
      "Card 5: What official/unofficial borrowing sources are there?",
      "Card 6: Are there unpaid money/favors owing to you?",
      "Card 7: The hidden obstacle.",
      "Card 8: The as-yet-unrevealed rescue/rescuer."
    ],
    "use": "The full deck.",
    "when": "Come to this spread when financial pressure is acute rather than chronic and you need guidance on the nearest available door rather than the ideal long-term strategy. Work through each position before settling on a course of action."
  },
  {
    "number": 130,
    "slug": "relocating-abroad-for-high-salary-job",
    "title": "Relocating Abroad for High Salary Job",
    "chapter": "Prosperity And Money-Making Spreads",
    "purpose": "A spread built for the specific complexity of international relocation tied to a career opportunity -- balancing financial gain, personal disruption, and the longer career trajectory. It addresses both the practical calculation and the less visible factors.",
    "positions": [
      "Card 1: What benefits of taking the offer short-term might outweigh other considerations?",
      "Card 2: What longer-term advantages would occur if you stayed in the job indefinitely?",
      "Card 3: What emotional/lifestyle problems might arise, and can they be overcome?",
      "Card 4: What are the hidden drawbacks?",
      "Card 5: Yes or no, taking the other four cards into account."
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when the relocation involves enough personal and financial consequence that a simple pros-and-cons analysis has not been enough. Let the positions map the full picture before you draw a conclusion."
  },
  {
    "number": 149,
    "slug": "breaking-generational-financial-scarcity",
    "title": "Breaking Generational Financial Scarcity",
    "chapter": "Spreads For Solving Difficulties With Money",
    "purpose": "A spread that reads the inherited dimension of financial struggle -- the beliefs, behaviours, and family patterns around money that were absorbed before they could be consciously chosen, and what it would take to operate outside them.",
    "positions": [],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread when financial difficulty seems to follow a pattern that predates your own choices -- when the money story feels inherited more than acquired. Read the generational positions before the practical ones."
  },
  {
    "number": 150,
    "slug": "setting-strong-boundaries-with-money",
    "title": "Setting Strong Boundaries with Money",
    "chapter": "Spreads For Solving Difficulties With Money",
    "purpose": "A spread for understanding the psychological and energetic landscape around financial boundary-setting -- identifying where money is leaking, what makes saying no difficult, and what internal shift would most change the pattern.",
    "positions": [
      "Card 1: What stops you from saying no?",
      "Card 2: Who takes advantage of you the most?",
      "Card 3: How will you cope with the resentment/pressure if you start saying no?",
      "Card 4: What do you gain by being overly generous?",
      "Card 5: Who will resist/protest/use emotional blackmail if you say no?",
      "Card 6: Are you with the wrong people?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when money keeps moving in ways that feel outside your conscious control despite genuine effort. Read the shadow and belief positions before the action ones."
  },
  {
    "number": 169,
    "slug": "interview-success-and-career-hiring-tarot",
    "title": "Interview Success and Career Hiring Tarot",
    "chapter": "Career Spreads",
    "purpose": "A spread designed for the specific pressure of a significant hiring situation -- reading your energetic alignment with the role, what the interview process is likely to surface, and how to position yourself most authentically.",
    "positions": [
      "Card 1: Are there more indications in your favor?",
      "Card 2: Are there more indications that you may not get this job?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread in the days before a significant interview or hiring decision, not the day of. The cards often point to preparation, not just outcome."
  },
  {
    "number": 170,
    "slug": "managing-difficult-bosses-and-coworkers",
    "title": "Managing Difficult Bosses and Coworkers",
    "chapter": "Career Spreads",
    "purpose": "A spread for reading the specific dynamic of a difficult professional relationship -- naming what is actually driving the friction, what each party needs that they are not currently getting, and what strategic move would most shift the interaction.",
    "positions": [
      "Card 1: The open cause of the conflict.",
      "Card 2: The hidden cause of the conflict.",
      "Card 3: The solution."
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread when a workplace relationship has been persistently difficult long enough to suggest the pattern needs to be understood rather than simply endured. Read the position that names the hidden dynamic before the advice position."
  },
  {
    "number": 171,
    "slug": "full-time-job-vs-side-hustle-tarot",
    "title": "Full Time Job vs Side Hustle Tarot",
    "chapter": "Career Spreads",
    "purpose": "A spread for the specific tension between employment security and entrepreneurial freedom -- reading each path for its energetic fit with where you are right now, what each genuinely requires, and which one your current resources can actually sustain.",
    "positions": [
      "Card 1 and",
      "Card 2 and neither seems definite, add a third card above and between"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when you have been moving back and forth between the two options long enough that the indecision is becoming its own cost. Read each card as its honest requirement, not its best-case promise."
  },
  {
    "number": 191,
    "slug": "entrepreneurship-launch-roadmap-tarot",
    "title": "Entrepreneurship Launch Roadmap Tarot",
    "chapter": "Business Spreads",
    "purpose": "A five-card spread for reading the energetic landscape around launching a new business or independent venture -- naming what is genuinely ready, what still needs preparation, and what specific quality of attention the first stage requires.",
    "positions": [
      "Card 1: Are you ready to launch your business?",
      "Card 2: Should you launch it 100%, or run it part-time until established?",
      "Card 3: Is there an existing market for your business, or do you need to create one?",
      "Card 4: Are the premises/equipment you have/will obtain adequate?",
      "Card 5: What expansion plans will be viable over the next twelve months?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when you are close to launching and need to understand what is ready versus what is still being assembled. Read each position as its own stage of the launch rather than as a single verdict on the whole."
  },
  {
    "number": 192,
    "slug": "brick-and-mortar-vs-e-commerce-scaling",
    "title": "Brick and Mortar vs E-Commerce Scaling",
    "chapter": "Business Spreads",
    "purpose": "A spread for the specific decision of how to grow an existing business -- comparing physical and digital expansion paths for their energetic fit, realistic requirements, and timing alignment. It reads readiness as much as strategy.",
    "positions": [
      "Card 1: Should you find/develop the right premises locally?",
      "Card 2: Is there sufficient local trade to support you/should you aim wider?",
      "Card 3: Should you travel to different venues/locations with your goods/services?",
      "Card 4: How can you achieve maximum publicity for the least cost?",
      "Card 5: Should/how should you incorporate Internet sales outlets into your business?",
      "Card 6: Should you focus almost entirely on offering online sales and services?",
      "Card 7: Would it be more effective to combine both methods equally?",
      "Card 8: Should you franchise or offer your goods/services through other stores/websites?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when a scaling decision has been postponed because neither option feels completely right. Let the cards name what each path genuinely demands rather than what you hope it will require."
  },
  {
    "number": 211,
    "slug": "audition-mastery-strategy-for-competitions",
    "title": "Audition Mastery Strategy for Competitions",
    "chapter": "Spreads For Fame And Fortune",
    "purpose": "A spread for reading the internal and external landscape around a significant performance opportunity -- what you are bringing, what is working against you, what the competition itself requires, and where your preparation can most improve the outcome.",
    "positions": [
      "Card 1: What do you need to know to get into the final?",
      "Card 2: How can you best overcome the competition of other entrants?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread at least a week before a significant audition or competition so the guidance has time to inform your preparation. Work through each position in order so the strategy each card suggests can build on the previous one."
  },
  {
    "number": 212,
    "slug": "winning-strategy-for-creative-contests",
    "title": "Winning Strategy for Creative Contests",
    "chapter": "Spreads For Fame And Fortune",
    "purpose": "A spread that reads creative competition through an energetic lens -- addressing what your work genuinely communicates, how it aligns with what is being judged, and what specific adjustment would most strengthen your positioning.",
    "positions": [
      "Card 1: Do you have an act that will make you stand out?",
      "Card 2: Are you used to showcasing your talents in public?",
      "Card 3: Do you want to practice more in front of strangers before applying?",
      "Card 4: Are you prepared to enter, even if you do not win this time?",
      "Card 5: Will/should you keep trying until you win?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when you want to understand the energetic dimension of a competition, not just the practical one. The cards often speak to how you are showing up rather than whether you will win."
  },
  {
    "number": 236,
    "slug": "asking-your-crush-out-success-tarot",
    "title": "Asking Your Crush Out Success Tarot",
    "chapter": "Spreads For Making Your Dearest Wishes And Dreams Come True",
    "purpose": "A spread for reading the mutual energy and timing around a romantic approach -- whether the moment is right, how the other person is likely to receive it, and what would make the approach most genuine rather than most strategic.",
    "positions": [],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when both the desire and the uncertainty are genuinely present -- not to outsource the decision but to understand the emotional landscape before stepping into it. Read the timing card last."
  },
  {
    "number": 237,
    "slug": "funding-solo-travel-using-inheritance",
    "title": "Funding Solo Travel Using Inheritance",
    "chapter": "Spreads For Making Your Dearest Wishes And Dreams Come True",
    "purpose": "A spread for a specific financial and values decision -- whether to use inherited or shared money for personal experience -- reading the emotional and energetic dimensions alongside the practical ones to understand what the choice would actually mean.",
    "positions": [
      "Card 1: Are you entitled to spend your own money any way you wish?",
      "Card 2: Should you feel guilty if you follow your dream?",
      "Card 3: Will you regret it if you do not follow your dream?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when the money question is inseparable from a question about what you owe yourself versus others. Read the values positions before the practical ones."
  },
  {
    "number": 265,
    "slug": "blended-family-dynamics-and-first-meetings",
    "title": "Blended Family Dynamics and First Meetings",
    "chapter": "Family Spreads",
    "purpose": "A spread for reading a first meeting within a complex family configuration -- naming what each person is bringing to the encounter, where the tension is likely to surface, and what would most allow the meeting to go better than feared.",
    "positions": [],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread a few days before the meeting, not the day of, so any practical preparation the cards suggest is still possible. Give the relational positions more time than you think they need."
  },
  {
    "number": 266,
    "slug": "handling-toxic-relatives-at-family-events",
    "title": "Handling Toxic Relatives at Family Events",
    "chapter": "Family Spreads",
    "purpose": "A spread for navigating a specific family event that involves a difficult or harmful relative -- reading how to protect your own energy, where the interaction is most likely to go wrong, and what level of engagement would serve you best.",
    "positions": [
      "Card 1: Will the invitation lead to more trouble than it is worth?",
      "Card 2: If you do not invite the person, will it cause",
      "Card 2 as a tiebreaker."
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread before the event, not during or after. The cards are more useful for preparation than for processing."
  },
  {
    "number": 293,
    "slug": "school-bullying-intervention-and-support",
    "title": "School Bullying Intervention and Support",
    "chapter": "Spreads For Babies, Children, And Grandchildren Of All Ages",
    "purpose": "A spread for reading the emotional landscape around a child or teenager experiencing bullying -- naming what the child needs most, what the dynamic is doing to their sense of self, and what support would be most genuinely effective.",
    "positions": [
      "Card 1: Who are the main bullies? Are they generally regarded as challenging children?",
      "Card 2: What is the main reason given for bullying your child?",
      "Card 3: Do they bully other children? Can you contact other parents for support?",
      "Card 4: Can you discover the official bullying policy and insist it is followed?",
      "Card 5: Can you avoid being intimidated by the school, which may blame your child in order to defend the school's reputation?",
      "Card 6: Can you/should you go higher than the principal to resolve this?",
      "Card 7: Whatever happens, do you want to move your child into a different school?"
    ],
    "use": "The full deck:",
    "when": "Come to this spread when you are trying to understand the situation from a deeper angle than reports and conversations have provided. Read the child's position with careful attention before moving to the adult positions."
  },
  {
    "number": 294,
    "slug": "cyberbullying-defense-advice-for-teens",
    "title": "Cyberbullying Defense Advice for Teens",
    "chapter": "Spreads For Babies, Children, And Grandchildren Of All Ages",
    "purpose": "A spread specific to online harassment -- reading the psychological impact of what has happened, the dynamics at work beyond the screen, and what combination of practical action and personal protection would most effectively address the situation.",
    "positions": [
      "Card 1: Is your child receiving an unusual number of text messages/does s/he appear upset after reading text messages?",
      "Card 2: Does your child come straight home after school instead of hanging out with friends?",
      "Card 3: Does your child look anxious and is s/he constantly checking their phone for messages?",
      "Card 4: Should you make a quiet time to talk about cyber bullying?",
      "Card 5: Would one of your child's friends talk to you regarding what may be happening to your child?",
      "Card 6: Can/should you contact a school counselor/leave a teenage helpline number around where it can be seen by your child?",
      "Card 7: Can/should you offer your child a new phone/number/social media page with strict privacy settings?"
    ],
    "use": "The full deck",
    "when": "Come to this spread when the online situation has been persistent enough to affect daily life. Each position names a specific layer of the problem rather than the situation as a whole."
  },
  {
    "number": 321,
    "slug": "calming-anxiety-and-overthinking-tarot",
    "title": "Calming Anxiety and Overthinking Tarot",
    "chapter": "Health And Healing Spreads",
    "purpose": "A spread that reads anxiety as a message rather than a malfunction -- identifying what the anxious thinking is pointing toward, what it is protecting against, and what the nervous system actually needs rather than what the mind is demanding.",
    "positions": [
      "Card 1: Is your anxiety triggered by external circumstances, or does it come from within?",
      "Card 2: Who or what situation makes it worse? Can you avoid these?",
      "Card 3: Who or what helps to calm the anxiety?",
      "Card 4: What instant strategies can you develop when you feel anxiety rising?",
      "Card 5: Would a change of lifestyle/location/career/relationship relieve the problem?",
      "Card 6: What new activity/desired situation suddenly becomes possible without the anxiety?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the six Court cards.",
    "when": "Come to this spread when anxious thinking has been running the situation for too long. Slow down at each position rather than reading quickly to reach a reassuring answer -- the card that makes you uncomfortable is often the most useful."
  },
  {
    "number": 322,
    "slug": "physical-healing-and-recovery-forecast",
    "title": "Physical Healing and Recovery Forecast",
    "chapter": "Health And Healing Spreads",
    "purpose": "A spread for reading the body's healing landscape -- where recovery energy is genuinely gathering, what is slowing the process, and what physical or emotional support would most accelerate repair. It addresses the body as a whole system rather than a single symptom.",
    "positions": [
      "Card 1: Is there anything in your life/lifestyle causing undue stress?",
      "Card 2: Should you explore alternative energy therapies such as acupuncture, acupressure, reiki, kinesiology, or meditation classes to release blocks and restore energy?",
      "Card 3: Will your health improve naturally when your life is in balance?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread during a recovery process rather than at its start. The cards speak most clearly when there is already some movement to read."
  },
  {
    "number": 354,
    "slug": "attracting-positive-good-luck-energy",
    "title": "Attracting Positive Good Luck Energy",
    "chapter": "Spreads For Good Luck",
    "purpose": "A spread for understanding the current energetic conditions around fortunate outcomes -- what internal alignments are already drawing good events, what is subtly blocking the flow, and what specific orientation would most open the channel.",
    "positions": [
      "Card 1: In what area of your life do you most need good luck?",
      "Card 2: How soon will this good luck come?",
      "Card 3: What or who is holding you back from good fortune?",
      "Card 4: In which part of your life will good fortune first come?",
      "Card 5: How can you hasten good fortune?",
      "Card 6: Who or what will help you attain good fortune?",
      "Card 7: What is the hidden secret to your good fortune?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when you want to understand why some periods feel charmed and others feel like wading through resistance. Read the obstruction card honestly rather than skipping to the action."
  },
  {
    "number": 355,
    "slug": "breaking-bad-luck-cycles-astrology",
    "title": "Breaking Bad Luck Cycles Astrology",
    "chapter": "Spreads For Good Luck",
    "purpose": "A spread for reading a persistent streak of difficult outcomes -- naming whether the pattern is circumstantial or internally driven, what is perpetuating it, and what genuine intervention would break the cycle rather than temporarily interrupting it.",
    "positions": [
      "Card 1: Do you believe you are in the hands of fate? If so, is this true, or a perception?",
      "Card 2: Is anyone causing your misfortune?",
      "Card 3: Can you/how can you change your luck?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when difficulty has been consistent enough to feel like a pattern rather than a run of events. Read the root position before the action position so you understand what is being addressed."
  },
  {
    "number": 382,
    "slug": "vastu-blessings-for-your-new-home",
    "title": "Vastu Blessings for Your New Home",
    "chapter": "Spreads For The Home And Property",
    "purpose": "A spread for reading the energetic quality of a new living space -- what it naturally supports, what it challenges, and what simple alignments would help you settle into it with the most ease and clarity.",
    "positions": [
      "Card 1: Did you feel when you first saw it that it was meant to be yours and that that was a valid feeling?",
      "Card 2: Will everything progress smoothly in negotiations/finance, etc., right through to the move?",
      "Card 3: Is this going to be a place of health, happiness, and prosperity?",
      "Card 4: Do you have any worries about the house/location and how can these be resolved?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread before unpacking rather than after -- when you still have the flexibility to choose where to set up the spaces that matter most. Read each position as information about the space, not a verdict."
  },
  {
    "number": 383,
    "slug": "real-estate-sale-success-timeline",
    "title": "Real Estate Sale Success Timeline",
    "chapter": "Spreads For The Home And Property",
    "purpose": "A ten-card spread for reading the full arc of a property sale -- timing, negotiation dynamics, what is genuinely supporting the process, and what needs attention before the right buyer arrives. It addresses both the market and the energetic conditions.",
    "positions": [
      "Card 1: Are there good reasons for the lack of serious offers, such as economic downturn/time of year, etc.?",
      "Card 2: If you are patient, will the sale come naturally eventually?",
      "Card 3: Are you being unrealistic about your price in relation to similar properties?",
      "Card 4: What is it about your home that, if emphasized, makes it particularly salable?",
      "Card 5: Should you change the target market at which it is aimed/family wanting a large place to renovate, etc.?",
      "Card 6: Should you get a new agent?",
      "Card 7: Should you advertise more on the Internet/advertise further afield?",
      "Card 8: Will the buyer be local, or from interstate or overseas?",
      "Card 9: Will the home sell within three to six months, or take up to a year?",
      "Card 10: Is there anything you should know that would speed the sale, such as price reduction/auction?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when a sale is already listed or imminent and you want to understand the landscape rather than just the outcome. Each position addresses a different dimension of the sale rather than a single prediction."
  },
  {
    "number": 411,
    "slug": "overcoming-social-isolation-and-loneliness",
    "title": "Overcoming Social Isolation and Loneliness",
    "chapter": "Spreads For Friendships And Your Social Life",
    "purpose": "A spread that reads loneliness as a specific emotional and energetic state -- naming what is creating the isolation, what kind of connection the person actually needs, and what specific first step would most genuinely shift the quality of their social life.",
    "positions": [
      "Card 1: Are you naturally a loner who doesn't want company, but feel you ought to?",
      "Card 2: Would you like a few like-minded friends? How/where can you meet them?",
      "Card 3: If you want to socialize more, what deep down holds you back?",
      "Card 4: Should you seek friends online, enjoying online friendships rather than face-to-face?",
      "Card 5: Where should you go/what should you join/new activities to try to meet more people directly?",
      "Card 6: Are you in the wrong place/should you change jobs/relocate?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when loneliness has been present long enough to feel structural rather than situational. Read the internal positions with as much honesty as the external ones."
  },
  {
    "number": 412,
    "slug": "resolving-friend-group-drama-advice",
    "title": "Resolving Friend Group Drama Advice",
    "chapter": "Spreads For Friendships And Your Social Life",
    "purpose": "A spread for reading the energetics of a specific friendship conflict or group rupture -- who needs what, where the fault line actually lives, and what approach would most genuinely restore or honestly end the situation.",
    "positions": [
      "Card 1: Who or what is causing problems in your social life?",
      "Card 2: Is there a person/clique working to exclude you?",
      "Card 3: What allies or friends do you have/could you develop within the social circle?",
      "Card 4: Should you ignore the problem/hope the troublemakers lose interest?",
      "Card 5: Do you need to tackle the difficult people head-on?",
      "Card 6: Should you move on?",
      "Card 7: What can be gained by staying in the same social circle, with or without resolution?",
      "Card 8: What is the best outcome for you?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread when the friendship situation has become complicated enough that the narrative of who is right keeps changing. Read the hidden dynamic position before deciding how to respond."
  },
  {
    "number": 441,
    "slug": "preparing-for-parenthood-relationship-check",
    "title": "Preparing for Parenthood Relationship Check",
    "chapter": "Spreads For Fertility, Conception, Pregnancy, And Babies",
    "purpose": "A four-card spread for reading the shared readiness of two people for a significant life transition -- naming each person's genuine state, the quality of their current foundation, and what the transition would most require from both of them.",
    "positions": [
      "Card 1: What does your partner really feel?",
      "Card 2: What do you really feel?",
      "Card 3: Is this the right time/do you still have things to do as a couple first?",
      "Card 4: Are the advantages of having a family greater than the disadvantages?"
    ],
    "use": "The Major twenty-two cards.",
    "when": "Come to this spread together if possible, or on behalf of both people if not. Read the individual cards before the relational ones so each position speaks on its own terms."
  },
  {
    "number": 442,
    "slug": "assessing-co-parenting-compatibility-tarot",
    "title": "Assessing Co-Parenting Compatibility Tarot",
    "chapter": "Spreads For Fertility, Conception, Pregnancy, And Babies",
    "purpose": "A three-card spread for the specific dynamic of co-parenting -- reading whether the two people can function as partners in raising a child even when the romantic relationship is not intact or unproven.",
    "positions": [
      "Card 1: Is s/he sufficiently mature, or does s/he need more time to grow up?",
      "Card 2: Would s/he be a loving supportive co-parent?",
      "Card 3: Should I go ahead and try for a baby with him/her, or move on to another relationship/go it alone?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when co-parenting is either already happening or being seriously considered and the dynamic between the two adults needs to be honestly assessed. Read each position as information about the parenting partnership specifically."
  },
  {
    "number": 467,
    "slug": "legal-victory-and-litigation-outcome",
    "title": "Legal Victory and Litigation Outcome",
    "chapter": "Spreads For Justice, Truth, Compensation, And Inheritance",
    "purpose": "A spread for reading the energetic landscape of an active legal case -- what is genuinely supporting your position, what factors are working against it, and what the case is most likely to require before it reaches resolution.",
    "positions": [
      "Card 1: Will judgment go in your favor?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when a legal matter is active enough to require strategic attention rather than just patience. The cards address the process as much as the outcome."
  },
  {
    "number": 468,
    "slug": "settlement-vs-going-to-trial-analysis",
    "title": "Settlement vs Going to Trial Analysis",
    "chapter": "Spreads For Justice, Truth, Compensation, And Inheritance",
    "purpose": "A spread for the specific legal decision of whether to accept a settlement or proceed to trial -- reading what each path genuinely costs and requires, not just in financial terms but in time, energy, and personal integrity.",
    "positions": [
      "Card 1: What are the advantages of settling out of court?",
      "Card 2: What are the disadvantages of settling out of court?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread before the decision becomes forced by external timing. The cards speak most clearly when there is still real agency over which path is chosen."
  },
  {
    "number": 493,
    "slug": "pet-adoption-readiness-assessment",
    "title": "Pet Adoption Readiness Assessment",
    "chapter": "Spreads For Pets Large And Small",
    "purpose": "A spread for weighing the emotional desire to adopt a pet against the honest practical readiness to do so -- naming what the animal would genuinely need, what the person is truly ready to provide, and whether the timing serves both.",
    "positions": [
      "Card 1: Will it/how will a pet fit in with your lifestyle?",
      "Card 2: What kind of pet would best fit your living arrangements?",
      "Card 3: If you share your home, will your partner/family/housemates welcome/accept, or dislike, a pet?",
      "Card 4: Who will care for the pet when you are on vacation/away working? Or will it be able to go with you to most places?",
      "Card 5: Will a young animal, or an older animal from a rescue center, fit best with your lifestyle?",
      "Card 6: Will your new pet fit well in your current home, or will you need to adapt/move?",
      "Card 7: Do you want a pet so much that you are willing to find a way around any difficulty?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread before making the adoption commitment rather than after. The cards are most useful as honest preparation rather than reassurance."
  },
  {
    "number": 494,
    "slug": "finding-best-pet-companion-for-your-home",
    "title": "Finding Best Pet Companion for Your Home",
    "chapter": "Spreads For Pets Large And Small",
    "purpose": "A seven-card spread for reading the energetic match between a person and different animal companions -- what kind of presence would best complement the home's current energy, what the person most needs from an animal relationship, and what the animal would need in return.",
    "positions": [
      "Card 1: Are you definite as to the right kind of pet, the species and age, or do you need more time to decide?",
      "Card 2: Do you want more than one pet, to be company for the other? Or is this impractical?",
      "Card 3: Have you narrowed down your choice to a particular breeder/rescue center, or should you explore more widely?",
      "Card 4: Will you instantly know the pet is right for you as soon as you see him/her?",
      "Card 5: Will your pet/s give you a sign that they are the right one?",
      "Card 6: Do you suspect that this will be a former deceased pet returned/a past life connection/a new but lovely connection?",
      "Card 7: Are you going to be happy together?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread when you are open to several types of companion and want guidance on which is the best fit rather than already set on a species or breed. Each position speaks to a different dimension of the match."
  },
  {
    "number": 520,
    "slug": "relocation-analysis-for-new-communities",
    "title": "Relocation Analysis for New Communities",
    "chapter": "Neighbors, Neighborhood, And Community Spreads",
    "purpose": "A spread for reading the energetic quality of a potential new neighbourhood or community -- what it would genuinely support in your life, where friction might emerge, and whether the timing is right for this particular move.",
    "positions": [
      "Card 1: Is this the right neighborhood for you? (answer depends on the strength of the positive feeling you get from the card)."
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when you are seriously weighing a specific location rather than exploring the idea of moving generally. The cards speak more precisely when the choice is real."
  },
  {
    "number": 521,
    "slug": "overcoming-isolation-after-moving",
    "title": "Overcoming Isolation After Moving",
    "chapter": "Neighbors, Neighborhood, And Community Spreads",
    "purpose": "A spread for the specific difficulty of rebuilding belonging after a significant geographic move -- reading what you need most to reconnect, what is making the process harder than expected, and what first move would most open the door.",
    "positions": [
      "Card 1: Should you knock on a few doors to say",
      "Card 2: Should you wait for them to contact you?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread after the move has already happened and the isolation has set in rather than before. The cards address what is actually happening rather than what might happen."
  },
  {
    "number": 543,
    "slug": "resolving-family-disputes-over-baby-names",
    "title": "Resolving Family Disputes Over Baby Names",
    "chapter": "Spreads For Celebrations",
    "purpose": "A spread for the specific family dynamic around a naming decision -- reading what each side of the dispute actually needs, where the real tension lives beneath the named disagreement, and what resolution would honour everyone without erasing anyone.",
    "positions": [
      "Card 1: Should you call your baby by the name you want, one that will fit into the modern world?",
      "Card 2: Would it be possible/practical to use the desired family choice as a middle name to honor the family (and keep the peace)?"
    ],
    "use": "The forty Minor cards and the twenty-two Major cards.",
    "when": "Come to this spread when the naming conversation has already become strained enough to need a fresh lens. Read each position as information about the people involved, not just the name itself."
  },
  {
    "number": 544,
    "slug": "vedic-baby-name-selection-guide",
    "title": "Vedic Baby Name Selection Guide",
    "chapter": "Spreads For Celebrations",
    "purpose": "A four-card spread for choosing a name that carries the energetic resonance you want to offer a child -- reading sound, meaning, and numerological quality as living dimensions of naming rather than aesthetic preferences.",
    "positions": [
      "Card 1: Will you know once your baby is born/comes home which names fit the personality?",
      "Card 2: Are the most likely names ones that will sound as good with a forty-year-old as a four-year-old?",
      "Card 3: Can you resist pressure from family to",
      "Card 3 . See which cards have the strongest positive meaning. If you need further guidance, see the Numerology Spread ("
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you have a shortlist of names and want deeper guidance on which one is the most genuine fit. Read each card as a distinct dimension of the name's energy rather than a ranked comparison."
  },
  {
    "number": 566,
    "slug": "holiday-travel-destination-picker-tarot",
    "title": "Holiday Travel Destination Picker Tarot",
    "chapter": "Spreads For Travel And Vacations",
    "purpose": "A spread for reading which travel destination would serve you best in a given period -- not which is most beautiful or affordable but which would offer what your energy most genuinely needs right now.",
    "positions": [
      "Card 1: What do you hope to gain most from your vacation?",
      "Card 2: What are the drawbacks of going on vacation, if any?",
      "Card 3: Is this/when is the right time to go on vacation?",
      "Card 4: Do you want to go far or near, or even vacation at home?",
      "Card 5: Will you have a happy vacation?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you are flexible about destination and want genuine guidance rather than confirmation of a preference already formed. The cards often point to the option you hadn't fully considered."
  },
  {
    "number": 567,
    "slug": "hotel-vs-resort-accommodation-decision",
    "title": "Hotel vs Resort Accommodation Decision",
    "chapter": "Spreads For Travel And Vacations",
    "purpose": "A spread for a specific travel choice where the accommodation style meaningfully affects the quality of the experience -- reading which environment would best support rest, adventure, or connection depending on what the trip is actually for.",
    "positions": [
      "Card 1: What factors aren't yet known that might influence the benefits and drawbacks of each choice?"
    ],
    "use": "The whole deck.",
    "when": "Come to this spread when the choice is genuinely open and the style of experience matters as much as the destination. Read each position as a piece of what the trip needs to provide."
  },
  {
    "number": 591,
    "slug": "breaking-hurdles-to-achieve-success",
    "title": "Breaking Hurdles to Achieve Success",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "A spread that maps specific obstacles on the path toward a defined goal -- naming each barrier, its nature, and the specific action or internal shift that would most effectively move past it rather than around it.",
    "positions": [
      "Card 1: Who or what is challenging you?",
      "Card 2: If you ignore the situation, will it pass/the person give up?",
      "Card 3: Can/should you face the challenge head-on?",
      "Card 4: What is in your favor if you take the challenge head-on?",
      "Card 5: What are your main fears in facing the challenge?",
      "Card 6: Desired or required action?",
      "Card 7: Will the action open the way to the change you want?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you have genuine momentum toward a goal but keep encountering the same type of resistance. Map each obstacle through a different position rather than treating them as a single undifferentiated challenge."
  },
  {
    "number": 592,
    "slug": "navigating-big-career-and-life-crossroads",
    "title": "Navigating Big Career and Life Crossroads",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "A nine-card spread for major life transitions where multiple dimensions -- career, relationships, identity, timing -- are all shifting at once. It gives enough room for the full scope of the change to be held without collapsing into a single question.",
    "positions": [
      "Card 1: Where you are in life right now generally. Are you happy with this?",
      "Card 2: Have you met the person you want to share your future life path with? Will you meet them soon, or do you prefer to stay independent?",
      "Card 3: Is your career path as you want it? If not, how should it progress/change?",
      "Card 4: Are your leisure activities making you happy? Do you want to leave some/add new ones?",
      "Card 5: Are you as fit and healthy as you would like to be? If not, how can you improve this?",
      "Card 6: Where do you want to be/what do you want to do at this time next year?",
      "Card 7: Where do you want to be/what do you want to do/be in five years' time?",
      "Card 8: Where do you want to be/what do you want to do in ten years' time?",
      "Card 9: What is your secret dream, and can you/how can you achieve it?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread at a genuine inflection point rather than during a period of general uncertainty. The spread works best when there is a real decision or transition at its centre."
  },
  {
    "number": 593,
    "slug": "overcoming-stagnation-and-feeling-stuck",
    "title": "Overcoming Stagnation and Feeling Stuck",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "A spread for diagnosing the specific nature of stagnation -- whether it is internal, circumstantial, or a signal that the direction itself needs reassessing -- and naming the most genuine first movement toward change.",
    "positions": [
      "Card 1: What practical and underlying factors are holding you back from making those changes?",
      "Card 2: Do you really want change, or do you just feel you ought to?",
      "Card 3: Is now the right time for change? Do you have unfinished business? Are you not quite ready?",
      "Card 4: If you are patient, will outside circumstances bring the desired change?",
      "Card 5: If you go all out for change and do not let anyone or anything stand in your way, will you succeed?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when stuck has been the felt experience for long enough that the cause is no longer obvious. Read the resistance position before the action one."
  },
  {
    "number": 622,
    "slug": "quick-zodiac-guidance-reading",
    "title": "Quick Zodiac Guidance Reading",
    "chapter": "Astrological Spreads, Part 1",
    "purpose": "A spread that pairs one tarot card with your sun sign's current energetic themes -- giving quick, solar-calendar-informed guidance on what to lean into and what to navigate carefully in the present period.",
    "positions": [
      "Card 1: The advantages of going ahead with what you are asking about.",
      "Card 2: The disadvantages of what you are asking about.",
      "Card 3: The outcome of acting/going forward."
    ],
    "use": "",
    "when": "Come to this spread for a short, grounded reading when you want something oriented by astrological season rather than a specific personal question. Read the single card through the lens of your sign's current themes."
  },
  {
    "number": 623,
    "slug": "aries-energy-bold-initiative-boost",
    "title": "Aries Energy Bold Initiative Boost",
    "chapter": "Astrological Spreads, Part 1",
    "purpose": "A spread tuned to Aries energy -- fire, bold action, and the initiating force -- for moments when a new beginning needs to be activated with the full force of the ram's directness rather than cautious strategy.",
    "positions": [
      "Card 1: Where in your life do you most need action?",
      "Card 2: How can you best assert yourself in this matter?",
      "Card 3: What advantages/opportunities will make this possible?",
      "Card 4: How can you avoid/overcome the",
      "Card 5: The unexpected factor.",
      "Card 6: The key to positive action.",
      "Card 7: The desired outcome.",
      "Card 8: The actual outcome."
    ],
    "use": "The full deck.",
    "when": "Come to this spread at the start of a new lunar cycle, a new project, or any moment when decisive action is clearly the need. Let the cards clarify which specific action is ready to be taken now rather than which general direction feels interesting."
  },
  {
    "number": 641,
    "slug": "weekly-navagraha-planetary-guide",
    "title": "Weekly Navagraha Planetary Guide",
    "chapter": "Astrological Spreads, Part 2: The Planetary Spreads",
    "purpose": "A seven-card spread mapped to the seven classical planets of Vedic astrology -- reading the current influence of each planetary energy on your life and identifying where each day's challenge or opportunity is most likely to concentrate.",
    "positions": [
      "Card 1: Sunday, day of the Sun. What is your greatest potential or talent/how can you manifest it?",
      "Card 2: Monday, day of the Moon. What is your current/long-term dream/is it attainable?",
      "Card 3: Tuesday, the day of Mars. What is your greatest challenge/obstacle to success?",
      "Card 4: Wednesday, the day of Mercury. What do you need to learn or initiate?",
      "Card 5: Thursday, the day of Jupiter. How can you most advance your cause/impress others/will you get your lucky break?",
      "Card 6: Friday, the day of Venus. What is your future in love/a significant relationship you are thinking about?",
      "Card 7: Saturday, the day of Saturn. What is your greatest source of security/stability/your greatest limitation to overcome?"
    ],
    "use": "",
    "when": "Come to this spread at the beginning of the week and read each planetary card for the day it governs rather than all seven at once. The guidance becomes more specific and actionable when it is applied one day at a time."
  },
  {
    "number": 642,
    "slug": "overcoming-imposter-syndrome-for-success",
    "title": "Overcoming Imposter Syndrome for Success",
    "chapter": "Astrological Spreads, Part 2: The Planetary Spreads",
    "purpose": "A spread for reading the internal landscape of professional self-doubt -- naming the specific belief that is generating the impostor feeling, what it is actually protecting, and what honest inner recognition would most change the relationship with your own competence.",
    "positions": [
      "Card 1: Is it",
      "Card 2: What unique qualities do you have that make you stand out?",
      "Card 3: Will you succeed this time?",
      "Card 4: If not, will you know how to succeed next time you try?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when the gap between your external success and your internal sense of legitimacy has become large enough to affect your decisions. Read the origin position before the action card."
  },
  {
    "number": 657,
    "slug": "new-moon-rituals-for-fresh-beginnings",
    "title": "New Moon Rituals for Fresh Beginnings",
    "chapter": "Moon Spreads",
    "purpose": "A spread for working with new moon energy -- setting intentions with clarity, naming what needs to be released from the previous cycle, and identifying the specific seed most ready to be planted in the new lunar phase.",
    "positions": [
      "Card 1: What do you hope for most from this new beginning, not just outwardly?",
      "Card 2: What are the outer and inner disadvantages/worries about this new phase?",
      "Card 3: Are you fully prepared for this new phase? What have you overlooked?",
      "Card 4: Is there anything/anyone you would like/need to take with you/leave behind?",
      "Card 5: Will your new beginning bring happiness soon, or take months?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread within the two days around the new moon. The reading works best when used as part of a quiet intentional ritual rather than as a quick check-in."
  },
  {
    "number": 658,
    "slug": "manifesting-fast-secondary-income",
    "title": "Manifesting Fast Secondary Income",
    "chapter": "Moon Spreads",
    "purpose": "A spread for reading the nearest genuine path toward additional income -- naming which skill or resource is most ready to be activated, what is holding the path back, and what concrete first action would move the fastest.",
    "positions": [
      "Card 1: Could any of your existing sources of money offer short-term increase through extra hours/input?",
      "Card 2: Are there any sources/assets from which you could borrow extra money/sell to make up the shortfall?",
      "Card 3: Are/how are negotiations possible to take the immediate pressure off you?",
      "Card 4: Will this shortfall continue unless you find a more permanent/lucrative source of income/input?",
      "Card 5: Will there be unexpected help?",
      "Card 6: Will you get the money by the time of the next crescent moon?"
    ],
    "use": "The forty Minor cards and the sixteen Court cards.",
    "when": "Come to this spread when financial need is genuinely pressing and you need to identify the nearest available door rather than the ideal long-term solution. Work through each position before settling on a direction."
  },
  {
    "number": 684,
    "slug": "launching-freelance-and-solopreneur-gigs",
    "title": "Launching Freelance and Solopreneur Gigs",
    "chapter": "Moon Zodiac Spreads",
    "purpose": "A spread for reading the energetic and practical readiness to launch independent work -- naming what makes your offering genuinely unique, where the first clients are most likely to come from, and what mindset most supports a sustainable start.",
    "positions": [
      "Card 1: What advantages are there in your going for self-employment now?",
      "Card 2: What disadvantages are there in launching now?",
      "Card 3: Go for it, wait, or abandon the idea?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread before formal launch rather than after -- when there is still time for the cards' guidance to shape the approach rather than assess the result."
  },
  {
    "number": 685,
    "slug": "breaking-free-from-toxic-family-dynamics",
    "title": "Breaking Free from Toxic Family Dynamics",
    "chapter": "Moon Zodiac Spreads",
    "purpose": "An eight-card spread for reading the psychological and energetic architecture of entrenched family toxicity -- naming the role you currently play, what makes breaking free difficult, and what specific internal shift creates the most genuine change.",
    "positions": [
      "Card 1: Do I/how do I get the strength to follow my own path?",
      "Card 2: What is the worst aspect of the interference/domination?",
      "Card 3: Are there/what are the positive benefits such as financial support/security that makes me allow this behavior to continue?",
      "Card 4: Should I speak out and not be shouted down?",
      "Card 5: Should I/do I want to physically move away/have reduced contact until I am more confident?",
      "Card 6: Can I overcome the problem and still retain the love of the family?",
      "Card 7: What will I have achieved toward my independence by the time the full moon is in the sky again?",
      "Card 8: What will I have achieved by the next full moon in Aries?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you want to understand the dynamic rather than manage your response to it. Read the role position and the root position before looking at the exit card."
  },
  {
    "number": 720,
    "slug": "healing-trauma-loss-and-betrayal-guide",
    "title": "Healing Trauma Loss and Betrayal Guide",
    "chapter": "Moon-Angel Spreads",
    "purpose": "A spread for reading the current stage of healing after a significant wound -- naming where the grief or trauma is still active, what it most needs to move through, and what specific quality of attention would most genuinely support the next stage of recovery.",
    "positions": [
      "Card 1: What should you temporarily withdraw from or take a step back from until you feel stronger?",
      "Card 2: What should you permanently withdraw from or not return to?",
      "Card 3: What plans/hopes do you have for the month ahead to start to enter life again?",
      "Card 4: What worries you about putting them in practice?",
      "Card 5: Can you/should you take advice/seek help, or would you sooner work to achieve these plans alone?",
      "Card 6: Is it realistic to have made progress by the time of the next new moon, or should you take as long as you need?",
      "Card 7: Will you find peace and harmony again?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when enough time has passed for initial shock to have given way to the slower work of healing. The cards speak most clearly in the middle stages, when the wound is real but the direction forward is not yet obvious."
  },
  {
    "number": 721,
    "slug": "divine-signs-for-uncertain-crossroads",
    "title": "Divine Signs for Uncertain Crossroads",
    "chapter": "Moon-Angel Spreads",
    "purpose": "A spread for moments when the rational mind has reached its limit and guidance is being sought from a wider intelligence -- reading the signs, synchronicities, and symbolic messages that may be pointing toward a direction not yet consciously seen.",
    "positions": [
      "Card 1: Is your new beginning in the right direction for you?",
      "Card 2: S",
      "Card 3: What resources/help can you call on to support you in these early days?",
      "Card 4: Are there practical steps you can take to hasten your new beginning?",
      "Card 5: Must you first/at the same time initiate an inner new beginning?",
      "Card 6: Who/what do you fear might hold it back?",
      "Card 7: How far will you have progressed by the next crescent moon?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread in a state of genuine openness rather than with a preferred outcome in mind. Sit quietly with each card before interpreting it so the symbolic meaning has room to arrive on its own terms."
  },
  {
    "number": 741,
    "slug": "angelic-protection-for-loneliness-and-fear",
    "title": "Angelic Protection for Loneliness and Fear",
    "chapter": "Angel And Archangel Spreads",
    "purpose": "A spread for moments of genuine fear or isolation -- reading the specific quality of protection and support available, what is most needed for the fear to ease, and what form of comfort would be most genuinely healing rather than merely reassuring.",
    "positions": [
      "Card 1: How can you feel the presence of your guardian angel in your life at this time?",
      "Card 2: What sign in the everyday world can your angel reveal so you know you are not alone?",
      "Card 3: What is the help you most need from your angel, rather than what you think you need?",
      "Card 4: Will earthly help/support come to you?",
      "Card 5: How can you most help yourself?",
      "Card 6: What special blessings will your angel bring into your life?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when you are in a state of genuine distress rather than mild uncertainty. Read the protection position first, and stay with it long enough to actually feel what it is offering before moving on."
  },
  {
    "number": 742,
    "slug": "turning-temporary-gigs-into-full-time-jobs",
    "title": "Turning Temporary Gigs into Full Time Jobs",
    "chapter": "Angel And Archangel Spreads",
    "purpose": "A spread for reading what it would take to convert a temporary working arrangement into a stable one -- naming what the employer or market needs to see, what you are genuinely ready to offer, and what specific action would most advance the transition.",
    "positions": [
      "Card 1: Will your current workplace offer more permanent employment if you ask?",
      "Card 2: Is there one particular place you have recently worked where you did especially well that would put you on a future vacancy list?",
      "Card 3: Is there an extra qualification/expertise that would make it easier to get a permanent job?",
      "Card 4: What special help would you ask of Archangel Sachiel to open the right doors to permanent employment?",
      "Card 5: Will you succeed?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread when you are genuinely interested in making a particular arrangement permanent rather than considering the possibility abstractly. The more specific the situation, the more precise the guidance."
  },
  {
    "number": 773,
    "slug": "healing-inner-child-reclaiming-joy",
    "title": "Healing Inner Child and Reclaiming Joy",
    "chapter": "Crystal Tarot Spreads",
    "purpose": "A single-card draw for contact with the part of yourself that existed before self-doubt and learned limitation narrowed the experience of what is possible. The card names one quality of that original self that is still available and can be actively reclaimed.",
    "positions": [
      "Card 1: What will be the results of your new beginning?"
    ],
    "use": "",
    "when": "Come to this spread when the protective mechanisms that once served you have begun to cost more than they protect. Hold the card's meaning as an active invitation rather than a passive description."
  },
  {
    "number": 774,
    "slug": "manifestation-strategy-for-startups",
    "title": "Manifestation Strategy for Startups",
    "chapter": "Crystal Tarot Spreads",
    "purpose": "A one-card spread for the very beginning of a venture -- naming the single most important energetic quality needed to support a new business through its earliest and most fragile stage. One clear signal is more useful here than a complex reading.",
    "positions": [
      "Card 1: Will your venture succeed immediately/take longer to evolve?"
    ],
    "use": "",
    "when": "Come to this spread before the formal start date of a new project or business. The single card works best as a centring focus to return to throughout the launch phase rather than as a one-time message."
  },
  {
    "number": 796,
    "slug": "karmic-destiny-crossroads-tarot",
    "title": "Karmic Destiny Crossroads Tarot",
    "chapter": "Spreads For Foretelling Your Destiny",
    "purpose": "A spread for reading the soul-level dimension of a major decision -- what past pattern this choice is being shaped by, what the crossroads is actually asking you to learn, and which direction serves the larger arc of your development rather than only the immediate desire.",
    "positions": [
      "Card 1: Boreas, the North Wind, the actual situation/the most likely effects if nothing changes/you do nothing.",
      "Card 2: Eurus, the East Wind, logically what can be done to positively affect matters.",
      "Card 3: Notus, the South Wind, what unexpected boost or mitigation exists of the situation from outside sources.",
      "Card 4: Zephyrus, the West Wind, what might blow you off course?",
      "Card 5: The result of all these factors coming together."
    ],
    "use": "The full deck.",
    "when": "Come to this spread when a decision feels unusually weighted, as though more is at stake than the practical outcome alone. Read the karmic position before the practical ones."
  },
  {
    "number": 797,
    "slug": "pendulum-divination-for-hidden-answers",
    "title": "Pendulum Divination for Hidden Answers",
    "chapter": "Spreads For Foretelling Your Destiny",
    "purpose": "A spread that uses the pendulum-like quality of the final card to name the hidden factor most shaping the situation -- the thing that the conscious mind has not yet been able to articulate or admit. It is a diagnostic spread rather than a roadmap.",
    "positions": [],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when you suspect there is something operating beneath the obvious narrative that needs to be surfaced before any other guidance can be accurate. Hold the hidden factor position open rather than pre-loading it with your guess."
  },
  {
    "number": 820,
    "slug": "rebalancing-yin-and-yang-energies",
    "title": "Rebalancing Yin and Yang Energies",
    "chapter": "Spreads For Self-Awareness And Knowledge And Planning Your Life Path",
    "purpose": "A spread for reading the current imbalance between receptive and active energies -- naming which is depleted and which is overdeveloped, and what specific reorientation would restore the quality of balance the situation most needs.",
    "positions": [
      "Card 1: What/who really caused/is causing the chaos?",
      "Card 2: Should you intervene, or wait for things to settle?",
      "Card 3: Who/what will prove most helpful in bringing peace to the situation?",
      "Card 4: How can you restore your own balance if others' behaviors are shaking it?",
      "Card 5: How can you prevent others' future chaos affecting your lasting harmony?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when life feels consistently one-directional -- when everything is either forcing or waiting, driving or drifting, without the natural alternation that sustains genuine wellbeing."
  },
  {
    "number": 821,
    "slug": "shadow-work-discovery-tarot-reading",
    "title": "Shadow Work Discovery Tarot Reading",
    "chapter": "Spreads For Self-Awareness And Knowledge And Planning Your Life Path",
    "purpose": "A spread for reading what is operating below the surface of conscious awareness -- the disowned patterns, defended wounds, and projected energies that are quietly shaping behaviour and outcomes. It asks what you are not yet ready to see clearly.",
    "positions": [
      "Card 1: How you are seen by the world.",
      "Card 2: The hidden self the world never sees.",
      "Card 3: How you can combine the two, so you feel at home in the world without becoming too vulnerable."
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when you are prepared to encounter what is uncomfortable rather than seeking confirmation or comfort. Move through each position slowly enough that the shadow can show itself rather than being named from the outside."
  },
  {
    "number": 848,
    "slug": "deep-tarot-card-meditation-techniques",
    "title": "Deep Tarot Card Meditation Techniques",
    "chapter": "Combining Tarot Spreads And Psychic Powers",
    "purpose": "A six-card layout for developing a genuine contemplative relationship with a specific card rather than understanding its abstract definition. Each position opens a different layer of the card's symbolism as it applies to the reader's current experience.",
    "positions": [],
    "use": "Twenty-two Major cards and thirty-six Minor cards, Twos to Tens (Aces aren't detailed enough).",
    "when": "Come to this spread when you want to move past intellectual understanding and spend real time inside a single card's meaning. Allow at least an hour rather than moving through it like a conventional reading."
  },
  {
    "number": 849,
    "slug": "channeled-spirit-automatic-writing-guide",
    "title": "Channeled Spirit Automatic Writing Guide",
    "chapter": "Combining Tarot Spreads And Psychic Powers",
    "purpose": "A spread for preparing the internal conditions most supportive of channelled writing or spirit communication -- reading what is genuinely available, what is creating interference, and what quality of receptivity would most allow the guidance to come through clearly.",
    "positions": [],
    "use": "The full deck.",
    "when": "Come to this spread before sitting down to write rather than during or after. The preparation positions are often more important than the message positions."
  },
  {
    "number": 870,
    "slug": "quarterly-solstice-and-equinox-reading",
    "title": "Quarterly Solstice and Equinox Reading",
    "chapter": "Spreads For Festivals And Seasons",
    "purpose": "A seasonal spread aligned to the solar calendar's four turning points -- reading the primary quality of the quarter ahead, what needs to be completed before the next threshold, and what the season's energy most wants to support.",
    "positions": [
      "Card 1: Spring: What is growing/needs to grow in your life?",
      "Card 2: Summer: How can you best gain recognition/rewards for your efforts?",
      "Card 3: Fall: What has worked well and will continue to flourish in your life?",
      "Card 4: Winter: What needs preserving for longer-term results, and what to let go?",
      "Card 5: Which will be my best season in the year ahead?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread within the few days around a solstice or equinox. Reading it as close to the actual solar threshold as possible gives the most accurate energetic attunement."
  },
  {
    "number": 871,
    "slug": "monthly-energetic-alignment-roadmap",
    "title": "Monthly Energetic Alignment Roadmap",
    "chapter": "Spreads For Festivals And Seasons",
    "purpose": "A month-by-month spread that reads each of the next several months as a distinct energetic chapter rather than a uniform timeline. It shows where concentration, rest, relationship, and practicality each have their natural season.",
    "positions": [
      "Card 1: January: How can you make a wise investment/financial decision?",
      "Card 2: February: How can you improve your social life?",
      "Card 3: March: How can you successfully divide your time between two people who both need you?",
      "Card 4: April: Should you compete in an event even if you do not think you will win?",
      "Card 5: May: Should you invest in a new health or fitness regime, major beauty treatment, or cosmetic surgery?",
      "Card 6: June: Should you take up a completely new interest that has always fascinated you?",
      "Card 7: July: Should you spend more quality time with your partner/family/friends if you work 24/7?",
      "Card 8: August: Should you take center stage/seek extra recognition/reward for what you do?",
      "Card 9: September: Should you relax more and slow down in order to enjoy life and avoid making careless mistakes?",
      "Card 10: October: Should you avoid being involved in other people's quarrels/trying to keep everyone around you happy?",
      "Card 11: November: Should you focus on your spiritual self/explore your psychic abilities to keep you one step ahead?",
      "Card 12: December: Should you enroll to learn something new/take an opportunity to extend your skills when the New Year begins?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you want to understand the rhythm of the months ahead rather than plan their specific events. Lay all positions before reading any so the monthly pattern can be seen as a whole before individual details are examined."
  },
  {
    "number": 896,
    "slug": "choosing-legal-battle-vs-settlement",
    "title": "Choosing Legal Battle vs Settlement",
    "chapter": "Tarot Spreads And The Saints",
    "purpose": "A spread for the decision between litigation and resolution -- reading not just financial outcome but the cost in time, energy, and personal integrity of each path, and which one serves the larger truth of the situation.",
    "positions": [
      "Card 1: If you carry on to the bitter end and win, will you recoup your expenses and more and be vindicated?",
      "Card 2: If you lose the case, will you suffer a severe financial loss because of court costs?",
      "Card 3: Should you transfer to a no-win/no-fee lawyer (also known as a contingency fee agreement), or do you want to stay with the lawyer you know and trust even if they do not work on a no-win/no-fee arrangement?",
      "Card 4: If partial compensation can be negotiated outside court, would that be enough to prove to the world that you were in the right?",
      "Card 5: Should you risk all?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread before the decision point is forced by external legal timing. The cards give most precise guidance when there is still genuine agency over which path is taken."
  },
  {
    "number": 897,
    "slug": "resolving-bitter-family-feuds-quietly",
    "title": "Resolving Bitter Family Feuds Quietly",
    "chapter": "Tarot Spreads And The Saints",
    "purpose": "A three-card spread for reading the core of an entrenched family conflict -- what each party's unacknowledged need actually is, where the wound lives beneath the grievance, and what form of resolution would allow both sides to move forward without requiring one to be declared wrong.",
    "positions": [
      "Card 1: Can/should you deal with the underlying unhappiness that is causing the problem, or try to resolve it once and for all?",
      "Card 2: Is anybody causing trouble behind the scenes and offloading the blame?",
      "Card 3: Is this a long-standing problem that can only have a temporary fix to avoid immediate disruption?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when you want to understand the feud's root rather than rehearse its history. Read the underlying need positions before the resolution card."
  },
  {
    "number": 921,
    "slug": "athletic-performance-and-fitness-tarot",
    "title": "Athletic Performance and Fitness Tarot",
    "chapter": "The Go-For-It Spreads: Health, Fitness, Leisure, And Sports",
    "purpose": "A spread for reading the energetic and psychological dimensions of physical performance -- what is genuinely supporting athletic capacity right now, where mental or emotional patterns are limiting physical potential, and what specific focus would most improve the next training phase.",
    "positions": [
      "Card 1: Should you undertake serious training with the aim of turning professional?",
      "Card 2: Would you be happier just getting fit or joining a team for pleasure?",
      "Card 3: Would gentle exercise for personal satisfaction and health be just one part of your many wider interests or occupations?",
      "Card 4: If you go for the top, will you succeed totally/partly/be happy?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread during an active training period rather than at its start. The cards speak most precisely when there is already real effort to reflect on."
  },
  {
    "number": 922,
    "slug": "overcoming-body-image-anxiety-strategies",
    "title": "Overcoming Body Image Anxiety Strategies",
    "chapter": "The Go-For-It Spreads: Health, Fitness, Leisure, And Sports",
    "purpose": "A spread for reading the emotional and psychological landscape beneath body image distress -- naming where the negative self-assessment originated, what it is protecting, and what honest inner relationship with the body would most genuinely shift the experience.",
    "positions": [
      "Card 1: How you see yourself right now/what you feel is wrong or unattractive.",
      "Card 2: What, from the past/childhood/teenage years, made you doubt your attractiveness.",
      "Card 3: Who in your present life/what airbrushed media images are making you feel insecure about yourself?",
      "Card 4: Do others want/in the past wanted to unsettle you because of their own insecurities? Should you disregard this negativity?",
      "Card 5: Is becoming fitter a first step to improving your feelings about yourself?",
      "Card 6: Who/what can help to make this happen?",
      "Card 7: Will anyone perhaps implicated in"
    ],
    "use": "",
    "when": "Come to this spread when body-related anxiety has been present long enough to suggest its roots are worth examining. Approach each card as honest information rather than looking for reassurance."
  },
  {
    "number": 951,
    "slug": "embracing-alternative-non-traditional-lives",
    "title": "Embracing Alternative Non-Traditional Lives",
    "chapter": "Spreads For Alternative Lifestyles, Doing Your Own Thing, And Living Your Own Way",
    "purpose": "A five-card spread for reading the internal and external landscape of choosing a path that does not follow conventional expectations -- what is genuinely pulling you toward it, what you may need to grieve in leaving the familiar behind, and what practical foundation the alternative path actually requires.",
    "positions": [
      "Card 1: The barriers of convention that may still hold you back through the disapproval of others and all those old voices from childhood.",
      "Card 2: The wall of economic stability: How you would manage financially if you gave up your steady day job to earn money based on your initiative and ingenuity.",
      "Card 3: The hidden fear: What has sometimes held you back because it hasn't been examined and faced or overcome.",
      "Card 4: The practical organization, selling up and finding somewhere new to live, maybe not even a house but a boat or recreational vehicle, where to go, what if you fall ill.",
      "Card 5: The way of freedom."
    ],
    "use": "The full deck.",
    "when": "Come to this spread when you are genuinely considering a non-conventional direction rather than testing whether you are allowed to want it. The cards speak to what the path requires, not whether you deserve it."
  },
  {
    "number": 952,
    "slug": "managing-animal-sanctuaries-and-wildlife",
    "title": "Managing Animal Sanctuaries and Wildlife",
    "chapter": "Spreads For Alternative Lifestyles, Doing Your Own Thing, And Living Your Own Way",
    "purpose": "A spread for reading the energetic and practical dimensions of caring for animals in a structured context -- what the work most needs from you right now, where burnout or overwhelm are accumulating, and what specific support would most sustain both the animals and the person caring for them.",
    "positions": [
      "Card 1: Could/should you take it over even though it would need time and resources to get it up and running?",
      "Card 2: Would it be better to turn the offer down and look for land/buildings suitable for conversion to fulfill your own blueprint?",
      "Card 3: Should you accept but keep your day job/give yourself a time limit to make it a viable enterprise?",
      "Card 4: Will your dreams of saving wildlife materialize?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread when the work has been heavy long enough to make you wonder whether you are genuinely sustaining it or merely enduring it. The cards speak to sustainability, not just to commitment."
  },
  {
    "number": 976,
    "slug": "evaluating-casual-sex-vs-emotional-bond",
    "title": "Evaluating Casual Sex vs Emotional Bond",
    "chapter": "Passion And Temptation Spreads",
    "purpose": "A spread for reading the genuine desires and unspoken needs beneath a romantic or sexual situation -- what each person is actually seeking, where those needs align or diverge, and what honest communication would most prevent the situation from becoming regrettable.",
    "positions": [
      "Card 1: Are you happy with this arrangement for now/for the foreseeable future?",
      "Card 2: Do you want to spend time together/go on vacation, but your partner is not free?",
      "Card 3: Are you ready to risk the relationship by asking for more?",
      "Card 4: Are you outgrowing the relationship as fun but going nowhere?"
    ],
    "use": "The sixteen Court cards.",
    "when": "Come to this spread before the situation progresses to a point where clarity would be harder to act on. The cards are most useful as early information rather than retrospective analysis."
  },
  {
    "number": 977,
    "slug": "deciphering-mixed-intimacy-signals-in-love",
    "title": "Deciphering Mixed Intimacy Signals in Love",
    "chapter": "Passion And Temptation Spreads",
    "purpose": "A spread for reading a romantic situation where the signals from one person are inconsistent -- naming what the mixed messages most likely indicate, what the person sending them may not yet be ready to say, and what approach would most help you respond authentically rather than reactively.",
    "positions": [
      "Card 1: Is your new love generally shy/finds it hard to show affection?",
      "Card 2: Has your love come out of a bad",
      "Card 3: Should you take the initiative?",
      "Card 4: Should you arrange a weekend vacation where it's obvious that you are sharing a room?",
      "Card 5: Should you talk about the subject generally, or would that send him/her heading for the hills fast?",
      "Card 6: If the relationship is otherwise good and sex is seen as a serious step to commitment by your partner, should you wait until your partner is ready?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread when confusion about another person's intentions has been persistent enough to affect your own behaviour and decisions. Read the other person's position with genuine curiosity rather than a hypothesis already formed."
  },
  {
    "number": 989,
    "slug": "grief-counseling-for-sudden-accidental-death",
    "title": "Grief Counseling for Sudden Accidental Death",
    "chapter": "Spreads For Grief And Loss",
    "purpose": "A spread for navigating the specific shock and disorientation of sudden, traumatic loss -- reading what the grief most needs to begin moving through, what support is genuinely available, and what the soul of the departed may most want the living to receive.",
    "positions": [
      "Card 1: Do you have closure why/how the accident happened/justice against anyone to blame?",
      "Card 2: If not, can this/how can justice/closure be obtained, if necessary by increasing pressure for justice/an official inquiry?",
      "Card 3: How can you best remember the person at their most vibrant/collect memories in recordings/videos/photographs or a memory book so younger and future family members will know them?",
      "Card 4: What kind of a memorial would your relative have liked/at the place of the accident/in a favorite spot/a prize or trophy in their honor?",
      "Card 5: What can be done to campaign to prevent similar accidents/if, for example, it was a dangerous stretch of road or lack of safety measures in the workplace?",
      "Card 6: What can you do in your life that they planned to do in order to fulfill their wishes?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when the initial shock has begun to give way to the longer grief, and when there is enough stillness to sit with whatever the cards bring. This is a spread for gentleness above all else."
  },
  {
    "number": 990,
    "slug": "coping-with-unresolved-suspicious-loss",
    "title": "Coping with Unresolved Suspicious Loss",
    "chapter": "Spreads For Grief And Loss",
    "purpose": "A spread for grief that is complicated by unanswered questions -- reading what the grief itself needs separate from the need for answers, what is making it hardest to find peace, and what the person who is gone would most want the grieving person to receive.",
    "positions": [
      "Card 1: Do the circumstances of the death go against your relative's pattern of behavior/where they would have been/had unexplained injuries?",
      "Card 2: Was your relative worried but wouldn't explain why/was getting strange phone calls/had dubious friends/connections with drugs?",
      "Card 3: Are the police so overwhelmed that they are going for the easiest explanation/if you live in a small community could there be a cover-up?",
      "Card 4: Do you want justice/are prepared to hire a detective/go to an investigative journalist/a medium?",
      "Card 5: Although people say let it rest, are you determined justice will be done?",
      "Card 6: Do you just want to move away/let your relative rest in peace?",
      "Card 7: Will you get justice if you persist?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when the loss has been present long enough for the initial shock to have settled and the harder, slower grief has taken its place. Read the unresolved position without demanding it provide certainty."
  },
  {
    "number": 1001,
    "slug": "birthday-solar-return-planetary-map",
    "title": "Birthday Solar Return Planetary Map",
    "chapter": "Spread 1001",
    "purpose": "A birthday spread for reading the dominant energetic themes of the personal year ahead -- what the solar return is activating, what is being completed from the previous year, and what this year most wants to grow through you. It reads a personal year as a whole arc rather than a collection of events.",
    "positions": [
      "Card 1 that remains is your overall year theme;",
      "Card 2 is what is unexpected in the year ahead;",
      "Card 3 is a particular opportunity the year will bring; and",
      "Card 4 is the challenges to be overcome in the year ahead."
    ],
    "use": "Use the full deck, removing the Death and Devil cards before laying out the year review.",
    "when": "Come to this spread on or near your birthday, within the solar return window. Lay all cards before reading any so the year's full pattern can be seen before individual months or themes are examined."
  }
]"""
SPREADS: list[dict[str, Any]] = json.loads(SPREADS_JSON)
SPREAD_INDEX = {item["slug"]: item for item in SPREADS}
SPREAD_INDEX_BY_NUMBER = {item["number"]: item["slug"] for item in SPREADS}

MAJOR_CARDS = [('the-fool', 'The Fool'), ('the-magician', 'The Magician'), ('the-high-priestess', 'The High Priestess'), ('the-empress', 'The Empress'), ('the-emperor', 'The Emperor'), ('the-hierophant', 'The Hierophant'), ('the-lovers', 'The Lovers'), ('the-chariot', 'The Chariot'), ('strength', 'Strength'), ('the-hermit', 'The Hermit'), ('wheel-of-fortune', 'Wheel of Fortune'), ('justice', 'Justice'), ('the-hanged-man', 'The Hanged Man'), ('death', 'Death'), ('temperance', 'Temperance'), ('the-devil', 'The Devil'), ('the-tower', 'The Tower'), ('the-star', 'The Star'), ('the-moon', 'The Moon'), ('the-sun', 'The Sun'), ('judgement', 'Judgement'), ('the-world', 'The World')]
MAJOR_MEANINGS = {'the-fool': {'upright': 'fresh possibility, trust, and a leap into the unknown', 'reversed': 'hesitation, naivety, or a leap made without grounding', 'imagery': 'the cliff edge, white rose, small dog, and open sky speak of innocence meeting destiny'}, 'the-magician': {'upright': 'focus, skill, and manifesting power through intention', 'reversed': 'scattered energy, mixed motives, or talent that is not fully owned', 'imagery': 'the raised wand, infinity sign, and tools on the table show power translated into action'}, 'the-high-priestess': {'upright': 'intuition, inner knowing, and a truth that ripens in silence', 'reversed': 'blocked intuition, secrecy, or confusion around what is felt', 'imagery': 'the moon crown, veil, and scroll suggest mystery, memory, and sacred inner knowledge'}, 'the-empress': {'upright': 'abundance, nourishment, sensuality, and fertile growth', 'reversed': 'overgiving, creative stagnation, or emotional depletion', 'imagery': 'the wheat field, Venus symbols, and lush cushions evoke beauty, comfort, and creation'}, 'the-emperor': {'upright': 'structure, authority, and mature leadership', 'reversed': 'rigidity, control struggles, or leadership rooted in fear', 'imagery': 'the ram throne, armour, and mountain backdrop suggest discipline and command'}, 'the-hierophant': {'upright': 'tradition, guidance, and meaningful spiritual teaching', 'reversed': 'restlessness with convention, dogma, or misfit values', 'imagery': 'the temple pillars, keys, and blessing hand point to lineage and formal wisdom'}, 'the-lovers': {'upright': 'alignment, intimacy, and values-based choice', 'reversed': 'misalignment, temptation, or a decision that splits heart and mind', 'imagery': 'the angel, mountain, and mirrored figures show union, choice, and sacred reflection'}, 'the-chariot': {'upright': 'direction, confidence, and purposeful momentum', 'reversed': 'drift, divided will, or ambition without control', 'imagery': 'the charioteer, black and white sphinxes, and city behind him speak of mastery through focus'}, 'strength': {'upright': 'courage, patience, and heart-led steadiness', 'reversed': 'self-doubt, emotional exhaustion, or force replacing trust', 'imagery': 'the lion, infinity sign, and calm hand show power expressed as gentleness'}, 'the-hermit': {'upright': 'solitude, wisdom, and a search for what is true', 'reversed': 'withdrawal, avoidance, or staying alone longer than needed', 'imagery': 'the lantern, staff, and mountain peak reflect reflection, maturity, and inner guidance'}, 'wheel-of-fortune': {'upright': 'turning points, luck, and destiny in motion', 'reversed': 'delays, resistance to change, or repeating cycles', 'imagery': 'the turning wheel, winged beings, and rising figures show life in dynamic transition'}, 'justice': {'upright': 'truth, balance, and clear consequence', 'reversed': 'imbalance, evasion, or accountability blurred by bias', 'imagery': 'the scales, sword, and straight-backed figure represent honesty and measured judgment'}, 'the-hanged-man': {'upright': 'pause, surrender, and a change in perspective', 'reversed': 'stalling, sacrifice without meaning, or clinging to an old angle', 'imagery': 'the suspended posture and halo show wisdom gained through release'}, 'death': {'upright': 'ending, transformation, and necessary renewal', 'reversed': 'holding on, fear of letting go, or delayed closure', 'imagery': 'the white rose, river, and rising sun point to rebirth through endings'}, 'temperance': {'upright': 'integration, healing, and measured flow', 'reversed': 'excess, impatience, or imbalance in rhythm', 'imagery': 'the mixing cups, one foot on land and one in water, and distant path signify harmony in motion'}, 'the-devil': {'upright': 'attachment, temptation, and shadow desire', 'reversed': 'release, awareness, or breaking a harmful loop', 'imagery': 'the chains, torch, and goat-like figure reveal bondage sustained by habit or fear'}, 'the-tower': {'upright': 'shock, revelation, and structures breaking apart', 'reversed': 'avoided change, private collapse, or truth delayed', 'imagery': 'lightning, falling crown, and broken tower represent truth that cannot stay hidden'}, 'the-star': {'upright': 'hope, healing, and spiritual freshness', 'reversed': 'discouragement, dim faith, or healing still in process', 'imagery': 'the pouring water, stars, and naked openness reflect renewal and trust'}, 'the-moon': {'upright': 'intuition, dream logic, and the half-seen path', 'reversed': 'fear, emotional fog, or truths surfacing slowly', 'imagery': 'the moon, path, towers, and animals speak of instinct, illusion, and deeper feeling'}, 'the-sun': {'upright': 'joy, clarity, and wholehearted vitality', 'reversed': 'temporary clouds, ego heat, or light that feels muted', 'imagery': 'the child, horse, sunflowers, and bright sky evoke life force and innocence'}, 'judgement': {'upright': 'awakening, reckoning, and a call to rise', 'reversed': 'self-judgment, hesitation, or avoiding the next level', 'imagery': 'the trumpet, rising figures, and open landscape imply a soul-level awakening'}, 'the-world': {'upright': 'completion, fulfilment, and integration', 'reversed': 'unfinished business, delays, or a threshold not yet crossed', 'imagery': 'the wreath, four creatures, and dancing figure suggest mastery and wholeness'}}
SUIT_META = {'wands': {'label': 'Wands', 'element': 'Fire', 'love': 'desire, attraction, and chemistry', 'career': 'ambition, leadership, and enterprise', 'health': 'stamina, motivation, and burnout risk', 'imagery': 'wands, sprouting wood, and flames point to drive and life force'}, 'cups': {'label': 'Cups', 'element': 'Water', 'love': 'emotion, intimacy, and receptivity', 'career': 'team harmony, creative work, and morale', 'health': 'nervous-system sensitivity and emotional wellbeing', 'imagery': 'chalices, flowing water, and moonlit scenes speak of feeling and intuition'}, 'swords': {'label': 'Swords', 'element': 'Air', 'love': 'boundaries, truth, and mental distance', 'career': 'strategy, conflict, and decision pressure', 'health': 'stress, sleep quality, and cognitive overload', 'imagery': 'blades, clouds, and strong winds show thought, tension, and clarity'}, 'pentacles': {'label': 'Pentacles', 'element': 'Earth', 'love': 'reliability, practical care, and long-term building', 'career': 'income, craft, and material progress', 'health': 'body routines, recovery, and tangible habits', 'imagery': 'coins, gardens, and architecture point to growth in the physical world'}}
RANK_DETAILS = {'ace': ('Ace', 'beginnings and pure potential'), '02': ('Two', 'choice and balancing forces'), '03': ('Three', 'collaboration and early growth'), '04': ('Four', 'stability and the need to consolidate'), '05': ('Five', 'friction, challenge, and adjustment'), '06': ('Six', 'movement, support, and regained rhythm'), '07': ('Seven', 'testing, discernment, and strategy'), '08': ('Eight', 'momentum, skill, and focused repetition'), '09': ('Nine', 'culmination, resilience, and hard-won perspective'), '10': ('Ten', 'completion, weight, and full consequence'), 'page': ('Page', 'curiosity, learning, and a fresh message'), 'knight': ('Knight', 'motion, pursuit, and committed effort'), 'queen': ('Queen', 'mastery through embodiment and inner authority'), 'king': ('King', 'leadership, direction, and mature command')}
INTENTIONS = {'love': {'label': 'Love', 'chapter': 'love and commitment', 'spread_numbers': [87, 88, 91], 'best_cards': ['the-lovers', 'two-of-cups', 'the-empress', 'the-sun', 'ten-of-cups', 'the-star'], 'caution_cards': ['three-of-swords', 'the-devil', 'the-moon', 'five-of-cups']}, 'career': {'label': 'Career', 'chapter': 'career and vocational direction', 'spread_numbers': [169, 171, 191], 'best_cards': ['the-magician', 'the-emperor', 'three-of-pentacles', 'ace-of-pentacles', 'six-of-wands', 'the-world'], 'caution_cards': ['five-of-swords', 'eight-of-swords', 'the-tower', 'five-of-pentacles']}, 'money': {'label': 'Money', 'chapter': 'prosperity and financial clarity', 'spread_numbers': [129, 149, 151], 'best_cards': ['ace-of-pentacles', 'nine-of-pentacles', 'ten-of-pentacles', 'the-empress', 'king-of-pentacles', 'wheel-of-fortune'], 'caution_cards': ['five-of-pentacles', 'seven-of-swords', 'the-devil', 'four-of-pentacles']}, 'health': {'label': 'Health', 'chapter': 'healing and energetic balance', 'spread_numbers': [321, 322, 921], 'best_cards': ['the-star', 'strength', 'temperance', 'the-sun', 'queen-of-cups', 'six-of-swords'], 'caution_cards': ['nine-of-swords', 'ten-of-wands', 'the-moon', 'five-of-cups']}, 'relationships': {'label': 'Relationships', 'chapter': 'relationships and emotional connection', 'spread_numbers': [90, 108, 109], 'best_cards': ['two-of-cups', 'temperance', 'the-lovers', 'queen-of-cups', 'ten-of-cups', 'judgement'], 'caution_cards': ['five-of-wands', 'the-devil', 'seven-of-swords', 'three-of-swords']}, 'breakup': {'label': 'Breakup', 'chapter': 'heartbreak, reconciliation, and release', 'spread_numbers': [111, 112, 989], 'best_cards': ['death', 'the-star', 'six-of-swords', 'judgement', 'ace-of-cups'], 'caution_cards': ['five-of-cups', 'three-of-swords', 'the-tower', 'ten-of-swords']}, 'new-beginnings': {'label': 'New Beginnings', 'chapter': 'fresh starts and transitions', 'spread_numbers': [70, 720, 773], 'best_cards': ['the-fool', 'ace-of-wands', 'ace-of-pentacles', 'the-sun', 'the-magician', 'the-world'], 'caution_cards': ['the-hanged-man', 'five-of-pentacles', 'the-moon', 'four-of-cups']}, 'anxiety': {'label': 'Anxiety', 'chapter': 'anxiety, phobia, and emotional overwhelm', 'spread_numbers': [321, 323, 741], 'best_cards': ['strength', 'temperance', 'the-star', 'queen-of-cups', 'six-of-swords', 'the-hermit'], 'caution_cards': ['nine-of-swords', 'the-moon', 'eight-of-swords', 'ten-of-wands']}, 'decision-making': {'label': 'Decision-Making', 'chapter': 'choices, crossroads, and strategy', 'spread_numbers': [14, 64, 592], 'best_cards': ['justice', 'two-of-wands', 'the-chariot', 'the-magician', 'wheel-of-fortune', 'king-of-swords'], 'caution_cards': ['seven-of-cups', 'two-of-swords', 'the-moon', 'the-hanged-man']}, 'spiritual-growth': {'label': 'Spiritual Growth', 'chapter': 'inner life and sacred development', 'spread_numbers': [775, 848, 850], 'best_cards': ['the-high-priestess', 'the-hermit', 'judgement', 'the-star', 'ace-of-cups', 'temperance'], 'caution_cards': ['the-devil', 'seven-of-cups', 'eight-of-swords', 'five-of-swords']}, 'family': {'label': 'Family', 'chapter': 'family patterns and home ties', 'spread_numbers': [265, 266, 897], 'best_cards': ['ten-of-cups', 'ten-of-pentacles', 'the-empress', 'six-of-cups', 'queen-of-pentacles', 'the-sun'], 'caution_cards': ['five-of-wands', 'the-devil', 'seven-of-swords', 'five-of-cups']}, 'travel': {'label': 'Travel', 'chapter': 'travel, relocation, and distance', 'spread_numbers': [566, 567, 568], 'best_cards': ['the-chariot', 'six-of-swords', 'the-world', 'ace-of-wands', 'temperance', 'wheel-of-fortune'], 'caution_cards': ['eight-of-cups', 'five-of-pentacles', 'the-moon', 'seven-of-swords']}, 'manifestation': {'label': 'Manifestation', 'chapter': 'wishes, fortune, and desired outcomes', 'spread_numbers': [211, 236, 238], 'best_cards': ['the-magician', 'ace-of-wands', 'ace-of-pentacles', 'the-star', 'wheel-of-fortune', 'the-sun'], 'caution_cards': ['seven-of-cups', 'four-of-cups', 'the-devil', 'five-of-pentacles']}, 'self-discovery': {'label': 'Self-Discovery', 'chapter': 'self-awareness and inner understanding', 'spread_numbers': [820, 821, 822], 'best_cards': ['the-hermit', 'the-high-priestess', 'strength', 'queen-of-cups', 'judgement', 'the-world'], 'caution_cards': ['the-moon', 'eight-of-swords', 'five-of-swords', 'four-of-cups']}, 'forgiveness': {'label': 'Forgiveness', 'chapter': 'release, amends, and softer truth', 'spread_numbers': [108, 110, 720], 'best_cards': ['temperance', 'judgement', 'six-of-cups', 'ace-of-cups', 'the-star', 'strength'], 'caution_cards': ['five-of-swords', 'the-devil', 'three-of-swords', 'the-tower']}, 'loss-grief': {'label': 'Loss and Grief', 'chapter': 'grief, mourning, and healing after loss', 'spread_numbers': [989, 991, 720], 'best_cards': ['the-star', 'six-of-swords', 'temperance', 'judgement', 'ace-of-cups', 'queen-of-cups'], 'caution_cards': ['five-of-cups', 'ten-of-swords', 'the-tower', 'nine-of-swords']}, 'friendship': {'label': 'Friendship', 'chapter': 'social life and platonic bonds', 'spread_numbers': [411, 412, 413], 'best_cards': ['three-of-cups', 'six-of-cups', 'queen-of-cups', 'page-of-cups', 'the-sun', 'temperance'], 'caution_cards': ['five-of-wands', 'seven-of-swords', 'five-of-cups', 'three-of-swords']}, 'pregnancy': {'label': 'Pregnancy', 'chapter': 'fertility, conception, and parenthood', 'spread_numbers': [441, 442, 443], 'best_cards': ['the-empress', 'ace-of-cups', 'queen-of-pentacles', 'the-sun', 'ten-of-cups', 'page-of-cups'], 'caution_cards': ['the-moon', 'five-of-pentacles', 'nine-of-swords', 'ten-of-wands']}, 'legal-matters': {'label': 'Legal Matters', 'chapter': 'justice, compensation, and truth', 'spread_numbers': [467, 468, 469], 'best_cards': ['justice', 'king-of-swords', 'six-of-wands', 'judgement', 'ace-of-swords', 'the-emperor'], 'caution_cards': ['seven-of-swords', 'five-of-swords', 'the-tower', 'eight-of-swords']}, 'past-lives': {'label': 'Past Lives', 'chapter': 'karmic memory and soul recognition', 'spread_numbers': [87, 850, 88], 'best_cards': ['judgement', 'the-high-priestess', 'the-moon', 'six-of-cups', 'the-world', 'wheel-of-fortune'], 'caution_cards': ['the-devil', 'five-of-cups', 'eight-of-swords', 'three-of-swords']}}
INTRO_SNIPPETS = {'love': 'Tarot can show where a bond feels mutual, where timing is off, and what emotional truth wants to be named.', 'career': 'Tarot is especially useful for career questions because it exposes motivation, environment, and the hidden cost of each path.', 'money': 'Money readings work best when tarot is used for clarity, values, and timing instead of magical certainty.', 'health': 'Health spreads are best used as reflective tools around stress, recovery, rhythm, and support rather than medical diagnosis.', 'relationships': 'Relationship spreads help separate chemistry, commitment, conflict, and long-term compatibility into clearer layers.', 'breakup': 'Breakup spreads create language for grief, unfinished patterns, and whether healing points toward reunion or release.', 'new-beginnings': 'New-beginning spreads are powerful when you need confidence, cleaner timing, and a better sense of what the next chapter asks of you.', 'anxiety': 'Tarot can be grounding in anxious periods because it gives the mind a structured way to name fear, pattern, and next steps.', 'decision-making': 'Decision spreads help by comparing consequences, motives, and the path of least regret.', 'spiritual-growth': 'Spiritual spreads invite stillness, symbolism, and a more intuitive reading of what your inner life is asking for.', 'family': 'Family spreads are useful when love and duty are tangled, and everyone seems to carry a different version of the truth.', 'travel': 'Travel spreads do more than say yes or no: they reveal timing, safety, motivation, and what the journey is trying to teach.', 'manifestation': 'Manifestation spreads work best when desire is matched with honest action, patience, and alignment.', 'self-discovery': 'Self-discovery spreads reveal the roles you have outgrown and the strengths you have not yet trusted enough.', 'forgiveness': 'Forgiveness spreads show what can soften, what still needs a boundary, and whether reconciliation is wise.', 'loss-grief': 'Grief spreads offer symbolic structure when words are difficult and feelings move in uneven waves.', 'friendship': 'Friendship spreads help clarify reciprocity, trust, and the social patterns that keep repeating.', 'pregnancy': 'Pregnancy and conception spreads are best approached gently, holding space for hope, fear, and practical support.', 'legal-matters': 'Legal spreads can illuminate fairness, leverage, timing, and whether a compromise serves you better than a fight.', 'past-lives': 'Past-life themed spreads are read symbolically, often surfacing karmic echoes, unfinished emotional memory, and soul recognition motifs.'}

def _guess_card_count(spread: dict[str, Any]) -> int:
    if spread.get("positions"):
        return len(spread["positions"])
    chapter = spread.get("chapter", "").lower()
    for word, value in [("one-card", 1), ("two-card", 2), ("three-card", 3), ("four-card", 4), ("five-card", 5), ("six-card", 6), ("seven-card", 7), ("eight-card", 8), ("nine-card", 9), ("multi-card", 12)]:
        if word in chapter:
            return value
    if spread.get("number") == 1001:
        return 12
    return 6

def _default_positions(count: int) -> list[str]:
    labels = ["Card 1: The heart of the question", "Card 2: The pressure or tension around it", "Card 3: What is emerging next", "Card 4: What supports progress", "Card 5: What needs honesty or release", "Card 6: The likely direction", "Card 7: The inner lesson", "Card 8: The outer influence", "Card 9: The hope or fear underneath", "Card 10: The integrating message", "Card 11: The long-view factor", "Card 12: The closing wisdom"]
    return labels[:count]

def _sample_card_pool() -> list[dict[str, str]]:
    return [{"name": "The Magician", "meaning": "focused will turns intention into practical movement"}, {"name": "The Star", "meaning": "hope and recovery create breathing room"}, {"name": "Justice", "meaning": "truth and accountability refine the decision"}, {"name": "Ace of Cups", "meaning": "a new emotional opening changes the tone"}, {"name": "Three of Pentacles", "meaning": "support and skill-building improve the outcome"}, {"name": "Six of Swords", "meaning": "a transition away from strain begins"}, {"name": "The Sun", "meaning": "clarity arrives when the path is simplified"}, {"name": "Queen of Cups", "meaning": "sensitivity and trust in intuition are essential"}, {"name": "Wheel of Fortune", "meaning": "timing shifts and opportunity starts moving"}, {"name": "Strength", "meaning": "steady courage matters more than force"}, {"name": "The World", "meaning": "a chapter closes with real integration"}, {"name": "Ten of Pentacles", "meaning": "the long-term picture becomes easier to secure"}]

def list_spread_summaries() -> list[dict[str, Any]]:
    return [{"slug": spread["slug"], "title": spread["title"], "chapter": spread["chapter"], "purpose": spread["purpose"], "card_count": _guess_card_count(spread)} for spread in SPREADS]

def get_spread(slug: str) -> dict[str, Any] | None:
    spread = SPREAD_INDEX.get(slug)
    if not spread:
        return None
    card_count = _guess_card_count(spread)
    positions = spread.get("positions") or _default_positions(card_count)
    sample_pool = _sample_card_pool()
    sample_reading = []
    for index, position in enumerate(positions):
        card = sample_pool[index % len(sample_pool)]
        sample_reading.append({"position": position, "card": card["name"], "interpretation": card["meaning"]})
    when_to_use = [spread["purpose"], f"Use this spread when the theme of {spread['chapter'].lower()} feels active and you want more structure than a one-card pull.", f"It works well when you can stay with all {card_count} positions long enough to notice the pattern instead of only the first answer."]
    how_to = ["Take a moment to settle your question into one sentence before you shuffle.", f"Lay out {card_count} cards in order, keeping the positions distinct rather than rushing to the conclusion.", "Read each position on its own first, then look for repeated symbols, suit emphasis, and reversals.", "End by summarising the message in plain language and noting one practical next step."]
    faq = [{"question": f"What is the {spread['title']} tarot spread for?", "answer": spread["purpose"]}, {"question": f"How many cards are in the {spread['title']} spread?", "answer": f"This page reads the spread as a {card_count}-card layout."}, {"question": f"When should I use the {spread['title']} spread?", "answer": spread["when"] or f"Use it when questions around {spread['chapter'].lower()} need more context than a quick draw."}, {"question": f"Do I need a full deck for the {spread['title']} spread?", "answer": spread["use"] or "A full 78-card deck works best unless you intentionally want a smaller reading range."}]
    return {"slug": spread["slug"], "title": spread["title"], "chapter": spread["chapter"], "purpose": spread["purpose"], "card_count": card_count, "positions": positions, "diagram": positions, "how_to": how_to, "sample_reading": sample_reading, "when_to_use": when_to_use, "faq": faq, "meta_title": f"{spread['title']} Tarot Spread - How to Do It and What It Reveals", "meta_description": f"Learn the {spread['title']} tarot spread: layout, positions, when to use it, and a sample reading walkthrough.", "schema_howto_steps": [{"name": "Clarify the question", "text": how_to[0]}, {"name": "Lay the cards", "text": how_to[1]}, {"name": "Read each position", "text": how_to[2]}, {"name": "Summarise the guidance", "text": how_to[3]}]}

def _build_cards() -> list[dict[str, Any]]:
    return json.loads(r"""[
  {
    "slug": "the-fool",
    "name": "The Fool",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Fool upright brings fresh possibility, trust, and a leap into the unknown into the foreground. It belongs to situations where discovery only happens after the first honest step is taken.",
    "reversed": "Reversed, The Fool can point to hesitation, naivety, or a leap made without grounding. Most of the time, the deeper issue is not danger itself but the urge to eliminate all uncertainty before living.",
    "love": "In love, The Fool points to an unscripted connection that grows through openness instead of guarantees.",
    "career": "In career matters, The Fool often marks the first brave step into work that has not fully proven itself yet.",
    "health": "For wellbeing, The Fool can reflect renewal that begins with lightness, movement, and fewer doom-scripts.",
    "imagery": "the cliff edge, white rose, small dog, and open sky speak of innocence meeting destiny"
  },
  {
    "slug": "the-magician",
    "name": "The Magician",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Magician upright brings focus, skill, and manifesting power through intention into the foreground. Its gift is precision: the will to act, the tools to act well, and the nerve to begin now.",
    "reversed": "Reversed, The Magician can point to scattered energy, mixed motives, or talent that is not fully owned. When this card turns, ability is still present, but it may be leaking through distraction, performance, or mixed intention.",
    "love": "In love, The Magician points to clear chemistry backed by intention and follow-through.",
    "career": "In career matters, The Magician often marks a moment when skill, timing, and self-belief can turn ideas into tangible results.",
    "health": "For wellbeing, The Magician can reflect better outcomes when you actively work with your habits instead of hoping they fix themselves.",
    "imagery": "the raised wand, infinity sign, and tools on the table show power translated into action"
  },
  {
    "slug": "the-high-priestess",
    "name": "The High Priestess",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The High Priestess upright brings intuition, inner knowing, and a truth that ripens in silence into the foreground. The answer is often already sensed before it can be logically defended, which is exactly why stillness matters here.",
    "reversed": "Reversed, The High Priestess can point to blocked intuition, secrecy, or confusion around what is felt. Noise, secrecy, or self-doubt can make genuine intuition feel harder to trust than other people's opinions.",
    "love": "In love, The High Priestess points to quiet but unmistakable emotional knowing, especially when words have not caught up yet.",
    "career": "In career matters, The High Priestess often marks wisdom that comes from observation, timing, and not revealing every card too early.",
    "health": "For wellbeing, The High Priestess can reflect healing that depends on rest, hormonal sensitivity, and listening to subtler body signals.",
    "imagery": "the moon crown, veil, and scroll suggest mystery, memory, and sacred inner knowledge"
  },
  {
    "slug": "the-empress",
    "name": "The Empress",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Empress upright brings abundance, nourishment, sensuality, and fertile growth into the foreground. It signals growth that wants to be fed, protected, and enjoyed rather than managed into exhaustion.",
    "reversed": "Reversed, The Empress can point to overgiving, creative stagnation, or emotional depletion. The imbalance usually appears where care has turned into depletion or where creation has lost its natural rhythm.",
    "love": "In love, The Empress points to warmth, receptivity, and affection that makes both people feel more fully alive.",
    "career": "In career matters, The Empress often marks creative fertility, resourcefulness, and the ability to grow something sustainable.",
    "health": "For wellbeing, The Empress can reflect recovery through nourishment, softness, and respect for the body's natural cycles.",
    "imagery": "the wheat field, Venus symbols, and lush cushions evoke beauty, comfort, and creation"
  },
  {
    "slug": "the-emperor",
    "name": "The Emperor",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Emperor upright brings structure, authority, and mature leadership into the foreground. This card stabilises the field by asking for boundaries, structure, and decisions that can actually hold weight.",
    "reversed": "Reversed, The Emperor can point to rigidity, control struggles, or leadership rooted in fear. Its shadow appears when control hardens into fear, pride, or the refusal to adapt.",
    "love": "In love, The Emperor points to the need for safety, consistency, and mature boundaries inside attraction.",
    "career": "In career matters, The Emperor often marks authority, organisation, and leadership that must be earned rather than merely claimed.",
    "health": "For wellbeing, The Emperor can reflect better stability through routine, discipline, and stronger physical boundaries.",
    "imagery": "the ram throne, armour, and mountain backdrop suggest discipline and command"
  },
  {
    "slug": "the-hierophant",
    "name": "The Hierophant",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Hierophant upright brings tradition, guidance, and meaningful spiritual teaching into the foreground. It favours tested wisdom, good instruction, and the kind of guidance that has survived more than one season of doubt.",
    "reversed": "Reversed, The Hierophant can point to restlessness with convention, dogma, or misfit values. The problem is not tradition itself but the point where borrowed rules stop serving the living truth of the situation.",
    "love": "In love, The Hierophant points to shared values, defined commitment, and the question of what kind of bond you both truly honour.",
    "career": "In career matters, The Hierophant often marks training, mentorship, certification, or alignment with a respected framework.",
    "health": "For wellbeing, The Hierophant can reflect support that comes from sound guidance, consistent practice, and time-tested methods.",
    "imagery": "the temple pillars, keys, and blessing hand point to lineage and formal wisdom"
  },
  {
    "slug": "the-lovers",
    "name": "The Lovers",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Lovers upright brings alignment, intimacy, and values-based choice into the foreground. At its best, this card is not only about romance but about choosing in a way that keeps the heart and conscience aligned.",
    "reversed": "Reversed, The Lovers can point to misalignment, temptation, or a decision that splits heart and mind. Its strain shows up when attraction, values, and action start pulling in different directions.",
    "love": "In love, The Lovers points to mutual attraction that also asks for honesty, consent, and values-based choice.",
    "career": "In career matters, The Lovers often marks choices that cannot be made well unless desire and integrity are both present.",
    "health": "For wellbeing, The Lovers can reflect healing that improves when inner conflict is reduced and decisions stop splitting the self.",
    "imagery": "the angel, mountain, and mirrored figures show union, choice, and sacred reflection"
  },
  {
    "slug": "the-chariot",
    "name": "The Chariot",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Chariot upright brings direction, confidence, and purposeful momentum into the foreground. Momentum is available, but it has to be directed; raw force without steering will not do the job.",
    "reversed": "Reversed, The Chariot can point to drift, divided will, or ambition without control. When the reins slip, ambition can scatter into frustration, overpush, or conflict between competing drives.",
    "love": "In love, The Chariot points to strong attraction that needs direction, emotional maturity, and clear intention to avoid becoming pure momentum.",
    "career": "In career matters, The Chariot often marks focused ambition, strategic movement, and the will to take command of the road ahead.",
    "health": "For wellbeing, The Chariot can reflect progress through disciplined effort without tipping into overexertion or control battles.",
    "imagery": "the charioteer, black and white sphinxes, and city behind him speak of mastery through focus"
  },
  {
    "slug": "strength",
    "name": "Strength",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "Strength upright brings courage, patience, and heart-led steadiness into the foreground. Its power is quiet, relational, and steady; nothing in this card needs domination to be effective.",
    "reversed": "Reversed, Strength can point to self-doubt, emotional exhaustion, or force replacing trust. The shadow appears when fear, fatigue, or self-criticism makes gentleness feel weaker than force.",
    "love": "In love, Strength points to trust built through patience, tenderness, and emotional steadiness under pressure.",
    "career": "In career matters, Strength often marks leadership that calms the room, holds the line, and does not waste energy proving itself.",
    "health": "For wellbeing, Strength can reflect resilience strengthened by nervous-system regulation, pacing, and self-trust.",
    "imagery": "the lion, infinity sign, and calm hand show power expressed as gentleness"
  },
  {
    "slug": "the-hermit",
    "name": "The Hermit",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Hermit upright brings solitude, wisdom, and a search for what is true into the foreground. This is the wisdom of stepping back far enough to hear what is true without the crowd deciding it for you.",
    "reversed": "Reversed, The Hermit can point to withdrawal, avoidance, or staying alone longer than needed. Isolation becomes unhelpful when reflection stops being restorative and starts becoming a hiding place.",
    "love": "In love, The Hermit points to the need for space, honesty, and emotional maturity rather than constant noise or reassurance.",
    "career": "In career matters, The Hermit often marks solitary mastery, deep study, and decisions that need distance before they need action.",
    "health": "For wellbeing, The Hermit can reflect repair that comes through rest, simplification, and listening to what the body says in quieter moments.",
    "imagery": "the lantern, staff, and mountain peak reflect reflection, maturity, and inner guidance"
  },
  {
    "slug": "wheel-of-fortune",
    "name": "Wheel of Fortune",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "Wheel of Fortune upright brings turning points, luck, and destiny in motion into the foreground. It marks a turning tide: timing changes, patterns move, and what felt fixed begins to rotate again.",
    "reversed": "Reversed, Wheel of Fortune can point to delays, resistance to change, or repeating cycles. Resistance to change can make the cycle feel harsher, slower, or more repetitive than it actually is.",
    "love": "In love, Wheel of Fortune points to changing tides in attachment, timing, and the strange luck that brings two lives into contact.",
    "career": "In career matters, Wheel of Fortune often marks an opening created by timing, market movement, or a cycle finally turning in your favour.",
    "health": "For wellbeing, Wheel of Fortune can reflect the body moving through a cycle that requires adaptation rather than rigid expectation.",
    "imagery": "the turning wheel, winged beings, and rising figures show life in dynamic transition"
  },
  {
    "slug": "justice",
    "name": "Justice",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "Justice upright brings truth, balance, and clear consequence into the foreground. This card strips drama away and asks what is accurate, proportionate, and ethically supportable.",
    "reversed": "Reversed, Justice can point to imbalance, evasion, or accountability blurred by bias. Its shadow lives where denial, bias, or avoidance makes the scales impossible to balance cleanly.",
    "love": "In love, Justice points to clear-eyed accountability, fair exchange, and the courage to name what is true.",
    "career": "In career matters, Justice often marks decisions with legal, ethical, or contractual weight that must stand up to scrutiny.",
    "health": "For wellbeing, Justice can reflect wellbeing shaped by cause and effect, personal responsibility, and practical correction.",
    "imagery": "the scales, sword, and straight-backed figure represent honesty and measured judgment"
  },
  {
    "slug": "the-hanged-man",
    "name": "The Hanged Man",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Hanged Man upright brings pause, surrender, and a change in perspective into the foreground. Nothing is lost in this pause if the pause changes what you are finally willing to see.",
    "reversed": "Reversed, The Hanged Man can point to stalling, sacrifice without meaning, or clinging to an old angle. Frustration grows when waiting becomes passive stalling rather than meaningful surrender.",
    "love": "In love, The Hanged Man points to the need to stop forcing a story and let a different perspective arrive.",
    "career": "In career matters, The Hanged Man often marks a strategic pause, reframing period, or necessary suspension before the next move is clear.",
    "health": "For wellbeing, The Hanged Man can reflect recovery that depends on rest, surrender, and a willingness to stop pushing against the process.",
    "imagery": "the suspended posture and halo show wisdom gained through release"
  },
  {
    "slug": "death",
    "name": "Death",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "Death upright brings ending, transformation, and necessary renewal into the foreground. Its medicine is clean release: something has reached its end, and life wants the next truth to begin.",
    "reversed": "Reversed, Death can point to holding on, fear of letting go, or delayed closure. Clinging to what is already over can make the transition feel more punishing than it needs to be.",
    "love": "In love, Death points to the end of an old relational pattern, whether that means closure or a deeper rebirth.",
    "career": "In career matters, Death often marks a chapter closing so that a truer role, structure, or ambition can replace it.",
    "health": "For wellbeing, Death can reflect necessary shedding, detoxifying, or letting go of habits that the body has outgrown.",
    "imagery": "the white rose, river, and rising sun point to rebirth through endings"
  },
  {
    "slug": "temperance",
    "name": "Temperance",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "Temperance upright brings integration, healing, and measured flow into the foreground. It is the art of blending without losing yourself, and of healing through proportion rather than extremes.",
    "reversed": "Reversed, Temperance can point to excess, impatience, or imbalance in rhythm. Imbalance shows where timing is forced, dosage is wrong, or competing needs are never truly integrated.",
    "love": "In love, Temperance points to emotional balance, mutual adjustment, and affection that matures through patience.",
    "career": "In career matters, Temperance often marks measured progress, collaboration, and skilful blending of different demands or talents.",
    "health": "For wellbeing, Temperance can reflect recovery through moderation, integration, and nervous-system steadiness.",
    "imagery": "the mixing cups, one foot on land and one in water, and distant path signify harmony in motion"
  },
  {
    "slug": "the-devil",
    "name": "The Devil",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Devil upright brings attachment, temptation, and shadow desire into the foreground. This card exposes the hook: the bond, craving, or fear that gains power when it goes unnamed.",
    "reversed": "Reversed, The Devil can point to release, awareness, or breaking a harmful loop. Freedom starts the moment the pattern is seen clearly enough to interrupt, even if the habit is not fully broken yet.",
    "love": "In love, The Devil points to desire entangled with attachment, obsession, power, or the fear of being without the bond.",
    "career": "In career matters, The Devil often marks pressure created by unhealthy ambition, dependency, or a bargain that costs too much spiritually.",
    "health": "For wellbeing, The Devil can reflect the impact of compulsions, shame loops, and habits that drain vitality while pretending to soothe.",
    "imagery": "the chains, torch, and goat-like figure reveal bondage sustained by habit or fear"
  },
  {
    "slug": "the-tower",
    "name": "The Tower",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Tower upright brings shock, revelation, and structures breaking apart into the foreground. It does not ask whether the old structure was comfortable; it asks whether it was true enough to survive revelation.",
    "reversed": "Reversed, The Tower can point to avoided change, private collapse, or truth delayed. The shock may be delayed, internalised, or softened, but the false structure still wants to come down.",
    "love": "In love, The Tower points to a sudden truth that breaks illusion and forces the relationship onto real ground.",
    "career": "In career matters, The Tower often marks disruption that clears out a shaky system, exposed weakness, or unsustainable plan.",
    "health": "For wellbeing, The Tower can reflect a wake-up call that demands immediate honesty about stress, overload, or what has been ignored.",
    "imagery": "lightning, falling crown, and broken tower represent truth that cannot stay hidden"
  },
  {
    "slug": "the-star",
    "name": "The Star",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Star upright brings hope, healing, and spiritual freshness into the foreground. Hope here is not fantasy but recovery: the kind that returns after the nervous system remembers safety.",
    "reversed": "Reversed, The Star can point to discouragement, dim faith, or healing still in process. When dimmed, the task is usually not to create hope from nothing but to clear what keeps blocking it.",
    "love": "In love, The Star points to healing, tenderness, and the return of faith after disappointment.",
    "career": "In career matters, The Star often marks renewed direction, inspiration, and work that reconnects effort to meaning.",
    "health": "For wellbeing, The Star can reflect repair, replenishment, and gradual restoration after strain or illness.",
    "imagery": "the pouring water, stars, and naked openness reflect renewal and trust"
  },
  {
    "slug": "the-moon",
    "name": "The Moon",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Moon upright brings intuition, dream logic, and the half-seen path into the foreground. The path is real even when the light is partial; this card asks for discernment rather than panic.",
    "reversed": "Reversed, The Moon can point to fear, emotional fog, or truths surfacing slowly. Confusion starts lifting once projection, denial, or unprocessed feeling is named for what it is.",
    "love": "In love, The Moon points to ambiguity, projection, strong feeling, and the need to separate intuition from fear.",
    "career": "In career matters, The Moon often marks unclear politics, mixed signals, or a process that is still too hidden to judge quickly.",
    "health": "For wellbeing, The Moon can reflect fluctuating moods, sleep sensitivity, and symptoms intensified by anxiety or uncertainty.",
    "imagery": "the moon, path, towers, and animals speak of instinct, illusion, and deeper feeling"
  },
  {
    "slug": "the-sun",
    "name": "The Sun",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The Sun upright brings joy, clarity, and wholehearted vitality into the foreground. It is a clarifying card: warmth, visibility, joy, and life force all become easier to trust in its presence.",
    "reversed": "Reversed, The Sun can point to temporary clouds, ego heat, or light that feels muted. Even shaded, the sun has not gone away; the work is clearing what is muting its natural brightness.",
    "love": "In love, The Sun points to openhearted affection, visible joy, and a bond that feels life-giving rather than guarded.",
    "career": "In career matters, The Sun often marks recognition, confidence, and success that thrives in the light instead of behind the curtain.",
    "health": "For wellbeing, The Sun can reflect vitality, optimism, and the body benefiting from rhythm, warmth, and clearer energy.",
    "imagery": "the child, horse, sunflowers, and bright sky evoke life force and innocence"
  },
  {
    "slug": "judgement",
    "name": "Judgement",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "Judgement upright brings awakening, reckoning, and a call to rise into the foreground. This is the call to answer your own life differently after seeing the pattern with new honesty.",
    "reversed": "Reversed, Judgement can point to self-judgment, hesitation, or avoiding the next level. Avoiding the call can look like self-doubt, procrastination, or keeping an old identity alive past its time.",
    "love": "In love, Judgement points to reckoning, forgiveness, and the chance to relate from a more awakened level.",
    "career": "In career matters, Judgement often marks a professional calling, review point, or decision that asks you to stand by your deeper purpose.",
    "health": "For wellbeing, Judgement can reflect healing linked to truth-telling, release, and the body responding to a more authentic life direction.",
    "imagery": "the trumpet, rising figures, and open landscape imply a soul-level awakening"
  },
  {
    "slug": "the-world",
    "name": "The World",
    "arcana": "major",
    "suit": null,
    "rank": null,
    "upright": "The World upright brings completion, fulfilment, and integration into the foreground. Completion here is not a finish line alone but the feeling of a cycle becoming whole enough to bless the next one.",
    "reversed": "Reversed, The World can point to unfinished business, delays, or a threshold not yet crossed. The final step may still be pending, but the card usually shows that the larger pattern is already close to completion.",
    "love": "In love, The World points to maturity, wholeness, and relationships that fit into a larger, lived sense of completion.",
    "career": "In career matters, The World often marks successful completion, integration, and work that connects multiple lessons into one coherent result.",
    "health": "For wellbeing, The World can reflect wellbeing supported by integration, grounded embodiment, and a stronger sense of being at home in yourself.",
    "imagery": "the wreath, four creatures, and dancing figure suggest mastery and wholeness"
  },
  {
    "slug": "ace-of-wands",
    "name": "Ace of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "ace",
    "upright": "Ace of Wands marks the first moment of genuine creative impulse -- before doubt, before planning, when the spark is cleaner than any argument against it. Something new is trying to begin, and this card says yes.",
    "reversed": "Reversed, Ace of Wands points to an impulse that fired prematurely, fizzled before it could be tested, or was delayed by something external. The energy is still present but may need better timing or a clearer intention before it can ignite.",
    "love": "In love, Ace of Wands brings bold attraction, a new relationship that starts with unmistakable chemistry, or the return of desire to something that had grown routine.",
    "career": "In career, Ace of Wands points to a new project, idea, or creative direction that is ready to be launched before all the conditions are perfect.",
    "health": "For wellbeing, Ace of Wands reflects renewed energy, physical vitality, or the impulse to start a new health routine before the habit has had time to form.",
    "imagery": "Ace of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-wands",
    "name": "Two of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "02",
    "upright": "Two of Wands shows someone who has made a first move and is now standing at the edge of a larger world, holding the map and deciding whether to cross. The ambition is real; the question is whether to settle or venture further.",
    "reversed": "Reversed, Two of Wands reflects a plan that stays on paper too long, fear of the larger step, or scattered direction that prevents commitment to any single path. The vision is present but obscured by indecision.",
    "love": "In love, Two of Wands points to a relationship testing whether both people share the same longer horizon -- whether this attraction is also a compatible direction.",
    "career": "In career, Two of Wands marks the moment after an initial success when the question is whether to expand, partner, or simply hold the ground already gained.",
    "health": "For wellbeing, Two of Wands reflects stepping beyond a comfortable health habit and looking toward what sustained improvement would actually require.",
    "imagery": "Two of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-wands",
    "name": "Three of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "03",
    "upright": "Three of Wands shows enterprise already in motion -- ships sent out, waiting for their return. The work has been done; the outcome is still in transit. The card carries the patience of someone who prepared well and trusts the process.",
    "reversed": "Reversed, Three of Wands points to delays in expected returns, expansion plans meeting resistance, or an inability to see far enough ahead to plan effectively. The preparation may have been incomplete or the timing misjudged.",
    "love": "In love, Three of Wands brings patient confidence in a developing connection -- or the discomfort of waiting for someone who has not yet returned the same level of investment.",
    "career": "In career, Three of Wands marks the phase between launching a project and seeing its results -- where trust in the work already done must carry the gap.",
    "health": "For wellbeing, Three of Wands reflects gradual progress where the results are still catching up to the effort already invested.",
    "imagery": "Three of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-wands",
    "name": "Four of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "04",
    "upright": "Four of Wands signals a genuine milestone -- a homecoming, a harvest, or the formal acknowledgment that something built together deserves marking. The atmosphere is festive and the foundation beneath it is real.",
    "reversed": "Reversed, Four of Wands points to a celebration cut short, an incomplete sense of homecoming, or joy that feels unstable because the foundation has not been fully secured.",
    "love": "In love, Four of Wands marks a significant relational milestone -- an engagement, a move-in, a shared threshold crossed -- where commitment becomes visible and concrete.",
    "career": "In career, Four of Wands signals the successful completion of a professional phase -- a launch, graduation, or promotion -- where the achievement is real enough to merit proper recognition.",
    "health": "For wellbeing, Four of Wands reflects recovery fully achieved, a new healthy environment established, or the body settling into a rhythm that finally feels sustainable.",
    "imagery": "Four of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-wands",
    "name": "Five of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "05",
    "upright": "Five of Wands brings friction, competing voices, and the productive disorder of people who all think they have the right answer. The conflict is often not malicious but energetic -- the challenge of getting aligned when everyone approaches differently.",
    "reversed": "Reversed, Five of Wands points to avoidance of necessary conflict, suppressed competition, or the exhaustion of ongoing argument without resolution. The friction has either gone underground or worn people past productive engagement.",
    "love": "In love, Five of Wands reflects tension, differing communication styles, or the ongoing friction of two people who approach emotion, decision, and expectation differently.",
    "career": "In career, Five of Wands points to team conflict, competitive pressure, or the challenge of getting alignment when multiple stakeholders have incompatible priorities.",
    "health": "For wellbeing, Five of Wands reflects scattered energy, competing demands, or the physical toll of sustained effort in a chaotic or adversarial environment.",
    "imagery": "Five of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-wands",
    "name": "Six of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "06",
    "upright": "Six of Wands marks a public victory -- the triumphant return, the winner's announcement, recognition that visible effort earns when it finally delivers. The confidence here is real, not borrowed.",
    "reversed": "Reversed, Six of Wands points to recognition delayed, ego that has outpaced the actual achievement, or success that arrived privately when public acknowledgment was needed.",
    "love": "In love, Six of Wands brings a moment of renewed attraction -- where effort to pursue or improve has been visibly rewarded and the relationship enters a prouder phase.",
    "career": "In career, Six of Wands signals genuine professional success -- a promotion, award, or project that delivers publicly, where the achievement is undeniable and well-timed.",
    "health": "For wellbeing, Six of Wands reflects visible improvement -- a fitness goal achieved, a recovery milestone passed -- where the body's progress is something you can see and others notice.",
    "imagery": "Six of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-wands",
    "name": "Seven of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "07",
    "upright": "Seven of Wands places someone on a defended height, under pressure from below. The position was earned, but holding it requires ongoing effort. This card is about resilience under persistent challenge -- staying when leaving would be easier.",
    "reversed": "Reversed, Seven of Wands points to a position surrendered too quickly, defensiveness hardening into stubbornness, or the exhaustion of fighting on a front that no longer serves the larger goal.",
    "love": "In love, Seven of Wands reflects the challenge of holding to one's values when a partner pushes back -- or the difficulty of staying present in a relationship that requires constant effort.",
    "career": "In career, Seven of Wands marks a professional position under competitive pressure -- defending territory, managing critics, or maintaining authority where challengers are visible and persistent.",
    "health": "For wellbeing, Seven of Wands reflects the mental and physical cost of sustained stress -- where staying functional requires deliberate effort to protect energy from ongoing demands.",
    "imagery": "Seven of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-wands",
    "name": "Eight of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "08",
    "upright": "Eight of Wands brings sudden swift movement -- communication flying, decisions accelerating, the air thick with incoming information. After a period of stillness or deliberation, everything is now moving at once.",
    "reversed": "Reversed, Eight of Wands points to delays after expected speed, messages lost in transit, or energy moving in crossed directions that cancel rather than compound. Communication errors are common here.",
    "love": "In love, Eight of Wands brings rapid developments -- messages returned quickly, feelings declared, or a relationship that accelerates past its expected pace.",
    "career": "In career, Eight of Wands signals a sudden burst of activity -- project momentum, multiple communications requiring response, or a window of opportunity that opens briefly and must be used now.",
    "health": "For wellbeing, Eight of Wands reflects a body returning to high function after slow recovery -- or the need to pace a surge of returning energy before it leads to burnout.",
    "imagery": "Eight of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-wands",
    "name": "Nine of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "09",
    "upright": "Nine of Wands shows someone still standing after taking real damage -- not triumphant, but upright. The battle has left marks; the question is whether enough remains to finish what was started. The card is honest about the cost and still says: continue.",
    "reversed": "Reversed, Nine of Wands points to the moment when the final push was too much -- when exhaustion overran resilience and retreat became necessary rather than chosen. The wound may need tending before the battle can resume.",
    "love": "In love, Nine of Wands reflects a relationship marked by past hurts -- where previous losses make it harder to stay open, and trust is rebuilt slowly and carefully.",
    "career": "In career, Nine of Wands marks a professional situation requiring persistence through fatigue -- holding a position or completing a long campaign where the finish line is finally visible.",
    "health": "For wellbeing, Nine of Wands reflects the body's resilience near the end of a sustained health challenge -- still functional but drawing on reserves that need careful management.",
    "imagery": "Nine of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-wands",
    "name": "Ten of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "10",
    "upright": "Ten of Wands shows someone carrying more than they should -- not because the load isn't real, but because they have taken on responsibility that belongs to others or no longer serves the original purpose. The burden is heavy and the end is in sight.",
    "reversed": "Reversed, Ten of Wands can point to the moment of release -- burdens set down, delegation accepted, or tasks abandoned because the cost finally outweighed the mission. It can also signal collapse before the relief arrives.",
    "love": "In love, Ten of Wands reflects one person shouldering the emotional labour of a relationship that has become unbalanced -- carrying too much of the maintenance, communication, or repair.",
    "career": "In career, Ten of Wands marks an overloaded professional situation -- too many responsibilities, a project grown beyond its scope, or a workload producing diminishing returns.",
    "health": "For wellbeing, Ten of Wands reflects physical or mental exhaustion from overextension -- where the body has been pushed past sustainable capacity and is asking clearly for rest.",
    "imagery": "Ten of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-wands",
    "name": "Page of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "page",
    "upright": "Page of Wands arrives with news, enthusiasm, and an appetite for everything new. The energy is exploratory -- not yet tested by consequence, but genuinely excited about possibility. Ideas arrive quickly; commitment follows more slowly.",
    "reversed": "Reversed, Page of Wands points to scattered enthusiasm with no follow-through, creative energy that generates more starts than completions, or messages delivered without enough maturity to land well.",
    "love": "In love, Page of Wands brings youthful attraction, the excitement of early connection, or new flirtatious energy entering a relationship that had grown too familiar.",
    "career": "In career, Page of Wands signals the arrival of a creative opportunity or inspiring idea -- a new direction worth exploring, even if the details are not yet fully formed.",
    "health": "For wellbeing, Page of Wands reflects renewed motivation -- the fresh impulse to try something new with the body before the discipline to sustain it has developed.",
    "imagery": "Page of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-wands",
    "name": "Knight of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "knight",
    "upright": "Knight of Wands charges in fast, acts first, and asks questions when the dust settles. The energy is magnetic and brave, but the speed can leave people and plans behind. This is someone who lives for momentum and is uncomfortable with pause.",
    "reversed": "Reversed, Knight of Wands reflects recklessness at full speed -- action without sufficient thought, conflict sparked through impatience, or energy that burns a situation down before it had a chance to build.",
    "love": "In love, Knight of Wands brings passionate pursuit that may or may not be accompanied by patience -- intense attraction, bold gestures, and the question of whether the flame can be sustained.",
    "career": "In career, Knight of Wands signals bold, fast-moving action -- launching before full preparation, or driving a project forward through sheer force of will.",
    "health": "For wellbeing, Knight of Wands reflects a burst of physical energy or exercise motivation -- intense, possibly overdone, and worth tempering with equal attention to recovery.",
    "imagery": "Knight of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-wands",
    "name": "Queen of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "queen",
    "upright": "Queen of Wands owns the room through warmth and natural magnetism rather than authority. She knows her creative power and uses it without apology -- confidence that invites others rather than excluding them.",
    "reversed": "Reversed, Queen of Wands points to charisma turned brittle -- confidence shading into aggression, warmth weaponised into manipulation, or creative power blocked by external criticism or internal self-doubt.",
    "love": "In love, Queen of Wands brings radiant confidence, playful warmth, and a partner who makes the relationship feel alive -- or calls you toward a version of yourself more fully expressed.",
    "career": "In career, Queen of Wands marks leadership through inspiration -- someone who draws the best from a team through genuine enthusiasm and the willingness to act as a creative anchor.",
    "health": "For wellbeing, Queen of Wands reflects vitality as a lived practice -- someone who has learned to protect and channel their energy rather than depleting it in every direction.",
    "imagery": "Queen of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-wands",
    "name": "King of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "king",
    "upright": "King of Wands leads through vision rather than process. He has converted his creative fire into a sustainable force -- something that can be directed, taught, and handed forward. The authority is real because the results are.",
    "reversed": "Reversed, King of Wands points to leadership that has become dictatorial, vision hardened into arrogance, or entrepreneurial energy burning through collaborators faster than it builds.",
    "love": "In love, King of Wands brings commanding attention, clear intention, and the challenge of a partner whose vision for life is strong enough to either inspire or overwhelm.",
    "career": "In career, King of Wands marks the fully realised entrepreneurial leader -- someone with a track record, a clear vision, and the capacity to mobilise others toward a larger goal.",
    "health": "For wellbeing, King of Wands reflects mastery of the body's energy -- knowing how to sustain high performance without the burnout cycles that plagued earlier chapters.",
    "imagery": "King of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises leadership, direction, and mature command."
  },
  {
    "slug": "ace-of-cups",
    "name": "Ace of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "ace",
    "upright": "Ace of Cups brings the overflowing cup -- pure emotional potential, love in its freshest form, before expectation or history enters. Whatever is beginning here has the quality of genuine opening: receptive, unguarded, and full.",
    "reversed": "Reversed, Ace of Cups points to emotional numbness, a heart closed for self-protection, or love offered but unable to be received. The cup is present but tipped -- what should flow is blocked or draining before it lands.",
    "love": "In love, Ace of Cups marks new emotional beginnings -- first love, renewed feeling, or the moment a connection becomes genuinely heartfelt rather than just convenient.",
    "career": "In career, Ace of Cups signals work becoming emotionally meaningful again -- a creative opportunity or role aligned with what you genuinely care about.",
    "health": "For wellbeing, Ace of Cups reflects emotional healing becoming available -- the moment when softness and receptivity start replacing guarded or depleted patterns.",
    "imagery": "Ace of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-cups",
    "name": "Two of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "02",
    "upright": "Two of Cups marks the moment two people recognise each other -- not the full story yet, but the mutual signal that something real is beginning. The connection is equal, conscious, and chosen.",
    "reversed": "Reversed, Two of Cups points to attraction without compatibility, imbalance in emotional investment, or a partnership that looked mutual but turned out to be one-sided.",
    "love": "In love, Two of Cups is the card of genuine mutual feeling -- where both people are equally present, equally choosing, and the energy between them flows both ways.",
    "career": "In career, Two of Cups marks the beginning of a meaningful professional partnership -- where two people's skills and values complement each other in a way that benefits both.",
    "health": "For wellbeing, Two of Cups reflects the healing power of genuine connection -- where a trusted relationship provides emotional balance and the body relaxes into supported calm.",
    "imagery": "Two of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-cups",
    "name": "Three of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "03",
    "upright": "Three of Cups brings genuine celebration -- not of achievement but of connection. The joy here is shared and spontaneous, rising naturally when the right people are in the right place together.",
    "reversed": "Reversed, Three of Cups points to social situations that feel hollow, overindulgence, gossip among friends, or a community that has fractured and lost its warmth.",
    "love": "In love, Three of Cups brings friendship as a foundation for romance -- relationships where genuine joy is mutual and the connection feels expansive rather than exclusive.",
    "career": "In career, Three of Cups signals creative collaboration where the team's combined output exceeds what any individual could produce -- a genuine collective that feeds rather than drains its members.",
    "health": "For wellbeing, Three of Cups reflects the health benefit of social joy -- laughter, ease, and the immune system's response to belonging rather than isolation.",
    "imagery": "Three of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-cups",
    "name": "Four of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "04",
    "upright": "Four of Cups shows someone so absorbed in their own internal conversation that they miss what is being offered. The cup extended toward them is real; they simply haven't looked up. The contemplation is genuine but has become its own obstacle.",
    "reversed": "Reversed, Four of Cups signals the moment of re-engagement -- finally looking up, accepting what was waiting, or ending the withdrawal and returning to participation.",
    "love": "In love, Four of Cups reflects emotional withdrawal, missed gestures, or a partner so absorbed in their own mood that they cannot receive what is offered.",
    "career": "In career, Four of Cups points to professional dissatisfaction, missed opportunity, or the inability to feel motivated by options that a clearer mind might recognise as worthwhile.",
    "health": "For wellbeing, Four of Cups reflects the lethargy and low motivation that accompany genuine disconnection from one's own life.",
    "imagery": "Four of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-cups",
    "name": "Five of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "05",
    "upright": "Five of Cups focuses on what has been lost -- the spilled cups, the grief, the genuine sorrow of something that mattered and is now gone. The upright cups behind the figure are real, but the attention is still on the spill.",
    "reversed": "Reversed, Five of Cups signals the beginning of turning around -- noticing the upright cups, acknowledging that something remains. The grief has not gone but the gaze has begun to lift.",
    "love": "In love, Five of Cups reflects heartbreak, disappointment, or the aftermath of emotional loss -- a time when grief is more present than possibility.",
    "career": "In career, Five of Cups marks professional disappointment -- a project failed, a role lost, a goal not achieved -- where the loss is real and needs genuine acknowledgment before moving forward.",
    "health": "For wellbeing, Five of Cups reflects the physical weight of grief -- where sadness registers in the body as fatigue, appetite changes, or the particular exhaustion of sustained sorrow.",
    "imagery": "Five of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-cups",
    "name": "Six of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "06",
    "upright": "Six of Cups carries the scent of the past -- childhood ease, kindness without agenda, the warmth of something that existed before complication. The connection it holds is genuine but belongs to an earlier time.",
    "reversed": "Reversed, Six of Cups points to nostalgia preventing forward movement, an idealised past blocking honest engagement with the present, or an old connection returned without the conditions to sustain it.",
    "love": "In love, Six of Cups brings the return of an old connection, the comfort of a relationship built on genuine history, or the bittersweet awareness of what once existed.",
    "career": "In career, Six of Cups can point to returning to earlier work, reconnecting with original career motivations, or benefiting from a professional relationship built long ago.",
    "health": "For wellbeing, Six of Cups reflects healing through reconnection with what once made the body feel genuinely well -- rhythms, practices, or environments from an earlier period.",
    "imagery": "Six of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-cups",
    "name": "Seven of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "07",
    "upright": "Seven of Cups places someone before a cloud of choices, each more enticing than the last and none of them fully real yet. The imagination is vivid and the desire is genuine, but no choice has been made, and not choosing has its own consequences.",
    "reversed": "Reversed, Seven of Cups signals the clearing of illusion -- seeing options more clearly, making a choice from a more grounded place, or losing the comforting fog that made avoiding the decision feel manageable.",
    "love": "In love, Seven of Cups reflects fantasised connections, confusion between what is real and what is projected, or difficulty committing when imagination provides endless alternatives.",
    "career": "In career, Seven of Cups points to too many directions, creative overwhelm, or the temptation of shiny opportunities not yet tested against reality.",
    "health": "For wellbeing, Seven of Cups reflects avoidance through distraction -- the way escapism or fantasy can substitute for the grounded, honest engagement the body actually needs.",
    "imagery": "Seven of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-cups",
    "name": "Eight of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "08",
    "upright": "Eight of Cups shows someone walking away from something that was, by every external measure, enough -- but internally no longer is. The figure leaves in the dark, alone. This is the quieter courage: choosing to seek what is missing even when what remains is safe.",
    "reversed": "Reversed, Eight of Cups points to staying when leaving is the more honest choice -- or to someone who left impulsively and is now questioning whether the departure was premature.",
    "love": "In love, Eight of Cups marks the quiet turning point -- the realisation that a relationship is not fulfilling something essential, and the growing awareness that staying requires a different quality of honesty.",
    "career": "In career, Eight of Cups signals leaving a role or organisation that no longer holds meaning -- even when the external rewards are intact -- because something more aligned is being sought.",
    "health": "For wellbeing, Eight of Cups reflects deliberate withdrawal from patterns or environments that have been quietly draining vitality -- a retreat made for the sake of restoration.",
    "imagery": "Eight of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-cups",
    "name": "Nine of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "09",
    "upright": "Nine of Cups carries the quiet confidence of someone who has arrived somewhere they genuinely wanted to reach. The satisfaction is emotional, internal, and complete. This is the wish card -- not wished for, but fulfilled.",
    "reversed": "Reversed, Nine of Cups points to wishes fulfilled on the surface but hollow inside, material satisfaction without meaning, or complacency settled where real contentment once was.",
    "love": "In love, Nine of Cups reflects emotional fullness -- a relationship where both people feel genuinely happy, cared for, and alive to something they value.",
    "career": "In career, Nine of Cups marks genuine professional satisfaction -- work that delivers on what was hoped for, recognition that feels earned, or a role where creative and practical fulfilment coexist.",
    "health": "For wellbeing, Nine of Cups reflects the body returning to genuine ease -- not performance of wellness but the real felt experience of being physically and emotionally at rest.",
    "imagery": "Nine of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-cups",
    "name": "Ten of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "10",
    "upright": "Ten of Cups shows the full emotional harvest -- family, belonging, lasting joy -- the emotional equivalent of home. This is not perfect happiness but something more durable: the feeling of being in the right place with the right people, and knowing it.",
    "reversed": "Reversed, Ten of Cups points to family systems whose external harmony masks real dysfunction, or to emotional promises not yet delivered in the domestic situation.",
    "love": "In love, Ten of Cups marks relational wholeness -- a partnership that has moved through its tests and arrived somewhere stable, warm, and fully chosen.",
    "career": "In career, Ten of Cups reflects work integrated into a life well-lived -- where the professional and personal are no longer in conflict and the daily rhythm supports something genuinely good.",
    "health": "For wellbeing, Ten of Cups reflects the deeply restorative effect of belonging -- where feeling at home in one's relationships directly supports physical vitality and emotional regulation.",
    "imagery": "Ten of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-cups",
    "name": "Page of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "page",
    "upright": "Page of Cups carries news from the emotional world -- a message from intuition, a surprising feeling, or a creative idea arriving through an unexpected channel. The energy is gentle, imaginative, and often catches people off guard.",
    "reversed": "Reversed, Page of Cups points to emotional immaturity, messages misread or miscommunicated, or creative sensitivity that has turned inward and become fragility rather than openness.",
    "love": "In love, Page of Cups brings soft, tentative feeling -- the very beginning of romantic awareness, or an emotional message from a connection that hasn't yet been given words.",
    "career": "In career, Page of Cups signals an invitation toward creative or emotionally meaningful work -- a new project or role that asks for both skill and genuine care.",
    "health": "For wellbeing, Page of Cups reflects the importance of emotional acknowledgment -- where physical symptoms are closely tied to feelings that haven't been processed or expressed.",
    "imagery": "Page of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-cups",
    "name": "Knight of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "knight",
    "upright": "Knight of Cups arrives bearing his heart openly -- romantic, artistic, idealistic, moving toward what he loves rather than what makes strategic sense. The pursuit is genuine even if the follow-through is uncertain.",
    "reversed": "Reversed, Knight of Cups points to seductive charm that doesn't follow through, romantic energy that exists only in the gesture rather than the commitment, or emotions that swing between intensity and sudden withdrawal.",
    "love": "In love, Knight of Cups brings romantic pursuit, heartfelt declarations, and attentive emotional presence that feels both flattering and sometimes overwhelming.",
    "career": "In career, Knight of Cups marks the movement toward work that aligns with passion -- following creative or service-oriented instincts rather than career strategy.",
    "health": "For wellbeing, Knight of Cups reflects emotional sensitivity that can both elevate mood and leave the body vulnerable to the physical effects of disappointment or romantic intensity.",
    "imagery": "Knight of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-cups",
    "name": "Queen of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "queen",
    "upright": "Queen of Cups holds her cup steady even while fully present to the depth of her feeling. She is not swept away -- she comprehends emotion, receives it, and reflects it back with extraordinary care. Her empathy is a practised art.",
    "reversed": "Reversed, Queen of Cups points to emotional boundaries dissolved, empathy that has become self-erasure, or intuitive gifts turned inward in depression or codependency.",
    "love": "In love, Queen of Cups brings profound emotional attunement -- the rare experience of feeling genuinely seen and held without needing to explain or justify what is felt.",
    "career": "In career, Queen of Cups marks mastery in emotionally demanding roles -- counselling, healing, teaching -- where the work requires both depth of feeling and the stability to hold space for others.",
    "health": "For wellbeing, Queen of Cups reflects the body responding to genuine emotional care -- where tending to the emotional landscape directly improves physical ease.",
    "imagery": "Queen of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-cups",
    "name": "King of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "king",
    "upright": "King of Cups has brought his emotional world under wise governance. He neither suppresses nor is ruled by feeling -- he understands it, acts from it with integrity, and remains steady when others' emotional weather would pull him under.",
    "reversed": "Reversed, King of Cups points to emotional volatility in someone who normally holds it together, manipulation through charm, or a leader whose unacknowledged wounds are quietly shaping decisions.",
    "love": "In love, King of Cups brings emotional maturity -- a partner who is fully present without losing themselves, whose depth of feeling is matched by stability and genuine care.",
    "career": "In career, King of Cups marks leadership through emotional intelligence -- the manager who keeps teams functioning through upheaval, the mentor who draws out what is best in others.",
    "health": "For wellbeing, King of Cups reflects the resilience that comes from emotional regulation -- where deep self-understanding insulates against the physical toll of suppressed or unmanaged feeling.",
    "imagery": "King of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises leadership, direction, and mature command."
  },
  {
    "slug": "ace-of-swords",
    "name": "Ace of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "ace",
    "upright": "Ace of Swords cuts through confusion with the clean force of a new idea or an honest recognition. Where there was fog, there is now a clear edge. The sword cuts both ways -- it reveals what is true and removes what is not, regardless of comfort.",
    "reversed": "Reversed, Ace of Swords points to a truth not yet spoken, a decision clouded by confusion, or mental clarity that has become cruelty rather than precision. The blade has not yet found its honest angle.",
    "love": "In love, Ace of Swords brings honesty that may be uncomfortable -- a conversation that clears the air, a recognition that cuts through self-deception, or the beginning of a mentally stimulating connection.",
    "career": "In career, Ace of Swords marks a breakthrough -- a new idea with real merit, a decision finally made with clarity, or intellectual force that cuts through a problem no one else has been willing to name directly.",
    "health": "For wellbeing, Ace of Swords reflects a diagnosis named, a pattern finally understood, or the mental clarity that arrives when the body stops being treated as an object and starts being listened to.",
    "imagery": "Ace of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-swords",
    "name": "Two of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "02",
    "upright": "Two of Swords shows someone sitting in deliberate blindness -- blades crossed, eyes covered, facing water that represents emotion not yet consulted. The mind is keeping the decision at bay because both options feel equally difficult.",
    "reversed": "Reversed, Two of Swords signals the blindfold finally removed -- seeing the situation as it actually is, with all the discomfort that brings -- or a decision forced by someone else's timing rather than made freely.",
    "love": "In love, Two of Swords reflects an emotional standoff -- two people who have both withdrawn behind their defenses, equally unwilling to make the first move toward honest communication.",
    "career": "In career, Two of Swords marks a professional decision where neither option feels clearly right, and the delay itself is becoming an answer that may not serve.",
    "health": "For wellbeing, Two of Swords reflects the mental tension of unresolved health decisions -- where anxiety about the choice creates more strain than either option itself would.",
    "imagery": "Two of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-swords",
    "name": "Three of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "03",
    "upright": "Three of Swords lands hard. The three blades through the heart represent grief that is real and must be felt -- betrayal, loss, a painful truth that arrived without preparation. This card does not soften what has happened.",
    "reversed": "Reversed, Three of Swords points to grief slowly releasing, a wound beginning to close, or pain that refuses to process and has become chronic -- carried long past the time when it served any protective function.",
    "love": "In love, Three of Swords marks heartbreak -- the sorrow of betrayal, the ache of separation, or the pain of finally seeing what could not be made to work.",
    "career": "In career, Three of Swords reflects the genuine emotional cost of professional loss -- a termination, a public failure, or a collaboration that ended with hurt feelings not cleanly resolved.",
    "health": "For wellbeing, Three of Swords reflects grief making itself known in the body -- where emotional pain registers as physical heaviness, chest tightness, or the particular exhaustion of sustained sorrow.",
    "imagery": "Three of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-swords",
    "name": "Four of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "04",
    "upright": "Four of Swords signals rest as a strategic necessity -- the knight laid to rest not because the battle is lost but because rest is what makes continuing possible. The recovery is deliberate, not defeated.",
    "reversed": "Reversed, Four of Swords points to a return to action that is too soon, rest that became avoidance, or the inability to remain still even when the body and mind are clearly asking for it.",
    "love": "In love, Four of Swords marks a necessary pause -- where both people step back from pressure or conflict and allow the relationship's underlying connection to reset.",
    "career": "In career, Four of Swords signals strategic withdrawal -- taking a break between intense professional efforts rather than burning out before the next phase begins.",
    "health": "For wellbeing, Four of Swords is one of the clearest health cards -- the body is asking for rest, recovery, and reduced stimulation, and honouring that request is exactly right.",
    "imagery": "Four of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-swords",
    "name": "Five of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "05",
    "upright": "Five of Swords shows the aftermath of a conflict won at a cost no one feels proud of. The swords are collected but the retreating figures tell the real story -- this was not a victory that serves the larger whole.",
    "reversed": "Reversed, Five of Swords points to a conflict finally over, an ego battle released, or the slow acknowledgment that winning was less important than the relationship or integrity sacrificed to get there.",
    "love": "In love, Five of Swords reflects a pattern of winning arguments at the cost of the relationship -- where the need to be right damages what both people actually value.",
    "career": "In career, Five of Swords marks competition that became damaging -- office politics, undermining behaviour, or achieving a goal through methods difficult to look back on without regret.",
    "health": "For wellbeing, Five of Swords reflects the physical toll of sustained conflict -- where the body holds the residue of repeated stress responses and needs release rather than more battle.",
    "imagery": "Five of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-swords",
    "name": "Six of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "06",
    "upright": "Six of Swords shows a difficult passage -- moving from turbulent water toward calmer shores. The journey is not triumphant, the figure still carries their swords, but the direction is undeniably better and the transition is underway.",
    "reversed": "Reversed, Six of Swords points to a transition stalled -- unable to leave the troubled water, resistance to the necessary passage, or a return to a difficult situation after a brief departure.",
    "love": "In love, Six of Swords marks moving through and beyond difficulty -- a relationship entering a calmer, more stable phase, or the honest leaving of one that was genuinely beyond repair.",
    "career": "In career, Six of Swords signals transition -- a role, field, or environment left behind in favour of something better suited to future development, even if the crossing is uncomfortable.",
    "health": "For wellbeing, Six of Swords reflects gradual improvement following illness, mental health challenge, or exhaustion -- movement in the right direction, not yet arrival.",
    "imagery": "Six of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-swords",
    "name": "Seven of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "07",
    "upright": "Seven of Swords carries the energy of someone who takes what they need without asking and leaves before they can be held accountable. The strategy can be necessary -- acting alone is sometimes the only way -- but the deception has a cost.",
    "reversed": "Reversed, Seven of Swords points to deception uncovered, a strategy that backfired, or the return of honesty after avoidance. It can also reflect self-deception -- the lies told to oneself more than others.",
    "love": "In love, Seven of Swords reflects dishonesty, hidden behaviour, or someone emotionally evasive -- acting alone in ways that undermine the trust the relationship depends on.",
    "career": "In career, Seven of Swords marks strategic cunning -- cutting corners, taking credit without acknowledgment, or acting unilaterally in ways that secure short-term advantage while damaging longer-term trust.",
    "health": "For wellbeing, Seven of Swords reflects avoidance of health realities -- delaying the conversation with the doctor, ignoring the symptom, or managing the surface while something real goes unaddressed.",
    "imagery": "Seven of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-swords",
    "name": "Eight of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "08",
    "upright": "Eight of Swords shows restriction that is largely self-created -- the figure is bound but the binding is loose, and the blindfold is the more confining thing. The prison is real but the walls are partly built from belief.",
    "reversed": "Reversed, Eight of Swords signals the loosening of self-imposed restriction -- the blindfold removed, the bindings fallen, the realisation that more movement was always available than the fear allowed.",
    "love": "In love, Eight of Swords reflects feeling trapped by a relationship -- where the barrier is more internal than external, maintained by the story told about what is possible.",
    "career": "In career, Eight of Swords marks professional paralysis -- the inability to move toward better options because the mind has constructed an airtight case for staying stuck.",
    "health": "For wellbeing, Eight of Swords reflects anxiety-driven limitation -- where fear or rigid thinking prevents the body from accessing the movement, treatment, or change it actually needs.",
    "imagery": "Eight of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-swords",
    "name": "Nine of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "09",
    "upright": "Nine of Swords is the card of 3am -- the mind running at full speed through worst-case scenarios in the dark. The suffering is real even though much of it is generated internally. The card does not dismiss the pain; it asks what part of it is actually happening now.",
    "reversed": "Reversed, Nine of Swords points to the slow easing of anxiety, the beginning of perspective after the dark night, or despair that has gone underground and become harder to track or speak about.",
    "love": "In love, Nine of Swords reflects anxiety about a relationship -- whether real problems are magnified by fear, or legitimate concern is driving a spiral of worst-case thinking that prevents clear action.",
    "career": "In career, Nine of Swords marks professional anxiety -- impostor syndrome, fear of exposure, or obsessive mental review of situations that require action rather than further analysis.",
    "health": "For wellbeing, Nine of Swords is a clear signal about mental health -- anxiety, insomnia, or the body's stress response running in the absence of the emergency it was designed for. Rest and professional support are both indicated.",
    "imagery": "Nine of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-swords",
    "name": "Ten of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "10",
    "upright": "Ten of Swords marks absolute ending -- rock bottom, the defeat so complete that there is nothing left to lose. And that is precisely its strange gift: nothing more needs to fall away. The only direction from here is up.",
    "reversed": "Reversed, Ten of Swords points to avoiding an inevitable ending, clinging to what has already been lost, or -- more hopefully -- the beginning of recovery after the worst has already happened.",
    "love": "In love, Ten of Swords marks the painful finality of a relationship ending -- the point where continuing is no longer possible and what remains is only the grief and what comes after.",
    "career": "In career, Ten of Swords marks a complete professional collapse -- a termination, business failure, or reputation event that makes continuing in the current form untenable.",
    "health": "For wellbeing, Ten of Swords reflects a health crisis -- a diagnosis that changes the landscape, a breakdown that forces genuine rest and recalibration, or the point where the body makes the patterns that brought it here impossible to continue.",
    "imagery": "Ten of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-swords",
    "name": "Page of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "page",
    "upright": "Page of Swords is all eyes and ears -- watchful, curious, and quicker to observe than to act. The curiosity is genuine and the blade is real, even if the figure doesn't yet know when to put it down. Ideas arrive faster than judgment does.",
    "reversed": "Reversed, Page of Swords points to sharpness that cuts indiscriminately, gossip delivered with precision, or intellectual curiosity that has turned into tactless truth-telling.",
    "love": "In love, Page of Swords brings careful observation before commitment -- wanting to understand the dynamic fully before emotionally investing, sometimes at the cost of genuine warmth.",
    "career": "In career, Page of Swords signals a sharp, analytically gifted early-career energy -- someone who sees problems quickly, communicates precisely, and is still learning when not to say everything they notice.",
    "health": "For wellbeing, Page of Swords reflects the analytical mind applying itself to health -- researching, monitoring, tracking -- sometimes with useful precision and sometimes with anxiety masquerading as information-gathering.",
    "imagery": "Page of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-swords",
    "name": "Knight of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "knight",
    "upright": "Knight of Swords charges forward without pausing to survey the terrain. The speed is real, the resolve is absolute, and the direction may or may not have been fully considered. The momentum itself becomes the decision.",
    "reversed": "Reversed, Knight of Swords points to rash action creating collateral damage, speed without discernment, or a communication delivered with such force that it left no room for the response it provoked.",
    "love": "In love, Knight of Swords brings directness and intensity -- someone who pursues without ambiguity or who says exactly what they think in a way that is clarifying but occasionally devastating.",
    "career": "In career, Knight of Swords marks fast-moving professional action -- pitching before being ready, pushing past resistance, or cutting through process in ways that get results but leave relationships damaged.",
    "health": "For wellbeing, Knight of Swords reflects the physical consequences of speed -- burnout from driving too hard, injury from pushing through pain signals, or the nervous system cost of chronic high-gear operation.",
    "imagery": "Knight of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-swords",
    "name": "Queen of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "queen",
    "upright": "Queen of Swords has earned her clarity through experience, including painful experience. She sees the situation without softening it for her own comfort or yours. Her independence and directness come from having depended on others and found it insufficient.",
    "reversed": "Reversed, Queen of Swords points to cold clarity turning into cruelty, independence hardening into bitterness, or sharp perception applied to wound rather than illuminate.",
    "love": "In love, Queen of Swords brings honesty, independence, and direct emotional presence that is deeply respectful and occasionally bracing -- she does not perform warmth she does not feel.",
    "career": "In career, Queen of Swords marks clear-headed professional authority -- someone who assesses without sentiment, communicates without flinching, and makes the call others avoid because they are not willing to be disliked for it.",
    "health": "For wellbeing, Queen of Swords reflects the clear-eyed approach to health -- understanding what is actually happening in the body, getting real information, and making decisions from fact rather than fear.",
    "imagery": "Queen of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-swords",
    "name": "King of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "king",
    "upright": "King of Swords governs through reason, precedent, and the precision of well-considered judgment. His authority is intellectual -- he has thought through the principles and applies them consistently, even when it costs him something.",
    "reversed": "Reversed, King of Swords points to intellect weaponised, judgment deployed for control rather than justice, or authority that has become tyrannical through rigid application of rule without compassion.",
    "love": "In love, King of Swords brings mental clarity and honest communication -- a partner who will not pretend and whose intellectual engagement is a form of deep respect, even when it removes the comfort of ambiguity.",
    "career": "In career, King of Swords marks senior intellectual authority -- the judge, the strategist, the architect of systems -- whose professional reputation rests on the quality and consistency of their reasoning.",
    "health": "For wellbeing, King of Swords reflects the disciplined mind's approach to health -- understanding the mechanisms, applying the appropriate interventions precisely, and maintaining the routine with the consistency of law.",
    "imagery": "King of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises leadership, direction, and mature command."
  },
  {
    "slug": "ace-of-pentacles",
    "name": "Ace of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "ace",
    "upright": "Ace of Pentacles brings the solid weight of a new material beginning -- a financial opportunity, a practical foundation, a seed in the real world rather than the imagination. The coin is offered and it is genuine.",
    "reversed": "Reversed, Ace of Pentacles points to a financial opportunity missed or mismanaged, a material start without the foundation to support it, or the offer present but the conditions not yet right to receive it fully.",
    "love": "In love, Ace of Pentacles marks a relationship taking root in the real world -- moving from possibility to tangible commitment, shared space, or practical partnership.",
    "career": "In career, Ace of Pentacles signals the beginning of a genuinely viable opportunity -- a job offer, client, grant, or contract -- where real resources are now available to support a direction.",
    "health": "For wellbeing, Ace of Pentacles reflects a practical new health beginning -- a diet, movement practice, or therapeutic relationship that has the material conditions to actually work.",
    "imagery": "Ace of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-pentacles",
    "name": "Two of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "02",
    "upright": "Two of Pentacles shows someone managing competing demands with remarkable ease -- the juggling looks effortless because the rhythm has been found. The key is adaptability; this figure succeeds by staying light on their feet rather than forcing stability.",
    "reversed": "Reversed, Two of Pentacles points to the juggling becoming too much -- one too many priorities, the rhythm lost, or the effort to appear in control no longer masking the genuine strain underneath.",
    "love": "In love, Two of Pentacles reflects the challenge of balancing a relationship against other life priorities -- a partnership that can thrive if both people can manage their mutual demands without one becoming invisible.",
    "career": "In career, Two of Pentacles marks skilled multitasking -- managing multiple projects or income streams with the flexibility to shift priority quickly as conditions change.",
    "health": "For wellbeing, Two of Pentacles reflects the challenge of maintaining health habits when life is genuinely full -- where juggling responsibilities sometimes comes at the body's expense.",
    "imagery": "Two of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-pentacles",
    "name": "Three of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "03",
    "upright": "Three of Pentacles shows skilled collaboration -- the mason, the architect, and the patron all working together, each contributing what only they can. The quality of the outcome depends on all three staying genuinely engaged.",
    "reversed": "Reversed, Three of Pentacles points to a collaborative failure -- poor communication between people who all think they're in charge, work done in silos, or craftsmanship undermined by a dysfunctional group dynamic.",
    "love": "In love, Three of Pentacles reflects a relationship built on more than attraction -- where two people actively work together on something shared, and the collaboration itself deepens the bond.",
    "career": "In career, Three of Pentacles marks the recognition and development of genuine skill -- where talent is developed through instruction, practice, and meaningful work within a structure that values craft.",
    "health": "For wellbeing, Three of Pentacles reflects the health benefit of working with professionals -- where the body improves through the right combination of specialist guidance, consistent practice, and real commitment.",
    "imagery": "Three of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-pentacles",
    "name": "Four of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "04",
    "upright": "Four of Pentacles shows someone holding tightly to what they have -- arms wrapped around their coin, feet planted on two more. The security is real but the posture prevents movement. What is being protected may be worth less than what is being missed.",
    "reversed": "Reversed, Four of Pentacles signals a release of grip -- money moving more freely, generosity returning, or the letting go of control that was preventing connection.",
    "love": "In love, Four of Pentacles reflects emotional withholding -- someone protecting themselves so thoroughly that genuine intimacy has become impossible, the very act of self-preservation preventing connection.",
    "career": "In career, Four of Pentacles marks a conservative, risk-averse professional stance -- valuable for protecting hard-won gains, potentially limiting when the moment calls for investment and movement.",
    "health": "For wellbeing, Four of Pentacles reflects the body as fortress -- over-controlled, resistant to anything that might disrupt the current equilibrium, even when that equilibrium is itself a form of stagnation.",
    "imagery": "Four of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-pentacles",
    "name": "Five of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "05",
    "upright": "Five of Pentacles shows two figures in the cold outside a lit window -- material hardship, genuine scarcity, and the particular pain of feeling excluded from what others take for granted. What is often missed: the door is not locked.",
    "reversed": "Reversed, Five of Pentacles signals a return to financial stability, the acceptance of help previously refused, or the beginning of recovery from a period of genuine material hardship.",
    "love": "In love, Five of Pentacles reflects the strain that scarcity puts on a relationship -- financial stress, feeling unsupported, or the difficulty of maintaining emotional warmth when survival anxiety dominates.",
    "career": "In career, Five of Pentacles marks genuine financial or professional hardship -- job loss, business failure, or the experience of being shut out of opportunities available to others.",
    "health": "For wellbeing, Five of Pentacles reflects the health impact of poverty, material stress, or the inability to access the care and resources that wellbeing actually requires.",
    "imagery": "Five of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-pentacles",
    "name": "Six of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "06",
    "upright": "Six of Pentacles shows the merchant weighing out gifts to those below while holding the scale. The generosity is real and the power differential is visible. What is being given is genuinely needed; who holds the scale matters.",
    "reversed": "Reversed, Six of Pentacles points to charity given with strings attached, resources flowing to those who don't need them, or an imbalance where one party is consistently depleted.",
    "love": "In love, Six of Pentacles reflects the generosity that sustains a healthy relationship -- or the imbalance where one person consistently gives and the other receives without reciprocity.",
    "career": "In career, Six of Pentacles marks the exchange of resources or skills in a way that genuinely benefits both parties -- fair compensation, mentorship, or professional generosity with real mutual return.",
    "health": "For wellbeing, Six of Pentacles reflects the health benefits of balanced exchange -- where giving and receiving care are in proportion and the body is not consistently depleted in service of others.",
    "imagery": "Six of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-pentacles",
    "name": "Seven of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "07",
    "upright": "Seven of Pentacles shows a farmer leaning on his hoe, looking at his crop. The work has been done; now comes patient waiting while the outcome matures. The card confirms the investment was real; it asks for the discipline not to pull up the roots to check them.",
    "reversed": "Reversed, Seven of Pentacles points to impatience undermining a long-term investment, poor returns on genuine effort, or the question of whether the direction of investment was correctly chosen.",
    "love": "In love, Seven of Pentacles reflects patient tending -- a relationship whose best qualities are still developing, where the commitment to cultivate rather than abandon determines the outcome.",
    "career": "In career, Seven of Pentacles marks the long-game professional -- someone who has invested significantly in a direction and is now in the difficult middle period, waiting for the return that patient effort earns.",
    "health": "For wellbeing, Seven of Pentacles reflects the discipline of a sustained health practice -- where the results are not yet dramatic but the consistent effort is compounding into something real.",
    "imagery": "Seven of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-pentacles",
    "name": "Eight of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "08",
    "upright": "Eight of Pentacles shows the apprentice fully absorbed in the work -- not looking up, not concerned with status, only with the quality of what is being made. Mastery is approached through repetition, attention, and the willingness to make the same thing better than before.",
    "reversed": "Reversed, Eight of Pentacles points to workmanship that has become mechanical, perfectionism preventing completion, or diligent effort invested in the wrong direction.",
    "love": "In love, Eight of Pentacles reflects the patient, unglamorous work of sustaining a relationship -- showing up consistently, communicating carefully, and getting better at the practice of loving this specific person.",
    "career": "In career, Eight of Pentacles marks the development of genuine professional skill through focused, repetitive practice -- the willingness to do the unglamorous work that produces expertise over time.",
    "health": "For wellbeing, Eight of Pentacles reflects the health benefits of consistent, focused practice -- where diligence applied to movement, nutrition, or therapeutic work produces measurable improvement.",
    "imagery": "Eight of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-pentacles",
    "name": "Nine of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "09",
    "upright": "Nine of Pentacles shows a woman alone in her garden, entirely at ease in her own world -- elegant, self-sufficient, and at peace with her independence. What she has was earned and it shows.",
    "reversed": "Reversed, Nine of Pentacles points to self-sufficiency that has become isolation, financial security purchased at the cost of genuine connection, or independence that began as strength and hardened into loneliness.",
    "love": "In love, Nine of Pentacles reflects a person who is genuinely complete without a partner -- bringing that self-sufficiency to a relationship as confidence rather than need, or finding independence more comfortable than compromise.",
    "career": "In career, Nine of Pentacles marks earned financial independence -- the freelancer with a full client roster, the professional whose reputation generates its own momentum.",
    "health": "For wellbeing, Nine of Pentacles reflects the body at its best expression of earned health -- where sustained investment in movement, nutrition, and self-care has produced a visible, felt quality of physical life.",
    "imagery": "Nine of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-pentacles",
    "name": "Ten of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "10",
    "upright": "Ten of Pentacles shows abundance extended across generations -- wealth that has become legacy, family that has become institution, security that outlasts any single person's life. The figure surveys what has been built and found it good.",
    "reversed": "Reversed, Ten of Pentacles points to a family system whose external wealth masks genuine dysfunction, or to wealth structured in a way that constrains rather than enables those who inherit it.",
    "love": "In love, Ten of Pentacles marks the relational equivalent of legacy -- a partnership that has built something together that could outlast them both: a home, a family, a shared life that has become something real.",
    "career": "In career, Ten of Pentacles marks the full fruition of a professional life -- the business handed to a successor, the career that produced lasting work, the institution built for the next generation.",
    "health": "For wellbeing, Ten of Pentacles reflects generational patterns of health -- where what the body carries has been inherited, and the habit of caring for oneself is something modelled and passed forward.",
    "imagery": "Ten of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-pentacles",
    "name": "Page of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "page",
    "upright": "Page of Pentacles holds his coin with great attention -- studying it, considering it, imagining what it can become. The enthusiasm is practical: he is in learning mode, building the foundation of future mastery with genuine application.",
    "reversed": "Reversed, Page of Pentacles points to study that stays theory, practical opportunity not fully engaged, or a student so absorbed in planning that they never begin the actual work.",
    "love": "In love, Page of Pentacles brings practical, grounded care -- the partner who remembers details, who shows up reliably, who builds something concrete rather than only expressing feeling.",
    "career": "In career, Page of Pentacles signals the beginning of serious professional development -- the student or intern who is genuinely interested in the material and willing to do the foundational work.",
    "health": "For wellbeing, Page of Pentacles reflects beginning a new health practice with genuine curiosity -- researching, investing in the right resources, and starting the slow process of building something sustainable.",
    "imagery": "Page of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-pentacles",
    "name": "Knight of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "knight",
    "upright": "Knight of Pentacles moves slowly, deliberately, and without shortcuts. He will complete the task -- not spectacularly, but completely, and correctly. The reliability is total; the excitement is not the point.",
    "reversed": "Reversed, Knight of Pentacles points to routine become stagnation, methodical effort that has lost its purpose, or the refusal to adapt when the situation has changed and the old method no longer serves.",
    "love": "In love, Knight of Pentacles brings steadfast presence -- showing up, keeping promises, building trust through consistency rather than grand gestures, providing the kind of safety that comes from being genuinely reliable.",
    "career": "In career, Knight of Pentacles marks the professional known for thorough work and reliable delivery -- not the flashiest performer, but the one the organisation depends on to get the unglamorous work done correctly.",
    "health": "For wellbeing, Knight of Pentacles reflects the health approach most likely to produce lasting results -- consistent, methodical, undramatic -- where the commitment to the routine outlasts the motivation that started it.",
    "imagery": "Knight of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-pentacles",
    "name": "Queen of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "queen",
    "upright": "Queen of Pentacles has made her home an abundance -- warm, practical, and nourishing to everything that enters it. Her prosperity is not hoarded but shared, and her care extends naturally to anyone who crosses her threshold.",
    "reversed": "Reversed, Queen of Pentacles points to maternal warmth that has become smothering, practical care tipping into control, or a person so busy maintaining the material world that their own deeper needs go completely unmet.",
    "love": "In love, Queen of Pentacles brings practical, embodied warmth -- a partner who shows love through feeding, tending, and creating comfort, whose care is expressed more through action than declaration.",
    "career": "In career, Queen of Pentacles marks the professional who has integrated material success and personal warmth -- where financial acumen is matched by real care for the people involved.",
    "health": "For wellbeing, Queen of Pentacles reflects a grounded, body-positive approach to health -- where the earth, food, movement, and sensory experience are treated as medicine rather than pleasure to be rationed.",
    "imagery": "Queen of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-pentacles",
    "name": "King of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "king",
    "upright": "King of Pentacles has built something real -- wealth from sustained, intelligent effort over many years. He is surrounded by his achievements and comfortable in that abundance: not flashy, not anxious, simply established in what he has made.",
    "reversed": "Reversed, King of Pentacles points to wealth used for domination, a business-first orientation that has squeezed the life out of relationships, or financial security that has become the measure of worth rather than the support for a richer life.",
    "love": "In love, King of Pentacles brings security and stability -- a partner whose reliability is genuinely stabilising, providing the material conditions in which a relationship can grow without existential anxiety.",
    "career": "In career, King of Pentacles marks the full expression of financial and professional mastery -- the CEO, the investor, the builder of institutions whose authority comes from a track record that speaks for itself.",
    "health": "For wellbeing, King of Pentacles reflects financial and practical stability as a direct health resource -- where having enough means the body can be properly cared for, adequately rested, and treated as an asset rather than merely a tool.",
    "imagery": "King of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises leadership, direction, and mature command."
  }
]""")

CARDS = _build_cards()
CARD_INDEX = {item["slug"]: item for item in CARDS}

def list_card_summaries() -> list[dict[str, Any]]:
    return [{"slug": card["slug"], "name": card["name"], "arcana": card["arcana"], "suit": card["suit"]} for card in CARDS]

def get_card(slug: str) -> dict[str, Any] | None:
    card = CARD_INDEX.get(slug)
    if not card:
        return None
    if card["arcana"] == "major":
        recommended = SPREADS[:3]
    else:
        suit_label = card["suit"].lower()
        recommended = [spread for spread in SPREADS if suit_label in spread["chapter"].lower() or suit_label in spread["title"].lower()][:3] or SPREADS[:3]
    faq = [{"question": f"What does {card['name']} mean upright?", "answer": card["upright"]}, {"question": f"What does {card['name']} mean reversed?", "answer": card["reversed"]}, {"question": f"Is {card['name']} a yes-or-no card?", "answer": f"{card['name']} is best read in context. The surrounding cards, question, and orientation matter more than a fixed yes-or-no label."}, {"question": f"Where is {card['name']} strongest in tarot spreads?", "answer": "It becomes especially vivid in spreads that ask for motive, turning points, emotional truth, or long-term consequence."}]
    return {**card, "best_spreads": [{"slug": spread["slug"], "title": spread["title"]} for spread in recommended], "faq": faq, "meta_title": f"{card['name']} Tarot Card - Meaning, Reversed and How to Read It", "meta_description": f"Learn {card['name']} tarot meanings upright and reversed, plus love, career, health, and symbolic interpretations."}

def list_intention_summaries() -> list[dict[str, Any]]:
    return [{"slug": slug, "label": payload["label"], "chapter": payload["chapter"]} for slug, payload in INTENTIONS.items()]

def get_intention(slug: str) -> dict[str, Any] | None:
    payload = INTENTIONS.get(slug)
    if not payload:
        return None
    spreads = [get_spread(SPREAD_INDEX_BY_NUMBER[number]) for number in payload["spread_numbers"] if number in SPREAD_INDEX_BY_NUMBER]
    best_cards = [get_card(card_slug) for card_slug in payload["best_cards"] if get_card(card_slug)]
    caution_cards = [get_card(card_slug) for card_slug in payload["caution_cards"] if get_card(card_slug)]
    walkthrough = {"spread_title": spreads[0]["title"], "steps": spreads[0]["sample_reading"][: min(3, len(spreads[0]["sample_reading"]))]} if spreads else None
    faq = [{"question": f"Which tarot spread is best for {payload['label'].lower()}?", "answer": f"This page compares three strong layouts for {payload['label'].lower()} so you can choose based on depth, timing, and emotional intensity."}, {"question": f"Can tarot help with {payload['label'].lower()}?", "answer": INTRO_SNIPPETS.get(slug, "Tarot helps by revealing patterns, motives, and the next honest step.")}, {"question": f"What cards are favourable for {payload['label'].lower()} readings?", "answer": (", ".join(card['name'] for card in best_cards[:5]) + ".") if best_cards else "Supportive cards usually show openness, clarity, and movement."}, {"question": f"What cards signal caution in {payload['label'].lower()} spreads?", "answer": (", ".join(card['name'] for card in caution_cards[:4]) + ".") if caution_cards else "Caution cards usually highlight fear, delay, conflict, or self-deception."}, {"question": f"Should I still use the interactive tarot tool for {payload['label'].lower()}?", "answer": "Yes. These SEO pages explain layouts and symbolism, while the live tarot tool is where you can actually draw and reflect on the cards."}]
    return {"slug": slug, "label": payload["label"], "intro": INTRO_SNIPPETS.get(slug, "Tarot helps by revealing patterns, motives, and the next honest step."), "top_spreads": [spread for spread in spreads if spread], "best_cards": [{"slug": card['slug'], "name": card['name'], "meaning": card['upright']} for card in best_cards], "caution_cards": [{"slug": card['slug'], "name": card['name'], "meaning": card['reversed']} for card in caution_cards], "sample_walkthrough": walkthrough, "faq": faq, "meta_title": f"Best Tarot Spreads for {payload['label']} - Top Layouts Explained", "meta_description": f"Explore the best tarot spreads for {payload['label'].lower()}, plus supportive cards, caution cards, and a sample reading walkthrough."}

def get_hub() -> dict[str, Any]:
    return {"title": "Tarot Spreads Hub", "description": "Browse source-backed tarot spread pages, all 78 card meanings, and intention guides for love, career, money, healing, and more.", "featured_spreads": list_spread_summaries()[:12], "spreads": list_spread_summaries(), "cards": list_card_summaries(), "intentions": list_intention_summaries(), "meta_title": "Tarot Spreads Hub - Card Meanings, Layouts and Intention Guides", "meta_description": "Explore tarot spreads by layout, all 78 tarot card meanings, and guided tarot pages for love, career, money, health, and more."}

def get_tarot_sitemap_urls() -> list[str]:
    urls = [f"{SITE_URL}/tarot/spreads"]
    urls.extend(f"{SITE_URL}/tarot/spread/{item['slug']}" for item in SPREADS)
    urls.extend(f"{SITE_URL}/tarot/card/{item['slug']}" for item in CARDS)
    urls.extend(f"{SITE_URL}/tarot/for/{slug}" for slug in INTENTIONS)
    return urls

# ── TAR-M4 COMBINATION MATRIX: 60 PRIORITY SPREADS (GAI D5d) ────────────────
# Source: GAI ECHO//PACE V2 response, filtered from 100 spreads for:
#   - Search volume potential
#   - Intent diversity (prevents cross-page semantic cannibalization)
#   - Unique card×spread intersection value
# Use: 78 cards × 60 spreads = 4,680 combination pages (TAR-M4)

PRIORITIZED_SPREAD_SLUGS: list[str] = [
    "daily-tarot-reading-insight",
    "past-present-future-timeline-reading",
    "horseshoe-layout-for-complex-decisions",
    "single-question-tarot-answer",
    "manifesting-true-love-and-soulmate-tarot",
    "resolving-relationship-conflicts-tarot",
    "choosing-between-two-paths-tarot",
    "interview-success-and-career-hiring-tarot",
    "manifesting-urgent-financial-abundance",
    "mid-term-future-vision-tarot-layout",
    "calming-anxiety-and-overthinking-tarot",
    "physical-healing-and-recovery-forecast",
    "entrepreneurship-launch-roadmap-tarot",
    "career-promotion-vs-work-life-balance-tarot",
    "breaking-generational-financial-scarcity",
    "turning-temporary-gigs-into-full-time-jobs",
    "twin-flame-recognition-signs-tarot",
    "dealing-with-emotional-immaturity-in-love",
    "resolving-friend-group-drama-advice",
    "achieving-big-goals-and-dreams-reading",
    "full-time-job-vs-side-hustle-tarot",
    "managing-difficult-bosses-and-coworkers",
    "legal-victory-and-litigation-outcome",
    "settlement-vs-going-to-trial-analysis",
    "setting-strong-boundaries-with-money",
    "relocating-abroad-for-high-salary-job",
    "brick-and-mortar-vs-e-commerce-scaling",
    "overcoming-fear-and-mental-blocks-tarot",
    "navigating-workplace-cliques-and-bullying",
    "school-bullying-intervention-and-support",
    "cyberbullying-defense-advice-for-teens",
    "navigating-big-career-and-life-crossroads",
    "overcoming-stagnation-and-feeling-stuck",
    "breaking-hurdles-to-achieve-success",
    "buying-a-house-vs-vacation-planning-tarot",
    "blended-family-dynamics-and-first-meetings",
    "handling-toxic-relatives-at-family-events",
    "overcoming-isolation-after-moving",
    "short-term-future-forecast-tarot",
    "birthday-solar-return-planetary-map",
    "past-life-love-and-soul-connection",
    "fertility-and-conception-guidance-tarot",
    "preparing-for-parenthood-relationship-check",
    "assessing-co-parenting-compatibility-tarot",
    "evaluating-casual-sex-vs-emotional-bond",
    "deciphering-mixed-intimacy-signals-in-love",
    "funding-solo-travel-using-inheritance",
    "real-estate-sale-success-timeline",
    "vastu-blessings-for-your-new-home",
    "relocation-analysis-for-new-communities",
    "holiday-travel-destination-picker-tarot",
    "hotel-vs-resort-accommodation-decision",
    "grief-counseling-for-sudden-accidental-death",
    "coping-with-unresolved-suspicious-loss",
    "new-moon-rituals-for-fresh-beginnings",
    "manifesting-fast-secondary-income",
    "healing-trauma-loss-and-betrayal-guide",
    "12-month-wheel-of-year-forecast",
    "5-year-life-path-long-term-layout",
    "athletic-performance-and-fitness-tarot",
]  # 78 × 60 = 4,680 TAR-M4 combination pages

# Intent category per priority spread -- used by TAR-M4 generator to select
# the correct card field (love/career/health/upright) for each combination page
SPREAD_INTENT_CATEGORY: dict[str, str] = {
    "daily-tarot-reading-insight":                 "general",
    "past-present-future-timeline-reading":         "general",
    "horseshoe-layout-for-complex-decisions":       "general",
    "single-question-tarot-answer":                 "general",
    "manifesting-true-love-and-soulmate-tarot":     "love",
    "resolving-relationship-conflicts-tarot":       "love",
    "choosing-between-two-paths-tarot":             "general",
    "interview-success-and-career-hiring-tarot":    "career",
    "manifesting-urgent-financial-abundance":       "career",
    "mid-term-future-vision-tarot-layout":          "general",
    "calming-anxiety-and-overthinking-tarot":       "health",
    "physical-healing-and-recovery-forecast":       "health",
    "entrepreneurship-launch-roadmap-tarot":        "career",
    "career-promotion-vs-work-life-balance-tarot":  "career",
    "breaking-generational-financial-scarcity":     "career",
    "turning-temporary-gigs-into-full-time-jobs":   "career",
    "twin-flame-recognition-signs-tarot":           "love",
    "dealing-with-emotional-immaturity-in-love":    "love",
    "resolving-friend-group-drama-advice":          "general",
    "achieving-big-goals-and-dreams-reading":       "general",
    "full-time-job-vs-side-hustle-tarot":           "career",
    "managing-difficult-bosses-and-coworkers":      "career",
    "legal-victory-and-litigation-outcome":         "general",
    "settlement-vs-going-to-trial-analysis":        "general",
    "setting-strong-boundaries-with-money":         "career",
    "relocating-abroad-for-high-salary-job":        "career",
    "brick-and-mortar-vs-e-commerce-scaling":       "career",
    "overcoming-fear-and-mental-blocks-tarot":      "health",
    "navigating-workplace-cliques-and-bullying":    "career",
    "school-bullying-intervention-and-support":     "general",
    "cyberbullying-defense-advice-for-teens":       "general",
    "navigating-big-career-and-life-crossroads":    "career",
    "overcoming-stagnation-and-feeling-stuck":      "general",
    "breaking-hurdles-to-achieve-success":          "general",
    "buying-a-house-vs-vacation-planning-tarot":    "general",
    "blended-family-dynamics-and-first-meetings":   "general",
    "handling-toxic-relatives-at-family-events":    "general",
    "overcoming-isolation-after-moving":            "general",
    "short-term-future-forecast-tarot":             "general",
    "birthday-solar-return-planetary-map":          "general",
    "past-life-love-and-soul-connection":           "love",
    "fertility-and-conception-guidance-tarot":      "health",
    "preparing-for-parenthood-relationship-check":  "love",
    "assessing-co-parenting-compatibility-tarot":   "love",
    "evaluating-casual-sex-vs-emotional-bond":      "love",
    "deciphering-mixed-intimacy-signals-in-love":   "love",
    "funding-solo-travel-using-inheritance":        "general",
    "real-estate-sale-success-timeline":            "general",
    "vastu-blessings-for-your-new-home":            "general",
    "relocation-analysis-for-new-communities":      "general",
    "holiday-travel-destination-picker-tarot":      "general",
    "hotel-vs-resort-accommodation-decision":       "general",
    "grief-counseling-for-sudden-accidental-death": "health",
    "coping-with-unresolved-suspicious-loss":       "health",
    "new-moon-rituals-for-fresh-beginnings":        "general",
    "manifesting-fast-secondary-income":            "career",
    "healing-trauma-loss-and-betrayal-guide":       "health",
    "12-month-wheel-of-year-forecast":              "general",
    "5-year-life-path-long-term-layout":            "general",
    "athletic-performance-and-fitness-tarot":       "health",
}
