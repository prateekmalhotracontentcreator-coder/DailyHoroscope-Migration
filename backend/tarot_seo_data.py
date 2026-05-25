from __future__ import annotations

import json
from typing import Any

SITE_URL = "https://www.everydayhoroscope.in"

SPREADS_JSON = r"""[
  {
    "number": 1,
    "slug": "card-of-the-day",
    "title": "Card Of The Day",
    "chapter": "One-Card Spreads",
    "purpose": "You can use this Spread every day to alert you to what you need to know about the day ahead. If the answer is not clear, or if it is a particularly significant day, add a second card.",
    "positions": [],
    "use": "A full deck of seventy-eight cards. Choose one card at random from anywhere in the facedown deck.",
    "when": "Every morning, soon after you have woken up. If you are still somewhat sleepy, you will be relaxed enough to interpret the chosen card with your intuition, rather than trying to make sense of the card with your logical mind."
  },
  {
    "number": 2,
    "slug": "one-question",
    "title": "One Question",
    "chapter": "One-Card Spreads",
    "purpose": "Any single uncomplicated question that requires a straightforward",
    "positions": [],
    "use": "A single card from the full deck of seventy-eight cards. Choose one card taken at random from anywhere in the facedown deck. If the answer is not clear, add a second card.",
    "when": "Whenever a quick answer is needed to an uncomplicated question."
  },
  {
    "number": 13,
    "slug": "should-you-continue-saving-for-a-house-or-take-a-break-and",
    "title": "Should You Continue Saving For A House, Or Take A Break And Have A Longed-For Vacation Overseas?",
    "chapter": "Two-Card Spreads",
    "purpose": "If you are saving hard for your first home or to upsize, but feel you just aren\u2019t having any fun anymore.",
    "positions": [],
    "use": "The full deck. Choose, before turning the cards over, one card for each option and read left to right.",
    "when": "Everyone is going on vacation and you feel left out."
  },
  {
    "number": 14,
    "slug": "should-you-go-for-a-major-promotion-or-focus-on-happiness-in-your-out-of-work-life",
    "title": "Should You Go For A Major Promotion, Or Focus On Happiness In Your Out-Of-Work Life?",
    "chapter": "Two-Card Spreads",
    "purpose": "If you are offered a promotion or extra training that will involve long hours and working weekends, but it promises great prospects for the future.",
    "positions": [],
    "use": "The full deck.",
    "when": "Before you apply for a promotion or go for an interview for that higher position you have been offered."
  },
  {
    "number": 25,
    "slug": "a-three-card-unstructured-reading-to-answer-any-question-on-any-topic",
    "title": "A Three-Card Unstructured Reading To Answer Any Question On Any Topic",
    "chapter": "Three-Card Spreads",
    "purpose": "This Spread can answer any question.",
    "positions": [
      "Card 2 to act as the"
    ],
    "use": "A full deck of 78 cards.",
    "when": "Any time you will not be disturbed, so you can allow the ideas to form."
  },
  {
    "number": 26,
    "slug": "past-present-and-future",
    "title": "Past, Present, And Future",
    "chapter": "Three-Card Spreads",
    "purpose": "Useful if you are planning changes based on what has previously happened in your life.",
    "positions": [
      "Card 1: What you need to leave behind to make the change or what is already moving out of your life.",
      "Card 2: The present influences and factors already emerging affecting your decision.",
      "Card 3: The results of taking action and what lies over the horizon if you do."
    ],
    "use": "The full seventy-eight-card deck.",
    "when": "Once you have all the facts and figures, but still hesitate."
  },
  {
    "number": 27,
    "slug": "what-lies-ahead-an-overview-of-the-next-three-days-weeks-or-months",
    "title": "What Lies Ahead An Overview Of The Next Three Days, Weeks, Or Months",
    "chapter": "Three-Card Spreads",
    "purpose": "If the next three days, weeks, or months are of significance, but there are unknown factors.",
    "positions": [
      "Card 1: Will represent factors or people who will be helpful.",
      "Card 2: Will signify factors or people who may stand in your way. And the all-important",
      "Card 3 represents what"
    ],
    "use": "The forty Number cards, Ace to Ten, and the sixteen Court or Personality cards.",
    "when": "The day before the selected period begins."
  },
  {
    "number": 37,
    "slug": "an-unstructured-reading-of-four-cards",
    "title": "An Unstructured Reading Of Four Cards",
    "chapter": "Four-Card Spreads",
    "purpose": "For absolutely any question, to build up an answer without assigning specific meanings. You can extend any unstructured three-card reading (see",
    "positions": [],
    "use": "Any combination of the seventy-eight cards that fits with your question.",
    "when": "Whenever you need extra information about your three-card reading."
  },
  {
    "number": 38,
    "slug": "spread-for-breaking-through-the-barriers-of-fear",
    "title": "Spread For Breaking Through The Barriers Of Fear",
    "chapter": "Four-Card Spreads",
    "purpose": "When fears or phobias are restricting your lifestyle.",
    "positions": [
      "Card 1: What is the real cause of my fear?",
      "Card 2: Is this bad thing actually likely to happen, or is it just fear?",
      "Card 3: What triggers/makes the fear worse?",
      "Card 4: What action can I take to prevent or overcome my fear?"
    ],
    "use": "The full deck.",
    "when": "A Tuesday, the day of courage."
  },
  {
    "number": 47,
    "slug": "the-horseshoe-spread",
    "title": "The Horseshoe Spread",
    "chapter": "Five-Card Spreads",
    "purpose": "You can use this Spread for absolutely any question.",
    "positions": [
      "Card 1: Your choice, dilemma or predominant question.",
      "Card 2: Present influences, people, and circumstances that affect your present position.",
      "Card 3: Hidden influences, both the messages in our heads from the past and what is just beyond the horizon.",
      "Card 4: Suggested action, whether to change or preserve the status quo.",
      "Card 5: Likely outcome, of either acting or waiting according to",
      "Card 4 ."
    ],
    "use": "The full deck.",
    "when": "When there are several background factors in play."
  },
  {
    "number": 48,
    "slug": "dealing-with-cliques-and-petty-bullying",
    "title": "Dealing With Cliques And Petty Bullying",
    "chapter": "Five-Card Spreads",
    "purpose": "When you are suffering at work or socially from being excluded, and from sarcasm or put-downs.",
    "positions": [
      "Card 1: Who/what is excluding me most.",
      "Card 2: What the motive is.",
      "Card 3: Can or should I ignore it?",
      "Card 4: Should I complain/tackle it head on?",
      "Card 5: Should I cut my losses and leave?"
    ],
    "use": "The full deck.",
    "when": "A Wednesday, day of protection against human snakes."
  },
  {
    "number": 49,
    "slug": "the-five-year-plan",
    "title": "The Five-Year Plan",
    "chapter": "Five-Card Spreads",
    "purpose": "When you are making long-term plans for any aspect of your life.",
    "positions": [
      "Card 1: Where I am now.",
      "Card 2: Where I would like to be in five years\u2019 time.",
      "Card 3: What extra resources/training/practice do I need?",
      "Card 4: Any possible challenges to overcome?",
      "Card 5: To achieve this long-term goal, do I need to expand/move on now, or stay where I am?"
    ],
    "use": "The full deck.",
    "when": "At a time when you need to make decisions about your future, rather than letting life decide."
  },
  {
    "number": 56,
    "slug": "an-unstructured-six-card-spread-to-answer-any-question-on-any-topic",
    "title": "An Unstructured Six-Card Spread To Answer Any Question On Any Topic",
    "chapter": "Six-Card Spreads",
    "purpose": "An extremely versatile Spread suitable for answering questions on any topic.",
    "positions": [
      "Card 6 the answer falls into place. Almost always the person shown in each card represents you\u2014or, if not, then the person/people who affect the question."
    ],
    "use": "A full deck of seventy-eight cards.",
    "when": "Any time when you are unlikely to be disturbed."
  },
  {
    "number": 57,
    "slug": "the-next-six-weeks-months-spread",
    "title": "The Next Six Weeks/Months Spread",
    "chapter": "Six-Card Spreads",
    "purpose": "A predictive view of the six weeks or months directly ahead, so you can plan strategies, meet challenges, and avoid pitfalls.",
    "positions": [
      "Card 1: What do you hope to achieve in the next six weeks/months?",
      "Card 2: What specific opportunities are you seeking?",
      "Card 3: What challenges are you worried about?",
      "Card 4: What would you like to remain unchanged?",
      "Card 5: What/who would you like to change?",
      "Card 6: What do you seek in the longer term?"
    ],
    "use": "The full deck.",
    "when": "The evening before the chosen period."
  },
  {
    "number": 58,
    "slug": "will-i-ever-find-my-soul-mate",
    "title": "Will I Ever Find My Soul Mate?",
    "chapter": "Six-Card Spreads",
    "purpose": "If you despair of finding the right love.",
    "positions": [
      "Card 1: Should I give up looking and just wait for it to happen?",
      "Card 2: Should I try an online dating site/friendship group?",
      "Card 3: Should I join a face-to-face/singles group?",
      "Card 4: Should I join new activities?",
      "Card 5: Should I relocate/change my job?",
      "Card 6: Will I meet my Twin Soul, or settle for someone nice?"
    ],
    "use": "The whole deck.",
    "when": "A Friday, the day of love."
  },
  {
    "number": 64,
    "slug": "the-options-spread",
    "title": "The Options Spread",
    "chapter": "Seven-Card Spreads",
    "purpose": "When you have two main options and wish to discover which is the most advantageous choice (if there are more than two options).",
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
    "when": "Whenever you have time to study the options in depth."
  },
  {
    "number": 65,
    "slug": "the-mystical-seven-spread",
    "title": "The Mystical Seven Spread",
    "chapter": "Seven-Card Spreads",
    "purpose": "An unstructured Spread for spiritual or psychic questions, or wherever an outcome depends on information not yet accessible or which is being deliberately concealed.",
    "positions": [
      "Card 7, will reveal what is just over the horizon or being hidden and the answer to your dilemma."
    ],
    "use": "The twenty-two Major cards or the full deck.",
    "when": "A good full-moon night or any Monday evening, day of the moon."
  },
  {
    "number": 70,
    "slug": "moving-toward-fulfilling-your-greatest-ambition-or-dream",
    "title": "Moving Toward Fulfilling Your Greatest Ambition Or Dream",
    "chapter": "Eight-Card Spreads",
    "purpose": "When a chance, however small, opens a door toward a longed-for opportunity, but you know it will bring disruption.",
    "positions": [
      "Card 1: Is this the window of opportunity for which I have been waiting?",
      "Card 2: Is this step that I am contemplating realistic?",
      "Card 3: Am I ready\u2014and, if not, when will I be?",
      "Card 4: Who/what will help me?",
      "Card 5: Who/what will oppose me/disapprove?",
      "Card 6: Should I modify/compromise my dream to make the step less disruptive?",
      "Card 7: The short-term outcome of taking the step, the next six months.",
      "Card 8: The longer-term outcome, the next five years."
    ],
    "use": "The full deck.",
    "when": "A Tuesday for major change, sometimes involving disruption."
  },
  {
    "number": 71,
    "slug": "should-you-try-to-conceive-a-baby",
    "title": "Should You Try To Conceive A Baby?",
    "chapter": "Eight-Card Spreads",
    "purpose": "When the biological clock is ticking and you and your partner are deciding the pros and cons of having a baby, which you both realize is a major lifestyle change. This Spread can also be used for any question where there are significant pros and cons.",
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
    "when": "A Friday, the day of fertility and families."
  },
  {
    "number": 76,
    "slug": "an-unstructured-nine-card-reading",
    "title": "An Unstructured Nine-Card Reading",
    "chapter": "Nine-Card Spreads",
    "purpose": "The nine-card unstructured reading will answer absolutely any question as you build up a whole picture step by step. You can add a tenth card as the Crown of the reading if it hasn\u2019t all come together by",
    "positions": [
      "Card 9 ."
    ],
    "use": "The full deck.",
    "when": "Any leisurely evening. Afterward, scribble in your Tarot journal any extra ideas for each card before clearing the cards away."
  },
  {
    "number": 77,
    "slug": "the-pathway-to-justice",
    "title": "The Pathway To Justice",
    "chapter": "Nine-Card Spreads",
    "purpose": "For any official, legal, or compensation matter, especially where there has been unfairness, corruption, or lies blocking your path.",
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
    "when": "A Thursday, the day of justice and truth."
  },
  {
    "number": 82,
    "slug": "an-unstructured-twelve-card-spread",
    "title": "An Unstructured Twelve-Card Spread",
    "chapter": "Multi-Card Spreads",
    "purpose": "For absolutely any question where you need more detail, or where there are many different aspects.",
    "positions": [],
    "use": "The full deck.",
    "when": "You have time to contemplate each card and allow the answer to form."
  },
  {
    "number": 83,
    "slug": "a-wheel-of-the-year-twelve-months-ahead-spread",
    "title": "A Wheel Of The Year Twelve-Months-Ahead Spread",
    "chapter": "Multi-Card Spreads",
    "purpose": "If you want to know what the year ahead has in store.",
    "positions": [
      "Card 1 being the month following the reading. Record the opportunities or challenges each card suggests during a particular month. As a rule, Major Arcana cards indicate major events or where outside circumstances play a big part. Minor cards refer to more ordinary but nevertheless significant happenings occurring in the period you are measuring. Court cards indicate dominant personalities\u2014or a new love or pregnancy. Finally, choose a card to sum up the twelve months ahead and put this in the center of the circle. You can pick two cards for each month if you wish."
    ],
    "use": "One or two full decks.",
    "when": "During the current month. If the month is nearly over, begin on the following one."
  },
  {
    "number": 87,
    "slug": "have-i-found-my-soulmate-from-a-past-world",
    "title": "Have I Found My Soulmate From A Past World?",
    "chapter": "Love And Commitment Spreads",
    "purpose": "When you are with a partner/have met someone special.",
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
    "when": "A Friday, the day of love."
  },
  {
    "number": 88,
    "slug": "can-it-be-true-i-have-met-my-twin-soul-at-last",
    "title": "Can It Be True I Have Met My Twin Soul At Last?",
    "chapter": "Love And Commitment Spreads",
    "purpose": "When deep sudden love feels right.",
    "positions": [
      "Card 1: Do you feel you have known each other forever?",
      "Card 2: Was there instant recognition/connection at the first meeting?",
      "Card 3: Does s/he fit totally with your family/friends/interests?",
      "Card 4: Is the relationship fast-moving but quite natural-feeling?",
      "Card 5: Is a missing part of your life now complete?",
      "Card 6: Do you have constant d\u00e9j\u00e0 vu and telepathic links?"
    ],
    "use": "The full deck.",
    "when": "On the same day of the week and at the same time you met/reconnected."
  },
  {
    "number": 108,
    "slug": "the-love-quarrel",
    "title": "The Love Quarrel",
    "chapter": "Spreads For Overcoming Difficulties In Love, Reconciliation, And Ending Destructive Relationships",
    "purpose": "When neither of you will back down.",
    "positions": [
      "Card 2: What is the underlying issue for you?",
      "Card 3: What is the underlying issue for your partner?",
      "Card 5: Are there principles on which you cannot/will not back down?",
      "Card 6: Are there issues on which your partner cannot/will not back down?",
      "Card 8: Is anyone outside fueling the fire?",
      "Card 9: What is the best outcome?"
    ],
    "use": "The full deck.",
    "when": "A Friday, day of peace."
  },
  {
    "number": 109,
    "slug": "the-immature-partner",
    "title": "The Immature Partner",
    "chapter": "Spreads For Overcoming Difficulties In Love, Reconciliation, And Ending Destructive Relationships",
    "purpose": "When your partner\u2019s childish behavior is impacting on the relationship.",
    "positions": [
      "Card 1: How is this most adversely affecting the relationship?",
      "Card 2: Will s/he change, given time?",
      "Card 3: How can change come about?",
      "Card 4: If s/he doesn\u2019t grow up, should I stick with the relationship?",
      "Card 5: What can I do to make things better?",
      "Card 6: Who/what bad influences need to be removed from his/her life?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "The waning moon."
  },
  {
    "number": 129,
    "slug": "to-make-money-fast-and-urgently",
    "title": "To Make Money Fast And Urgently",
    "chapter": "Prosperity And Money-Making Spreads",
    "purpose": "Making an informed decision as to the best way forward.",
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
    "when": "A Wednesday, day for financial maneuverability."
  },
  {
    "number": 130,
    "slug": "if-you-are-offered-an-overseas-offshore-job-with-a-huge-tax-free-salary",
    "title": "If You Are Offered An Overseas/Offshore Job With A Huge Tax-Free Salary",
    "chapter": "Prosperity And Money-Making Spreads",
    "purpose": "When you would be set up for life financially, but other factors intrude.",
    "positions": [
      "Card 1: What benefits of taking the offer short-term might outweigh other considerations?",
      "Card 2: What longer-term advantages would occur if you stayed in the job indefinitely?",
      "Card 3: What emotional/lifestyle problems might arise, and can they be overcome?",
      "Card 4: What are the hidden drawbacks?",
      "Card 5: Yes or no, taking the other four cards into account."
    ],
    "use": "The twenty-two Major cards.",
    "when": "Any morning, as soon as you wake."
  },
  {
    "number": 149,
    "slug": "why-does-money-drain-out-no-matter-how-hard-you-try",
    "title": "Why Does Money Drain Out, No Matter How Hard You Try?",
    "chapter": "Spreads For Solving Difficulties With Money",
    "purpose": "",
    "positions": [],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "A Wednesday for money dilemmas."
  },
  {
    "number": 150,
    "slug": "why-do-people-take-advantage-of-you-financially",
    "title": "Why Do People Take Advantage Of You Financially?",
    "chapter": "Spreads For Solving Difficulties With Money",
    "purpose": "When you realize you are always paying and are made to feel guilty if you do not.",
    "positions": [
      "Card 1: What stops you from saying no?",
      "Card 2: Who takes advantage of you the most?",
      "Card 3: How will you cope with the resentment/pressure if you start saying no?",
      "Card 4: What do you gain by being overly generous?",
      "Card 5: Who will resist/protest/use emotional blackmail if you say no?",
      "Card 6: Are you with the wrong people?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "A Tuesday, the day of courage."
  },
  {
    "number": 169,
    "slug": "will-you-get-the-job-you-are-applying-for",
    "title": "Will You Get The Job You Are Applying For?",
    "chapter": "Career Spreads",
    "purpose": "When you aren\u2019t certain about your prospects.",
    "positions": [
      "Card 1: Are there more indications in your favor?",
      "Card 2: Are there more indications that you may not get this job?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "After submitting your application."
  },
  {
    "number": 170,
    "slug": "when-you-are-constantly-in-conflict-with-a-colleague-or-manager",
    "title": "When You Are Constantly In Conflict With A Colleague Or Manager",
    "chapter": "Career Spreads",
    "purpose": "If whatever you do is considered wrong, but you do not want to leave your job.",
    "positions": [
      "Card 1: The open cause of the conflict.",
      "Card 2: The hidden cause of the conflict.",
      "Card 3: The solution."
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "The beginning of the work week."
  },
  {
    "number": 171,
    "slug": "which-should-take-priority-right-now-your-day-job-or-your-on-the-side-business",
    "title": "Which Should Take Priority Right Now Your Day Job, Or Your On-The-Side Business?",
    "chapter": "Career Spreads",
    "purpose": "If you are finding it hard to balance the two.",
    "positions": [
      "Card 1 and",
      "Card 2 and neither seems definite, add a third card above and between"
    ],
    "use": "The twenty-two Major cards.",
    "when": "At a crisis point in your working world."
  },
  {
    "number": 191,
    "slug": "starting-your-own-business",
    "title": "Starting Your Own Business",
    "chapter": "Business Spreads",
    "purpose": "If you want to give your business idea a try after years of employment/looking after the home.",
    "positions": [
      "Card 1: Are you ready to launch your business?",
      "Card 2: Should you launch it 100%, or run it part-time until established?",
      "Card 3: Is there an existing market for your business, or do you need to create one?",
      "Card 4: Are the premises/equipment you have/will obtain adequate?",
      "Card 5: What expansion plans will be viable over the next twelve months?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "A Wednesday, day of enterprise."
  },
  {
    "number": 192,
    "slug": "should-you-trade-your-products-or-services-locally-or-online",
    "title": "Should You Trade Your Products Or Services Locally, Or Online?",
    "chapter": "Business Spreads",
    "purpose": "When you are not sure how to maximize sales.",
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
    "when": "A Thursday, for secure business ventures."
  },
  {
    "number": 211,
    "slug": "what-should-you-do-to-get-through-to-the-finals-of-a-major-talent-contest",
    "title": "What Should You Do To Get Through To The Finals Of A Major Talent Contest?",
    "chapter": "Spreads For Fame And Fortune",
    "purpose": "A two-carder when you need some no-frills guidance.",
    "positions": [
      "Card 1: What do you need to know to get into the final?",
      "Card 2: How can you best overcome the competition of other entrants?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "The night before the contest."
  },
  {
    "number": 212,
    "slug": "if-you-want-to-win-a-tv-talent-show",
    "title": "If You Want To Win A TV Talent Show",
    "chapter": "Spreads For Fame And Fortune",
    "purpose": "If people say you should enter a TV talent contest, but you lack confidence.",
    "positions": [
      "Card 1: Do you have an act that will make you stand out?",
      "Card 2: Are you used to showcasing your talents in public?",
      "Card 3: Do you want to practice more in front of strangers before applying?",
      "Card 4: Are you prepared to enter, even if you do not win this time?",
      "Card 5: Will/should you keep trying until you win?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "When you discover auditions are coming to your area."
  },
  {
    "number": 236,
    "slug": "will-the-person-of-your-dreams-agree-to-go-on-a-date-with-you-if-you-ask-now",
    "title": "Will The Person Of Your Dreams Agree To Go On A Date With You If You Ask Now?",
    "chapter": "Spreads For Making Your Dearest Wishes And Dreams Come True",
    "purpose": "A one-carder to discover if now is the right time to speak. If the answer is negative, you can deal a second card to ask if the person will say yes in the future.",
    "positions": [],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "The morning before you intend to ask."
  },
  {
    "number": 237,
    "slug": "should-you-spend-some-of-the-familys-future-inheritance-on-an-around",
    "title": "Should You Spend Some Of The Family\u2019S Future Inheritance On An Around-The-World Trip Or Major Holiday For Yourself?",
    "chapter": "Spreads For Making Your Dearest Wishes And Dreams Come True",
    "purpose": "When your adult children say you are selfish to spend your money on fulfilling a personal dream rather than saving it.",
    "positions": [
      "Card 1: Are you entitled to spend your own money any way you wish?",
      "Card 2: Should you feel guilty if you follow your dream?",
      "Card 3: Will you regret it if you do not follow your dream?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "When you are thinking about planning for an adventure."
  },
  {
    "number": 265,
    "slug": "will-you-like-a-new-prospective-family-member-when-you-meet-for-the-first-time",
    "title": "Will You Like A New Prospective Family Member When You Meet For The First Time?",
    "chapter": "Family Spreads",
    "purpose": "Deal and turn over one card for a yes/no result.",
    "positions": [],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "The morning of the meeting."
  },
  {
    "number": 266,
    "slug": "should-you-invite-a-particular-relative-to-a-family-gathering",
    "title": "Should You Invite A Particular Relative To A Family Gathering?",
    "chapter": "Family Spreads",
    "purpose": "When you know the person\u2019s presence will cause difficulties, but you do not want to offend.",
    "positions": [
      "Card 1: Will the invitation lead to more trouble than it is worth?",
      "Card 2: If you do not invite the person, will it cause",
      "Card 2 as a tiebreaker."
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "When you are planning the guest list."
  },
  {
    "number": 293,
    "slug": "if-your-child-or-teenager-is-being-bullied-at-school",
    "title": "If Your Child Or Teenager Is Being Bullied At School",
    "chapter": "Spreads For Babies, Children, And Grandchildren Of All Ages",
    "purpose": "When your child is afraid to go to school, but the school will not listen.",
    "positions": [
      "Card 1: Who are the main bullies? Are they generally regarded as challenging children?",
      "Card 2: What is the main reason given for bullying your child?",
      "Card 3: Do they bully other children? Can you contact other parents for support?",
      "Card 4: Can you discover the official bullying policy and insist it is followed?",
      "Card 5: Can you avoid being intimidated by the school, which may blame your child in order to defend the school\u2019s reputation?",
      "Card 6: Can you/should you go higher than the principal to resolve this?",
      "Card 7: Whatever happens, do you want to move your child into a different school?"
    ],
    "use": "The full deck:",
    "when": "A Tuesday, the day of courage."
  },
  {
    "number": 294,
    "slug": "if-your-child-or-teenager-is-being-bullied-on-social-media",
    "title": "If Your Child Or Teenager Is Being Bullied On Social Media",
    "chapter": "Spreads For Babies, Children, And Grandchildren Of All Ages",
    "purpose": "If your child becomes upset by text messages/is unduly secretive about social media contacts.",
    "positions": [
      "Card 1: Is your child receiving an unusual number of text messages/does s/he appear upset after reading text messages?",
      "Card 2: Does your child come straight home after school instead of hanging out with friends?",
      "Card 3: Does your child look anxious and is s/he constantly checking their phone for messages?",
      "Card 4: Should you make a quiet time to talk about cyber bullying?",
      "Card 5: Would one of your child\u2019s friends talk to you regarding what may be happening to your child?",
      "Card 6: Can/should you contact a school counselor/leave a teenage helpline number around where it can be seen by your child?",
      "Card 7: Can/should you offer your child a new phone/number/social media page with strict privacy settings?"
    ],
    "use": "The full deck",
    "when": "A Wednesday, day for overcoming human snakes."
  },
  {
    "number": 321,
    "slug": "the-overcoming-anxiety-spread",
    "title": "The Overcoming-Anxiety Spread",
    "chapter": "Health And Healing Spreads",
    "purpose": "When you are constantly anxious, but do not want to take calming pills.",
    "positions": [
      "Card 1: Is your anxiety triggered by external circumstances, or does it come from within?",
      "Card 2: Who or what situation makes it worse? Can you avoid these?",
      "Card 3: Who or what helps to calm the anxiety?",
      "Card 4: What instant strategies can you develop when you feel anxiety rising?",
      "Card 5: Would a change of lifestyle/location/career/relationship relieve the problem?",
      "Card 6: What new activity/desired situation suddenly becomes possible without the anxiety?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the six Court cards.",
    "when": "Any time during the waning moon."
  },
  {
    "number": 322,
    "slug": "will-your-health-improve",
    "title": "Will Your Health Improve?",
    "chapter": "Health And Healing Spreads",
    "purpose": "When you are chronically ill, but no organic or medical solution can be found.",
    "positions": [
      "Card 1: Is there anything in your life/lifestyle causing undue stress?",
      "Card 2: Should you explore alternative energy therapies such as acupuncture, acupressure, reiki, kinesiology, or meditation classes to release blocks and restore energy?",
      "Card 3: Will your health improve naturally when your life is in balance?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "A Wednesday, day of health and healing."
  },
  {
    "number": 354,
    "slug": "bringing-good-luck-into-your-life",
    "title": "Bringing Good Luck Into Your Life",
    "chapter": "Spreads For Good Luck",
    "purpose": "If you need more good luck in your life.",
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
    "when": "At the crescent or waxing moon."
  },
  {
    "number": 355,
    "slug": "will-your-bad-luck-change-soon",
    "title": "Will Your Bad Luck Change Soon?",
    "chapter": "Spreads For Good Luck",
    "purpose": "When one thing after another goes wrong, making you feel jinxed.",
    "positions": [
      "Card 1: Do you believe you are in the hands of fate? If so, is this true, or a perception?",
      "Card 2: Is anyone causing your misfortune?",
      "Card 3: Can you/how can you change your luck?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "A Friday or Saturday, both days of good fortune."
  },
  {
    "number": 382,
    "slug": "will-your-new-home-be-lucky-for-you",
    "title": "Will Your New Home Be Lucky For You?",
    "chapter": "Spreads For The Home And Property",
    "purpose": "When you have rented or purchased a new home or are about to do so.",
    "positions": [
      "Card 1: Did you feel when you first saw it that it was meant to be yours and that that was a valid feeling?",
      "Card 2: Will everything progress smoothly in negotiations/finance, etc., right through to the move?",
      "Card 3: Is this going to be a place of health, happiness, and prosperity?",
      "Card 4: Do you have any worries about the house/location and how can these be resolved?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "A Sunday for new beginnings."
  },
  {
    "number": 383,
    "slug": "will-you-ever-sell-your-home",
    "title": "Will You Ever Sell Your Home?",
    "chapter": "Spreads For The Home And Property",
    "purpose": "When your home has been on the market for a while without any serious offers.",
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
    "when": "A Wednesday for speeding up sales."
  },
  {
    "number": 411,
    "slug": "why-does-it-seem-so-hard-to-make-friends",
    "title": "Why Does It Seem So Hard To Make Friends?",
    "chapter": "Spreads For Friendships And Your Social Life",
    "purpose": "If you never seem to get asked to parties or social events.",
    "positions": [
      "Card 1: Are you naturally a loner who doesn\u2019t want company, but feel you ought to?",
      "Card 2: Would you like a few like-minded friends? How/where can you meet them?",
      "Card 3: If you want to socialize more, what deep down holds you back?",
      "Card 4: Should you seek friends online, enjoying online friendships rather than face-to-face?",
      "Card 5: Where should you go/what should you join/new activities to try to meet more people directly?",
      "Card 6: Are you in the wrong place/should you change jobs/relocate?"
    ],
    "use": "The full deck.",
    "when": "The beginning of a new week or month."
  },
  {
    "number": 412,
    "slug": "dealing-with-social-life-conflicts",
    "title": "Dealing With Social Life Conflicts",
    "chapter": "Spreads For Friendships And Your Social Life",
    "purpose": "When friendships are proving troublesome.",
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
    "when": "A Wednesday, to protect against human snakes."
  },
  {
    "number": 441,
    "slug": "are-you-both-ready-for-the-life-changes-a-baby-will-bring",
    "title": "Are You Both Ready For The Life Changes A Baby Will Bring?",
    "chapter": "Spreads For Fertility, Conception, Pregnancy, And Babies",
    "purpose": "When you are discussing having a family.",
    "positions": [
      "Card 1: What does your partner really feel?",
      "Card 2: What do you really feel?",
      "Card 3: Is this the right time/do you still have things to do as a couple first?",
      "Card 4: Are the advantages of having a family greater than the disadvantages?"
    ],
    "use": "The Major twenty-two cards.",
    "when": "At the full moon, folklorically the traditional time for conception."
  },
  {
    "number": 442,
    "slug": "is-my-partner-the-right-person-to-be-the-parent-of-my-child",
    "title": "Is My Partner The Right Person To Be The Parent Of My Child?",
    "chapter": "Spreads For Fertility, Conception, Pregnancy, And Babies",
    "purpose": "When you aren\u2019t 100% sure the person you love is good parent material.",
    "positions": [
      "Card 1: Is s/he sufficiently mature, or does s/he need more time to grow up?",
      "Card 2: Would s/he be a loving supportive co-parent?",
      "Card 3: Should I go ahead and try for a baby with him/her, or move on to another relationship/go it alone?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "When the talk turns to babies."
  },
  {
    "number": 467,
    "slug": "will-you-win-your-court-case",
    "title": "Will You Win Your Court Case?",
    "chapter": "Spreads For Justice, Truth, Compensation, And Inheritance",
    "purpose": "For a basic answer.",
    "positions": [
      "Card 1: Will judgment go in your favor?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "When deciding whether to proceed or not."
  },
  {
    "number": 468,
    "slug": "is-it-more-advantageous-to-accept-an-out-of-court-settlement-or",
    "title": "Is It More Advantageous To Accept An Out-Of-Court Settlement Or To Go Ahead With The Court Case?",
    "chapter": "Spreads For Justice, Truth, Compensation, And Inheritance",
    "purpose": "When you are tempted to settle out of court to avoid further lawyers\u2019 bills.",
    "positions": [
      "Card 1: What are the advantages of settling out of court?",
      "Card 2: What are the disadvantages of settling out of court?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "When you have received your final out-of-court offer."
  },
  {
    "number": 493,
    "slug": "should-you-buy-a-pet",
    "title": "Should You Buy A Pet?",
    "chapter": "Spreads For Pets Large And Small",
    "purpose": "When you want a pet but need to consider whether it is practical, given your lifestyle.",
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
    "when": "A Saturday, the day of animals."
  },
  {
    "number": 494,
    "slug": "choosing-the-right-pet",
    "title": "Choosing The Right Pet",
    "chapter": "Spreads For Pets Large And Small",
    "purpose": "When you want to be sure your new pet is right for you and you for your chosen pet.",
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
    "when": "Before you make your final choice."
  },
  {
    "number": 520,
    "slug": "should-you-move-to-a-particular-neighborhood",
    "title": "Should You Move To A Particular Neighborhood?",
    "chapter": "Neighbors, Neighborhood, And Community Spreads",
    "purpose": "When you have found the right house but are not sure about the neighborhood.",
    "positions": [
      "Card 1: Is this the right neighborhood for you? (answer depends on the strength of the positive feeling you get from the card)."
    ],
    "use": "The twenty-two Major cards.",
    "when": "Before you put in an offer on the property."
  },
  {
    "number": 521,
    "slug": "when-you-move-into-a-new-neighborhood-and-no-one-comes-to-greet-you",
    "title": "When You Move Into A New Neighborhood And No One Comes To Greet You",
    "chapter": "Neighbors, Neighborhood, And Community Spreads",
    "purpose": "If you come from a friendly neighborhood and aren\u2019t sure if people here are just busy or do not mix.",
    "positions": [
      "Card 1: Should you knock on a few doors to say",
      "Card 2: Should you wait for them to contact you?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Once you are settled, if contact is not forthcoming."
  },
  {
    "number": 543,
    "slug": "should-you-and-your-partner-call-your-baby-the-name-you-want",
    "title": "Should You And Your Partner Call Your Baby The Name You Want, Or The One Your Families Want?",
    "chapter": "Spreads For Celebrations",
    "purpose": "When you are being pressured to name your baby after an elderly relative or a traditional family name that you dislike.",
    "positions": [
      "Card 1: Should you call your baby by the name you want, one that will fit into the modern world?",
      "Card 2: Would it be possible/practical to use the desired family choice as a middle name to honor the family (and keep the peace)?"
    ],
    "use": "The forty Minor cards and the twenty-two Major cards.",
    "when": "A Monday, the day of all matters concerning babies."
  },
  {
    "number": 544,
    "slug": "how-can-you-decide-the-right-name-for-your-baby",
    "title": "How Can You Decide The Right Name For Your Baby?",
    "chapter": "Spreads For Celebrations",
    "purpose": "When you have several names but are having difficulty making a decision.",
    "positions": [
      "Card 1: Will you know once your baby is born/comes home which names fit the personality?",
      "Card 2: Are the most likely names ones that will sound as good with a forty-year-old as a four-year-old?",
      "Card 3: Can you resist pressure from family to",
      "Card 3 . See which cards have the strongest positive meaning. If you need further guidance, see the Numerology Spread ("
    ],
    "use": "The full deck.",
    "when": "A Sunday, a good naming day."
  },
  {
    "number": 566,
    "slug": "where-should-you-go-on-vacation",
    "title": "Where Should You Go On Vacation?",
    "chapter": "Spreads For Travel And Vacations",
    "purpose": "When you have several options but aren\u2019t sure which is best.",
    "positions": [
      "Card 1: What do you hope to gain most from your vacation?",
      "Card 2: What are the drawbacks of going on vacation, if any?",
      "Card 3: Is this/when is the right time to go on vacation?",
      "Card 4: Do you want to go far or near, or even vacation at home?",
      "Card 5: Will you have a happy vacation?"
    ],
    "use": "The full deck.",
    "when": "A Thursday, for serious planning."
  },
  {
    "number": 567,
    "slug": "where-to-stay-when-theres-a-choice-between-two-in-any-question",
    "title": "Where To Stay When There\u2019S A Choice Between Two In Any Question About Traveling Or Vacations",
    "chapter": "Spreads For Travel And Vacations",
    "purpose": "For absolutely anything where you have a choice between two different dates, hotels, locations, between two family members or friends to stay/travel with, two airlines with similar prices, two similar cruises, two city breaks, whether to go for seven or fourteen days, expensive or budget range.",
    "positions": [
      "Card 1: What factors aren\u2019t yet known that might influence the benefits and drawbacks of each choice?"
    ],
    "use": "The whole deck.",
    "when": "When you have exhausted logic and the information available and need to look over the horizon."
  },
  {
    "number": 591,
    "slug": "if-you-face-challenges-and-obstacles-to-overcome-in-order-to-achieve-desired-change",
    "title": "If You Face Challenges And Obstacles To Overcome In Order To Achieve Desired Change",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "If people or situations are getting in the way of desired change.",
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
    "when": "The beginning of any month, or New Year\u2019s Day."
  },
  {
    "number": 592,
    "slug": "for-major-life-path-choices-and-transitions",
    "title": "For Major Life-Path Choices And Transitions",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "For a major reassessment of where you are and what changes you seek.",
    "positions": [
      "Card 1: Where you are in life right now generally. Are you happy with this?",
      "Card 2: Have you met the person you want to share your future life path with? Will you meet them soon, or do you prefer to stay independent?",
      "Card 3: Is your career path as you want it? If not, how should it progress/change?",
      "Card 4: Are your leisure activities making you happy? Do you want to leave some/add new ones?",
      "Card 5: Are you as fit and healthy as you would like to be? If not, how can you improve this?",
      "Card 6: Where do you want to be/what do you want to do at this time next year?",
      "Card 7: Where do you want to be/what do you want to do/be in five years\u2019 time?",
      "Card 8: Where do you want to be/what do you want to do in ten years\u2019 time?",
      "Card 9: What is your secret dream, and can you/how can you achieve it?"
    ],
    "use": "The full deck.",
    "when": "When you have plenty of time to cast and interpret this Spread and consider the full implications."
  },
  {
    "number": 593,
    "slug": "if-you-want-to-make-a-major-life-change-but-feel-stuck",
    "title": "If You Want To Make A Major Life Change But Feel Stuck",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "When no matter how hard you try to initiate change in whatever part of your life you seek it, you\u2019re unable to progress.",
    "positions": [
      "Card 1: What practical and underlying factors are holding you back from making those changes?",
      "Card 2: Do you really want change, or do you just feel you ought to?",
      "Card 3: Is now the right time for change? Do you have unfinished business? Are you not quite ready?",
      "Card 4: If you are patient, will outside circumstances bring the desired change?",
      "Card 5: If you go all out for change and do not let anyone or anything stand in your way, will you succeed?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "At a full moon, or when Mercury has just moved out of retrograde."
  },
  {
    "number": 622,
    "slug": "a-fast-answer-sun-sign-spread",
    "title": "A Fast-Answer Sun Sign Spread",
    "chapter": "Astrological Spreads, Part 1",
    "purpose": "If you have a specific question that is of great significance, but you want a fast answer. Check back for Major card zodiac associations.",
    "positions": [
      "Card 1: The advantages of going ahead with what you are asking about.",
      "Card 2: The disadvantages of what you are asking about.",
      "Card 3: The outcome of acting/going forward."
    ],
    "use": "",
    "when": "At a full moon."
  },
  {
    "number": 623,
    "slug": "the-aries-spread-of-action",
    "title": "The Aries Spread Of Action",
    "chapter": "Astrological Spreads, Part 1",
    "purpose": "For anyone born under Aries, anyone asking the question during the Star sign period or if you need an Arian quality in your life.",
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
    "when": "During the Star sign period, or when the moon enters Aries during each month (for about two and a half days)."
  },
  {
    "number": 641,
    "slug": "the-seven-day-planet-spread",
    "title": "The Seven-Day Planet Spread",
    "chapter": "Astrological Spreads, Part 2: The Planetary Spreads",
    "purpose": "Because each of the original seven planets (prior to the discoveries of Uranus, Neptune, and Pluto), including the Sun and Moon, is associated with a day of the week, this is a perfect Spread for a mini-life review. If you get a planet Tarot card on its own day. it is especially lucky.",
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
    "when": ""
  },
  {
    "number": 642,
    "slug": "the-sun-spread-for-going-for-a-major-achievement-even-if-you",
    "title": "The Sun Spread For Going For A Major Achievement Even If You Suspect You May Be Out Of Your League",
    "chapter": "Astrological Spreads, Part 2: The Planetary Spreads",
    "purpose": "Sun:",
    "positions": [
      "Card 1: Is it",
      "Card 2: What unique qualities do you have that make you stand out?",
      "Card 3: Will you succeed this time?",
      "Card 4: If not, will you know how to succeed next time you try?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "A Sunday."
  },
  {
    "number": 657,
    "slug": "a-crescent-moon-spread-if-you-are-starting-a-new-phase-of-your-life",
    "title": "A Crescent Moon Spread If You Are Starting A New Phase Of Your Life",
    "chapter": "Moon Spreads",
    "purpose": "For a major location, career or study move or new beginning after loss or betrayal in love.",
    "positions": [
      "Card 1: What do you hope for most from this new beginning, not just outwardly?",
      "Card 2: What are the outer and inner disadvantages/worries about this new phase?",
      "Card 3: Are you fully prepared for this new phase? What have you overlooked?",
      "Card 4: Is there anything/anyone you would like/need to take with you/leave behind?",
      "Card 5: Will your new beginning bring happiness soon, or take months?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "The crescent moon, or as close as possible afterward."
  },
  {
    "number": 658,
    "slug": "a-crescent-moon-spread-for-a-new-source-of-money-in-your-life-within-a-month",
    "title": "A Crescent Moon Spread For A New Source Of Money In Your Life Within A Month",
    "chapter": "Moon Spreads",
    "purpose": "When you have a shortfall or need to find extra money fast.",
    "positions": [
      "Card 1: Could any of your existing sources of money offer short-term increase through extra hours/input?",
      "Card 2: Are there any sources/assets from which you could borrow extra money/sell to make up the shortfall?",
      "Card 3: Are/how are negotiations possible to take the immediate pressure off you?",
      "Card 4: Will this shortfall continue unless you find a more permanent/lucrative source of income/input?",
      "Card 5: Will there be unexpected help?",
      "Card 6: Will you get the money by the time of the next crescent moon?"
    ],
    "use": "The forty Minor cards and the sixteen Court cards.",
    "when": "As close to the crescent moon as possible."
  },
  {
    "number": 684,
    "slug": "a-waxing-moon-in-aries-spread-for-launching-a-self-employed-venture",
    "title": "A Waxing Moon In Aries Spread For Launching A Self-Employed Venture",
    "chapter": "Moon Zodiac Spreads",
    "purpose": "When you are wondering if you can make a go of it.",
    "positions": [
      "Card 1: What advantages are there in your going for self-employment now?",
      "Card 2: What disadvantages are there in launching now?",
      "Card 3: Go for it, wait, or abandon the idea?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Any time during the two and a half days of the month that the moon is waxing as it moves through Aries."
  },
  {
    "number": 685,
    "slug": "a-full-moon-in-aries-spread-for-independence-from-an-over-possessive",
    "title": "A Full Moon In Aries Spread For Independence From An Over-Possessive Or Dominant Family",
    "chapter": "Moon Zodiac Spreads",
    "purpose": "If you are feeling stifled by your family\u2019s constant interference in your lifestyle/decisions.",
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
    "when": "When the full moon is in Aries, about once a year."
  },
  {
    "number": 720,
    "slug": "a-new-moon-angel-spread-for-returning-to-life-after-hurt-betrayal-loss-or-illness",
    "title": "A New Moon-Angel Spread For Returning To Life After Hurt, Betrayal, Loss, Or Illness",
    "chapter": "Moon-Angel Spreads",
    "purpose": "Under the protection of angels Geniel, Enediel, and Anixiel, angels described with pale silver wings and a pale silver halo.",
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
    "when": "Days 1, 2, and 3 from when the waning moon disappears from the sky until the night of the crescent."
  },
  {
    "number": 721,
    "slug": "a-crescent-moon-angel-spread-for-new-beginnings-in-any-part-of",
    "title": "A Crescent-Moon Angel Spread For New Beginnings In Any Part Of Your Life If You Are Unsure",
    "chapter": "Moon-Angel Spreads",
    "purpose": "Under the protection of Azariel, Gabriel, and Dirachiel, crescent-moon angels with the exception of Gabriel (see",
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
    "when": "Crescent moon days 4\u20137."
  },
  {
    "number": 741,
    "slug": "a-guardian-angel-spread-if-you-are-feeling-alone-or-afraid",
    "title": "A Guardian-Angel Spread If You Are Feeling Alone Or Afraid",
    "chapter": "Angel And Archangel Spreads",
    "purpose": "Whether or not you know your guardian angel, to gain strength and support when life seems bleak. Picture your guardian angel as shimmering light.",
    "positions": [
      "Card 1: How can you feel the presence of your guardian angel in your life at this time?",
      "Card 2: What sign in the everyday world can your angel reveal so you know you are not alone?",
      "Card 3: What is the help you most need from your angel, rather than what you think you need?",
      "Card 4: Will earthly help/support come to you?",
      "Card 5: How can you most help yourself?",
      "Card 6: What special blessings will your angel bring into your life?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "As twilight falls."
  },
  {
    "number": 742,
    "slug": "an-archangel-sachiel-spread-for-a-permanent-job-if-you-can-only-get-temporary-work",
    "title": "An Archangel Sachiel Spread For A Permanent Job If You Can Only Get Temporary Work",
    "chapter": "Angel And Archangel Spreads",
    "purpose": "When you need job security. Sachiel is pictured with a rich purple and golden halo and blue and purple wings. He is the Archangel of Jupiter.",
    "positions": [
      "Card 1: Will your current workplace offer more permanent employment if you ask?",
      "Card 2: Is there one particular place you have recently worked where you did especially well that would put you on a future vacancy list?",
      "Card 3: Is there an extra qualification/expertise that would make it easier to get a permanent job?",
      "Card 4: What special help would you ask of Archangel Sachiel to open the right doors to permanent employment?",
      "Card 5: Will you succeed?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Thursday, Sachiel\u2019s special day."
  },
  {
    "number": 773,
    "slug": "spread-of-the-fool-inner-child-if-you-seek-a-new-beginning",
    "title": "Spread Of The Fool/Inner Child If You Seek A New Beginning",
    "chapter": "Crystal Tarot Spreads",
    "purpose": "\u2022 Lucky card: The Fool \u2022 Lucky crystal: clear quartz",
    "positions": [
      "Card 1: What will be the results of your new beginning?"
    ],
    "use": "",
    "when": ""
  },
  {
    "number": 774,
    "slug": "spread-of-the-magician-for-the-success-of-an-entrepreneurial-venture",
    "title": "Spread Of The Magician For The Success Of An Entrepreneurial Venture",
    "chapter": "Crystal Tarot Spreads",
    "purpose": "\u2022 Lucky card: The Magician \u2022 Lucky crystal: citrine or brown tiger eye.",
    "positions": [
      "Card 1: Will your venture succeed immediately/take longer to evolve?"
    ],
    "use": "",
    "when": ""
  },
  {
    "number": 796,
    "slug": "a-four-winds-spread-of-fate",
    "title": "A Four-Winds Spread Of Fate",
    "chapter": "Spreads For Foretelling Your Destiny",
    "purpose": "If matters feel out of your control, to see what the likely results will be and what, if anything, you can do to make things better/right.",
    "positions": [
      "Card 1: Boreas, the North Wind, the actual situation/the most likely effects if nothing changes/you do nothing.",
      "Card 2: Eurus, the East Wind, logically what can be done to positively affect matters.",
      "Card 3: Notus, the South Wind, what unexpected boost or mitigation exists of the situation from outside sources.",
      "Card 4: Zephyrus, the West Wind, what might blow you off course?",
      "Card 5: The result of all these factors coming together."
    ],
    "use": "The full deck.",
    "when": "A windy day if possible, otherwise when it is cloudy."
  },
  {
    "number": 797,
    "slug": "the-ring-of-fate-pendulum-spread-for-asking-a-specific-question-about",
    "title": "The Ring-Of-Fate Pendulum Spread For Asking A Specific Question About An Unknown Aspect Of Your Future",
    "chapter": "Spreads For Foretelling Your Destiny",
    "purpose": "Using a pendulum, a crystal on a chain, or a favorite pendant with the chain twisted to form a single chain.",
    "positions": [],
    "use": "The twenty-two Major cards.",
    "when": "When the answer cannot be deduced logically or from what is known."
  },
  {
    "number": 820,
    "slug": "the-coming-into-balance-spread",
    "title": "The Coming-Into-Balance Spread",
    "chapter": "Spreads For Self-Awareness And Knowledge And Planning Your Life Path",
    "purpose": "When external events or relationships are proving chaotic and you want normality restored in your own life.",
    "positions": [
      "Card 1: What/who really caused/is causing the chaos?",
      "Card 2: Should you intervene, or wait for things to settle?",
      "Card 3: Who/what will prove most helpful in bringing peace to the situation?",
      "Card 4: How can you restore your own balance if others\u2019 behaviors are shaking it?",
      "Card 5: How can you prevent others\u2019 future chaos affecting your lasting harmony?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "A Friday, the day of finding peace."
  },
  {
    "number": 821,
    "slug": "the-hidden-self-spread",
    "title": "The Hidden-Self Spread",
    "chapter": "Spreads For Self-Awareness And Knowledge And Planning Your Life Path",
    "purpose": "When you feel that the image you present to the world is holding you back from revealing your true self.",
    "positions": [
      "Card 1: How you are seen by the world.",
      "Card 2: The hidden self the world never sees.",
      "Card 3: How you can combine the two, so you feel at home in the world without becoming too vulnerable."
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "At a crescent moon, or early in the waxing cycle"
  },
  {
    "number": 848,
    "slug": "visualizing-your-chosen-card-in-your-minds-eye-for-an-in-depth",
    "title": "Visualizing Your Chosen Card In Your Mind\u2019S Eye For An In-Depth Understanding Into The Card\u2019S Relevance To Your Life",
    "chapter": "Combining Tarot Spreads And Psychic Powers",
    "purpose": "Expanding the meaning of the card using clairvoyant or psychic vision through your Third or mind\u2019s eye.",
    "positions": [],
    "use": "Twenty-two Major cards and thirty-six Minor cards, Twos to Tens (Aces aren\u2019t detailed enough).",
    "when": "An evening by candlelight when you will not be disturbed."
  },
  {
    "number": 849,
    "slug": "a-tarot-spread-using-automatic-writing",
    "title": "A Tarot Spread Using Automatic Writing",
    "chapter": "Combining Tarot Spreads And Psychic Powers",
    "purpose": "Choose a card from the deck as you ask a question. Hold the card in the hand you do not write with. Allow your hand to write without consciously formulating words. When your hand slows, read what you have written. If you wish, choose another card and repeat the process, using up to five cards, one at a time. The information reveals what was not known about the question.",
    "positions": [],
    "use": "The full deck.",
    "when": "When a matter has hidden factors."
  },
  {
    "number": 870,
    "slug": "a-four-seasons-spread",
    "title": "A Four-Seasons Spread",
    "chapter": "Spreads For Festivals And Seasons",
    "purpose": "To link your inner changing energies with the changing energy flows of the year.",
    "positions": [
      "Card 1: Spring: What is growing/needs to grow in your life?",
      "Card 2: Summer: How can you best gain recognition/rewards for your efforts?",
      "Card 3: Fall: What has worked well and will continue to flourish in your life?",
      "Card 4: Winter: What needs preserving for longer-term results, and what to let go?",
      "Card 5: Which will be my best season in the year ahead?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Start at any seasonal change points, or at any time during the current season."
  },
  {
    "number": 871,
    "slug": "a-month-by-month-spread-for-taking-advantage-of-the-underlying-energies",
    "title": "A Month-By-Month Spread For Taking Advantage Of The Underlying Energies Of Each Month",
    "chapter": "Spreads For Festivals And Seasons",
    "purpose": "Discovering what the cards say about how you should take advantage/avoid pitfalls each month. According to the meaning of the card, you will know whether following the month trend will bring a positive result, or a challenge you will need to win through in order to succeed.",
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
      "Card 10: October: Should you avoid being involved in other people\u2019s quarrels/trying to keep everyone around you happy?",
      "Card 11: November: Should you focus on your spiritual self/explore your psychic abilities to keep you one step ahead?",
      "Card 12: December: Should you enroll to learn something new/take an opportunity to extend your skills when the New Year begins?"
    ],
    "use": "The full deck.",
    "when": "Start the reading in the current month, or the first day of the following month."
  },
  {
    "number": 896,
    "slug": "a-st-joan-of-arc-spread-for-deciding-whether-to-continue-to",
    "title": "A St.-Joan-Of-Arc Spread For Deciding Whether To Continue To Seek Justice Or Accept A Compromise",
    "chapter": "Tarot Spreads And The Saints",
    "purpose": "The warrior Saint. If you are running out of money for a court case, but fear that to give way now would be to condone injustice.",
    "positions": [
      "Card 1: If you carry on to the bitter end and win, will you recoup your expenses and more and be vindicated?",
      "Card 2: If you lose the case, will you suffer a severe financial loss because of court costs?",
      "Card 3: Should you transfer to a no-win/no-fee lawyer (also known as a contingency fee agreement), or do you want to stay with the lawyer you know and trust even if they do not work on a no-win/no-fee arrangement?",
      "Card 4: If partial compensation can be negotiated outside court, would that be enough to prove to the world that you were in the right?",
      "Card 5: Should you risk all?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "A Tuesday for courage, or a Thursday for justice."
  },
  {
    "number": 897,
    "slug": "a-st-martha-dragon-slaying-spread-for-dealing-with-a-difficult-relative",
    "title": "A St.-Martha-Dragon-Slaying Spread For Dealing With A Difficult Relative Without Causing A Major Family Rift",
    "chapter": "Tarot Spreads And The Saints",
    "purpose": "The motherly St. Martha slayed a dragon because it was threatening the people of Tarascon, an ancient fortified town on the Rh\u00f4ne, between Avignon and Arles in France, not with a sword but by sprinkling holy water over it. When you know the difficult relative is just unhappy, rather than malicious.",
    "positions": [
      "Card 1: Can/should you deal with the underlying unhappiness that is causing the problem, or try to resolve it once and for all?",
      "Card 2: Is anybody causing trouble behind the scenes and offloading the blame?",
      "Card 3: Is this a long-standing problem that can only have a temporary fix to avoid immediate disruption?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Traditionally, St. Martha is asked for help on a Tuesday."
  },
  {
    "number": 921,
    "slug": "the-sports-and-fitness-spread",
    "title": "The Sports-And-Fitness Spread",
    "chapter": "The Go-For-It Spreads: Health, Fitness, Leisure, And Sports",
    "purpose": "When you are considering how far to push yourself in sports and fitness.",
    "positions": [
      "Card 1: Should you undertake serious training with the aim of turning professional?",
      "Card 2: Would you be happier just getting fit or joining a team for pleasure?",
      "Card 3: Would gentle exercise for personal satisfaction and health be just one part of your many wider interests or occupations?",
      "Card 4: If you go for the top, will you succeed totally/partly/be happy?"
    ],
    "use": "The full deck.",
    "when": "A Wednesday for health and fitness, also for competitiveness."
  },
  {
    "number": 922,
    "slug": "if-you-are-worried-about-the-way-other-people-perceive-your-appearance",
    "title": "If You Are Worried About The Way Other People Perceive Your Appearance And Feel Getting Fit Will Help",
    "chapter": "The Go-For-It Spreads: Health, Fitness, Leisure, And Sports",
    "purpose": "When you are feeling negative about your body image and are looking for a way to improve your self-confidence.",
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
    "when": ""
  },
  {
    "number": 951,
    "slug": "breaking-down-the-walls-that-stop-you-seeking-an-alternative-lifestyle",
    "title": "Breaking Down The Walls That Stop You Seeking An Alternative Lifestyle",
    "chapter": "Spreads For Alternative Lifestyles, Doing Your Own Thing, And Living Your Own Way",
    "purpose": "For finding the freedom and independence you want and need. This is a more concise version of the earlier nine-card Tower of Freedom Spread for gaining clarity. Cards 1, 2, 3, and 4 each represent a wall; after you have read each one, remove it from the Spread.",
    "positions": [
      "Card 1: The barriers of convention that may still hold you back through the disapproval of others and all those old voices from childhood.",
      "Card 2: The wall of economic stability: How you would manage financially if you gave up your steady day job to earn money based on your initiative and ingenuity.",
      "Card 3: The hidden fear: What has sometimes held you back because it hasn\u2019t been examined and faced or overcome.",
      "Card 4: The practical organization, selling up and finding somewhere new to live, maybe not even a house but a boat or recreational vehicle, where to go, what if you fall ill.",
      "Card 5: The way of freedom."
    ],
    "use": "The full deck.",
    "when": "When you change"
  },
  {
    "number": 952,
    "slug": "if-you-are-offered-a-run-down-animal-sanctuary-or-indigenous-wildlife-center",
    "title": "If You Are Offered A Run-Down Animal Sanctuary Or Indigenous Wildlife Center",
    "chapter": "Spreads For Alternative Lifestyles, Doing Your Own Thing, And Living Your Own Way",
    "purpose": "When it would be a dream come true but would need a lot of financing and organizing.",
    "positions": [
      "Card 1: Could/should you take it over even though it would need time and resources to get it up and running?",
      "Card 2: Would it be better to turn the offer down and look for land/buildings suitable for conversion to fulfill your own blueprint?",
      "Card 3: Should you accept but keep your day job/give yourself a time limit to make it a viable enterprise?",
      "Card 4: Will your dreams of saving wildlife materialize?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "When you have looked at the finances and practicalities but hesitate in making a decision."
  },
  {
    "number": 976,
    "slug": "when-a-relationship-is-all-about-sex-and-not-about-love",
    "title": "When A Relationship Is All About Sex And Not About Love",
    "chapter": "Passion And Temptation Spreads",
    "purpose": "If you regularly meet for a date followed by sex, but the relationship doesn\u2019t progress.",
    "positions": [
      "Card 1: Are you happy with this arrangement for now/for the foreseeable future?",
      "Card 2: Do you want to spend time together/go on vacation, but your partner is not free?",
      "Card 3: Are you ready to risk the relationship by asking for more?",
      "Card 4: Are you outgrowing the relationship as fun but going nowhere?"
    ],
    "use": "The sixteen Court cards.",
    "when": "When the excitement is waning."
  },
  {
    "number": 977,
    "slug": "if-your-new-love-is-giving-mixed-messages-about-lovemaking",
    "title": "If Your New Love Is Giving Mixed Messages About Lovemaking",
    "chapter": "Passion And Temptation Spreads",
    "purpose": "If you have indicated that you are willing and your love seems keen, but nothing happens.",
    "positions": [
      "Card 1: Is your new love generally shy/finds it hard to show affection?",
      "Card 2: Has your love come out of a bad",
      "Card 3: Should you take the initiative?",
      "Card 4: Should you arrange a weekend vacation where it\u2019s obvious that you are sharing a room?",
      "Card 5: Should you talk about the subject generally, or would that send him/her heading for the hills fast?",
      "Card 6: If the relationship is otherwise good and sex is seen as a serious step to commitment by your partner, should you wait until your partner is ready?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Any evening before you meet."
  },
  {
    "number": 989,
    "slug": "when-a-relative-or-close-friend-dies-in-an-accident",
    "title": "When A Relative Or Close Friend Dies In An Accident",
    "chapter": "Spreads For Grief And Loss",
    "purpose": "When the loss makes no sense and seems such a waste of life.",
    "positions": [
      "Card 1: Do you have closure why/how the accident happened/justice against anyone to blame?",
      "Card 2: If not, can this/how can justice/closure be obtained, if necessary by increasing pressure for justice/an official inquiry?",
      "Card 3: How can you best remember the person at their most vibrant/collect memories in recordings/videos/photographs or a memory book so younger and future family members will know them?",
      "Card 4: What kind of a memorial would your relative have liked/at the place of the accident/in a favorite spot/a prize or trophy in their honor?",
      "Card 5: What can be done to campaign to prevent similar accidents/if, for example, it was a dangerous stretch of road or lack of safety measures in the workplace?",
      "Card 6: What can you do in your life that they planned to do in order to fulfill their wishes?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "A Sunday with the sun rising again."
  },
  {
    "number": 990,
    "slug": "when-a-relative-suffers-a-mysterious-death-and-you-cannot-get-justice",
    "title": "When A Relative Suffers A Mysterious Death And You Cannot Get Justice",
    "chapter": "Spreads For Grief And Loss",
    "purpose": "When the police insist the death is suicide or an accident, but you know that there are unexplained facts.",
    "positions": [
      "Card 1: Do the circumstances of the death go against your relative\u2019s pattern of behavior/where they would have been/had unexplained injuries?",
      "Card 2: Was your relative worried but wouldn\u2019t explain why/was getting strange phone calls/had dubious friends/connections with drugs?",
      "Card 3: Are the police so overwhelmed that they are going for the easiest explanation/if you live in a small community could there be a cover-up?",
      "Card 4: Do you want justice/are prepared to hire a detective/go to an investigative journalist/a medium?",
      "Card 5: Although people say let it rest, are you determined justice will be done?",
      "Card 6: Do you just want to move away/let your relative rest in peace?",
      "Card 7: Will you get justice if you persist?"
    ],
    "use": "The full deck.",
    "when": "When no one will listen to you."
  },
  {
    "number": 1001,
    "slug": "your-personal-year-ahead-spread",
    "title": "Your Personal-Year-Ahead Spread",
    "chapter": "Spread 1001",
    "purpose": "A year-ahead master spread that reviews six life areas month by month and then frames the overall theme, surprise, opportunity, and challenge.",
    "positions": [
      "Card 1 that remains is your overall year theme;",
      "Card 2 is what is unexpected in the year ahead;",
      "Card 3 is a particular opportunity the year will bring; and",
      "Card 4 is the challenges to be overcome in the year ahead."
    ],
    "use": "Use the full deck, removing the Death and Devil cards before laying out the year review.",
    "when": "Ideal on New Year's Day or at the start of any new personal cycle."
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
    cards: list[dict[str, Any]] = []
    for slug, name in MAJOR_CARDS:
        meaning = MAJOR_MEANINGS[slug]
        cards.append({"slug": slug, "name": name, "arcana": "major", "suit": None, "rank": None, "upright": f"Upright, {name} speaks of {meaning['upright']}. In a reading it usually shows the theme becoming visible, active, and impossible to ignore. It asks for conscious participation rather than passive hope.", "reversed": f"Reversed, {name} often points to {meaning['reversed']}. The lesson is still present, but it may be internalised, delayed, or distorted by fear, over-control, or avoidance.", "love": f"In love readings, {name} highlights {meaning['upright']} and asks whether the relationship can hold that energy honestly.", "career": f"In career readings, {name} often shows {meaning['upright']} affecting leadership, timing, responsibility, or visibility.", "health": f"In wellbeing readings, {name} can symbolise how the nervous system, mindset, and daily rhythm respond to {meaning['upright']}.", "imagery": meaning["imagery"]})
    ordered_ranks = ["ace", "02", "03", "04", "05", "06", "07", "08", "09", "10", "page", "knight", "queen", "king"]
    for suit_slug, meta in SUIT_META.items():
        for rank in ordered_ranks:
            label, tone = RANK_DETAILS[rank]
            slug = f"{label.lower().replace(' ', '-')}-of-{suit_slug}"
            name = f"{label} of {meta['label']}"
            cards.append({"slug": slug, "name": name, "arcana": "minor", "suit": suit_slug, "rank": rank, "upright": f"Upright, {name} points to {tone} expressed through {meta['element'].lower()} energy. It shows the suit's theme moving outward in a readable, practical way.", "reversed": f"Reversed, {name} suggests the same lesson is meeting resistance, delay, or misdirection. It often asks for pacing, honesty, and a reset in how the energy is used.", "love": f"In love readings, {name} often speaks to {meta['love']}.", "career": f"In career readings, {name} usually reflects {meta['career']}.", "health": f"In health readings, {name} can highlight {meta['health']}.", "imagery": f"{name} uses the imagery of {meta['imagery']} while the rank emphasises {tone}."})
    return cards

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
