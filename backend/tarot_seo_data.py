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
    "purpose": "This one-card practice is for moments when you want a daily anchor before the day begins. It keeps the reading focused so one clear symbol can name the energy, lesson, or invitation most active right now.",
    "positions": [],
    "use": "A full deck of seventy-eight cards. Choose one card at random from anywhere in the facedown deck.",
    "when": "Come to this spread when you want a daily anchor before the day begins. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 2,
    "slug": "one-question",
    "title": "One Question",
    "chapter": "One-Card Spreads",
    "purpose": "Use this single-card draw when you need a clean, uncluttered answer to a single question. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [],
    "use": "A single card from the full deck of seventy-eight cards. Choose one card taken at random from anywhere in the facedown deck. If the answer is not clear, add a second card.",
    "when": "Turn to it when you need a clean, uncluttered answer to a single question. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 13,
    "slug": "should-you-continue-saving-for-a-house-or-take-a-break-and",
    "title": "Should You Continue Saving For A House, Or Take A Break And Have A Longed-For Vacation Overseas?",
    "chapter": "Two-Card Spreads",
    "purpose": "A practical 2-card spread for times when a work, money, or long-range practical decision needs a steadier reading. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [],
    "use": "The full deck. Choose, before turning the cards over, one card for each option and read left to right.",
    "when": "Use it when a work, money, or long-range practical decision needs a steadier reading. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 14,
    "slug": "should-you-go-for-a-major-promotion-or-focus-on-happiness-in-your-out-of-work-life",
    "title": "Should You Go For A Major Promotion, Or Focus On Happiness In Your Out-Of-Work Life?",
    "chapter": "Two-Card Spreads",
    "purpose": "This layout is most useful when a work, money, or long-range practical decision needs a steadier reading. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [],
    "use": "The full deck.",
    "when": "Reach for it when a work, money, or long-range practical decision needs a steadier reading. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 25,
    "slug": "a-three-card-unstructured-reading-to-answer-any-question-on-any-topic",
    "title": "A Three-Card Unstructured Reading To Answer Any Question On Any Topic",
    "chapter": "Three-Card Spreads",
    "purpose": "Use this single-card draw when you want structured guidance around three card unstructured reading to answer any question on any topic. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [
      "Card 2 to act as the"
    ],
    "use": "A full deck of 78 cards.",
    "when": "Come to this spread when you want structured guidance around three card unstructured reading to answer any question on any topic. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 26,
    "slug": "past-present-and-future",
    "title": "Past, Present, And Future",
    "chapter": "Three-Card Spreads",
    "purpose": "Use this 3-card layout when you need to understand what is ending, what is active now, and what direction the path is taking. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: What you need to leave behind to make the change or what is already moving out of your life.",
      "Card 2: The present influences and factors already emerging affecting your decision.",
      "Card 3: The results of taking action and what lies over the horizon if you do."
    ],
    "use": "The full seventy-eight-card deck.",
    "when": "Turn to it when you need to understand what is ending, what is active now, and what direction the path is taking. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 27,
    "slug": "what-lies-ahead-an-overview-of-the-next-three-days-weeks-or-months",
    "title": "What Lies Ahead An Overview Of The Next Three Days, Weeks, Or Months",
    "chapter": "Three-Card Spreads",
    "purpose": "A practical 3-card spread for times when you want to read a longer cycle rather than a single event. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Will represent factors or people who will be helpful.",
      "Card 2: Will signify factors or people who may stand in your way. And the all-important",
      "Card 3 represents what"
    ],
    "use": "The forty Number cards, Ace to Ten, and the sixteen Court or Personality cards.",
    "when": "Use it when you want to read a longer cycle rather than a single event. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 37,
    "slug": "an-unstructured-reading-of-four-cards",
    "title": "An Unstructured Reading Of Four Cards",
    "chapter": "Four-Card Spreads",
    "purpose": "This layout is most useful when you want structured guidance around unstructured reading of four cards. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [],
    "use": "Any combination of the seventy-eight cards that fits with your question.",
    "when": "Reach for it when you want structured guidance around unstructured reading of four cards. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 38,
    "slug": "spread-for-breaking-through-the-barriers-of-fear",
    "title": "Spread For Breaking Through The Barriers Of Fear",
    "chapter": "Four-Card Spreads",
    "purpose": "This 4-card spread is built for moments when fear, pressure, or social stress is shaping your choices more than you want it to. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: What is the real cause of my fear?",
      "Card 2: Is this bad thing actually likely to happen, or is it just fear?",
      "Card 3: What triggers/makes the fear worse?",
      "Card 4: What action can I take to prevent or overcome my fear?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when fear, pressure, or social stress is shaping your choices more than you want it to. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 47,
    "slug": "the-horseshoe-spread",
    "title": "The Horseshoe Spread",
    "chapter": "Five-Card Spreads",
    "purpose": "Use this 6-card layout when the situation has several visible and hidden influences moving at once. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Your choice, dilemma or predominant question.",
      "Card 2: Present influences, people, and circumstances that affect your present position.",
      "Card 3: Hidden influences, both the messages in our heads from the past and what is just beyond the horizon.",
      "Card 4: Suggested action, whether to change or preserve the status quo.",
      "Card 5: Likely outcome, of either acting or waiting according to",
      "Card 4 ."
    ],
    "use": "The full deck.",
    "when": "Turn to it when the situation has several visible and hidden influences moving at once. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 48,
    "slug": "dealing-with-cliques-and-petty-bullying",
    "title": "Dealing With Cliques And Petty Bullying",
    "chapter": "Five-Card Spreads",
    "purpose": "A practical 5-card spread for times when fear, pressure, or social stress is shaping your choices more than you want it to. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Who/what is excluding me most.",
      "Card 2: What the motive is.",
      "Card 3: Can or should I ignore it?",
      "Card 4: Should I complain/tackle it head on?",
      "Card 5: Should I cut my losses and leave?"
    ],
    "use": "The full deck.",
    "when": "Use it when fear, pressure, or social stress is shaping your choices more than you want it to. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 49,
    "slug": "the-five-year-plan",
    "title": "The Five-Year Plan",
    "chapter": "Five-Card Spreads",
    "purpose": "This layout is most useful when you are working with the theme of five year plan. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Where I am now.",
      "Card 2: Where I would like to be in five years' time.",
      "Card 3: What extra resources/training/practice do I need?",
      "Card 4: Any possible challenges to overcome?",
      "Card 5: To achieve this long-term goal, do I need to expand/move on now, or stay where I am?"
    ],
    "use": "The full deck.",
    "when": "Reach for it when you are working with the theme of five year plan. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 56,
    "slug": "an-unstructured-six-card-spread-to-answer-any-question-on-any-topic",
    "title": "An Unstructured Six-Card Spread To Answer Any Question On Any Topic",
    "chapter": "Six-Card Spreads",
    "purpose": "This one-card practice is for moments when you want structured guidance around unstructured six card spread to answer any question on any topic. It keeps the reading focused so one clear symbol can name the energy, lesson, or invitation most active right now.",
    "positions": [
      "Card 6 the answer falls into place. Almost always the person shown in each card represents you--or, if not, then the person/people who affect the question."
    ],
    "use": "A full deck of seventy-eight cards.",
    "when": "Come to this spread when you want structured guidance around unstructured six card spread to answer any question on any topic. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 57,
    "slug": "the-next-six-weeks-months-spread",
    "title": "The Next Six Weeks/Months Spread",
    "chapter": "Six-Card Spreads",
    "purpose": "Use this 6-card layout when you want to read a longer cycle rather than a single event. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: What do you hope to achieve in the next six weeks/months?",
      "Card 2: What specific opportunities are you seeking?",
      "Card 3: What challenges are you worried about?",
      "Card 4: What would you like to remain unchanged?",
      "Card 5: What/who would you like to change?",
      "Card 6: What do you seek in the longer term?"
    ],
    "use": "The full deck.",
    "when": "Turn to it when you want to read a longer cycle rather than a single event. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 58,
    "slug": "will-i-ever-find-my-soul-mate",
    "title": "Will I Ever Find My Soul Mate?",
    "chapter": "Six-Card Spreads",
    "purpose": "A practical 6-card spread for times when your heart is involved and you need clarity about connection, desire, or commitment. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Should I give up looking and just wait for it to happen?",
      "Card 2: Should I try an online dating site/friendship group?",
      "Card 3: Should I join a face-to-face/singles group?",
      "Card 4: Should I join new activities?",
      "Card 5: Should I relocate/change my job?",
      "Card 6: Will I meet my Twin Soul, or settle for someone nice?"
    ],
    "use": "The whole deck.",
    "when": "Use it when your heart is involved and you need clarity about connection, desire, or commitment. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 64,
    "slug": "the-options-spread",
    "title": "The Options Spread",
    "chapter": "Seven-Card Spreads",
    "purpose": "This layout is most useful when two strong options are competing for your attention. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when two strong options are competing for your attention. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 65,
    "slug": "the-mystical-seven-spread",
    "title": "The Mystical Seven Spread",
    "chapter": "Seven-Card Spreads",
    "purpose": "Use this single-card draw when you want the reading to reach hidden, symbolic, or intuitive layers of the question. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [
      "Card 7, will reveal what is just over the horizon or being hidden and the answer to your dilemma."
    ],
    "use": "The twenty-two Major cards or the full deck.",
    "when": "Come to this spread when you want the reading to reach hidden, symbolic, or intuitive layers of the question. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 70,
    "slug": "moving-toward-fulfilling-your-greatest-ambition-or-dream",
    "title": "Moving Toward Fulfilling Your Greatest Ambition Or Dream",
    "chapter": "Eight-Card Spreads",
    "purpose": "Use this 8-card layout when the theme of moving toward fulfilling your greatest ambition or dream is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
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
    "when": "Turn to it when the theme of moving toward fulfilling your greatest ambition or dream is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 71,
    "slug": "should-you-try-to-conceive-a-baby",
    "title": "Should You Try To Conceive A Baby?",
    "chapter": "Eight-Card Spreads",
    "purpose": "A practical 8-card spread for times when you are weighing whether try to conceive a baby. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
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
    "when": "Use it when you are weighing whether try to conceive a baby. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 76,
    "slug": "an-unstructured-nine-card-reading",
    "title": "An Unstructured Nine-Card Reading",
    "chapter": "Nine-Card Spreads",
    "purpose": "Use this single-card draw when you want structured guidance around unstructured nine card reading. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [
      "Card 9 ."
    ],
    "use": "The full deck.",
    "when": "Reach for it when you want structured guidance around unstructured nine card reading. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 77,
    "slug": "the-pathway-to-justice",
    "title": "The Pathway To Justice",
    "chapter": "Nine-Card Spreads",
    "purpose": "This 9-card spread is built for moments when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 82,
    "slug": "an-unstructured-twelve-card-spread",
    "title": "An Unstructured Twelve-Card Spread",
    "chapter": "Multi-Card Spreads",
    "purpose": "Use this 12-card layout when you want structured guidance around unstructured twelve card spread. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [],
    "use": "The full deck.",
    "when": "Turn to it when you want structured guidance around unstructured twelve card spread. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 83,
    "slug": "a-wheel-of-the-year-twelve-months-ahead-spread",
    "title": "A Wheel Of The Year Twelve-Months-Ahead Spread",
    "chapter": "Multi-Card Spreads",
    "purpose": "Use this single-card draw when you want to read a longer cycle rather than a single event. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [
      "Card 1 being the month following the reading. Record the opportunities or challenges each card suggests during a particular month. As a rule, Major Arcana cards indicate major events or where outside circumstances play a big part. Minor cards refer to more ordinary but nevertheless significant happenings occurring in the period you are measuring. Court cards indicate dominant personalities--or a new love or pregnancy. Finally, choose a card to sum up the twelve months ahead and put this in the center of the circle. You can pick two cards for each month if you wish."
    ],
    "use": "One or two full decks.",
    "when": "Use it when you want to read a longer cycle rather than a single event. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 87,
    "slug": "have-i-found-my-soulmate-from-a-past-world",
    "title": "Have I Found My Soulmate From A Past World?",
    "chapter": "Love And Commitment Spreads",
    "purpose": "This layout is most useful when your heart is involved and you need clarity about connection, desire, or commitment. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when your heart is involved and you need clarity about connection, desire, or commitment. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 88,
    "slug": "can-it-be-true-i-have-met-my-twin-soul-at-last",
    "title": "Can It Be True I Have Met My Twin Soul At Last?",
    "chapter": "Love And Commitment Spreads",
    "purpose": "This 6-card spread is built for moments when the theme of can it be true i have met my twin soul at last is active in your life. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: Do you feel you have known each other forever?",
      "Card 2: Was there instant recognition/connection at the first meeting?",
      "Card 3: Does s/he fit totally with your family/friends/interests?",
      "Card 4: Is the relationship fast-moving but quite natural-feeling?",
      "Card 5: Is a missing part of your life now complete?",
      "Card 6: Do you have constant déjà vu and telepathic links?"
    ],
    "use": "The full deck.",
    "when": "Come to this spread when the theme of can it be true i have met my twin soul at last is active in your life. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 108,
    "slug": "the-love-quarrel",
    "title": "The Love Quarrel",
    "chapter": "Spreads For Overcoming Difficulties In Love, Reconciliation, And Ending Destructive Relationships",
    "purpose": "Use this 6-card layout when your heart is involved and you need clarity about connection, desire, or commitment. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 2: What is the underlying issue for you?",
      "Card 3: What is the underlying issue for your partner?",
      "Card 5: Are there principles on which you cannot/will not back down?",
      "Card 6: Are there issues on which your partner cannot/will not back down?",
      "Card 8: Is anyone outside fueling the fire?",
      "Card 9: What is the best outcome?"
    ],
    "use": "The full deck.",
    "when": "Turn to it when your heart is involved and you need clarity about connection, desire, or commitment. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 109,
    "slug": "the-immature-partner",
    "title": "The Immature Partner",
    "chapter": "Spreads For Overcoming Difficulties In Love, Reconciliation, And Ending Destructive Relationships",
    "purpose": "A practical 6-card spread for times when your heart is involved and you need clarity about connection, desire, or commitment. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: How is this most adversely affecting the relationship?",
      "Card 2: Will s/he change, given time?",
      "Card 3: How can change come about?",
      "Card 4: If s/he doesn't grow up, should I stick with the relationship?",
      "Card 5: What can I do to make things better?",
      "Card 6: Who/what bad influences need to be removed from his/her life?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Use it when your heart is involved and you need clarity about connection, desire, or commitment. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 129,
    "slug": "to-make-money-fast-and-urgently",
    "title": "To Make Money Fast And Urgently",
    "chapter": "Prosperity And Money-Making Spreads",
    "purpose": "This layout is most useful when a work, money, or long-range practical decision needs a steadier reading. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when a work, money, or long-range practical decision needs a steadier reading. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 130,
    "slug": "if-you-are-offered-an-overseas-offshore-job-with-a-huge-tax-free-salary",
    "title": "If You Are Offered An Overseas/Offshore Job With A Huge Tax-Free Salary",
    "chapter": "Prosperity And Money-Making Spreads",
    "purpose": "This 5-card spread is built for moments when a work, money, or long-range practical decision needs a steadier reading. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: What benefits of taking the offer short-term might outweigh other considerations?",
      "Card 2: What longer-term advantages would occur if you stayed in the job indefinitely?",
      "Card 3: What emotional/lifestyle problems might arise, and can they be overcome?",
      "Card 4: What are the hidden drawbacks?",
      "Card 5: Yes or no, taking the other four cards into account."
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when a work, money, or long-range practical decision needs a steadier reading. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 149,
    "slug": "why-does-money-drain-out-no-matter-how-hard-you-try",
    "title": "Why Does Money Drain Out, No Matter How Hard You Try?",
    "chapter": "Spreads For Solving Difficulties With Money",
    "purpose": "Use this 6-card layout when a work, money, or long-range practical decision needs a steadier reading. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Turn to it when a work, money, or long-range practical decision needs a steadier reading. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 150,
    "slug": "why-do-people-take-advantage-of-you-financially",
    "title": "Why Do People Take Advantage Of You Financially?",
    "chapter": "Spreads For Solving Difficulties With Money",
    "purpose": "A practical 6-card spread for times when a work, money, or long-range practical decision needs a steadier reading. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: What stops you from saying no?",
      "Card 2: Who takes advantage of you the most?",
      "Card 3: How will you cope with the resentment/pressure if you start saying no?",
      "Card 4: What do you gain by being overly generous?",
      "Card 5: Who will resist/protest/use emotional blackmail if you say no?",
      "Card 6: Are you with the wrong people?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Use it when a work, money, or long-range practical decision needs a steadier reading. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 169,
    "slug": "will-you-get-the-job-you-are-applying-for",
    "title": "Will You Get The Job You Are Applying For?",
    "chapter": "Career Spreads",
    "purpose": "This layout is most useful when a work, money, or long-range practical decision needs a steadier reading. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Are there more indications in your favor?",
      "Card 2: Are there more indications that you may not get this job?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Reach for it when a work, money, or long-range practical decision needs a steadier reading. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 170,
    "slug": "when-you-are-constantly-in-conflict-with-a-colleague-or-manager",
    "title": "When You Are Constantly In Conflict With A Colleague Or Manager",
    "chapter": "Career Spreads",
    "purpose": "This 3-card spread is built for moments when when you are constantly in conflict with a colleague or manager. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: The open cause of the conflict.",
      "Card 2: The hidden cause of the conflict.",
      "Card 3: The solution."
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread when when you are constantly in conflict with a colleague or manager. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 171,
    "slug": "which-should-take-priority-right-now-your-day-job-or-your-on-the-side-business",
    "title": "Which Should Take Priority Right Now Your Day Job, Or Your On-The-Side Business?",
    "chapter": "Career Spreads",
    "purpose": "Use this 2-card layout when a work, money, or long-range practical decision needs a steadier reading. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1 and",
      "Card 2 and neither seems definite, add a third card above and between"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Turn to it when a work, money, or long-range practical decision needs a steadier reading. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 191,
    "slug": "starting-your-own-business",
    "title": "Starting Your Own Business",
    "chapter": "Business Spreads",
    "purpose": "A practical 5-card spread for times when a work, money, or long-range practical decision needs a steadier reading. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Are you ready to launch your business?",
      "Card 2: Should you launch it 100%, or run it part-time until established?",
      "Card 3: Is there an existing market for your business, or do you need to create one?",
      "Card 4: Are the premises/equipment you have/will obtain adequate?",
      "Card 5: What expansion plans will be viable over the next twelve months?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Use it when a work, money, or long-range practical decision needs a steadier reading. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 192,
    "slug": "should-you-trade-your-products-or-services-locally-or-online",
    "title": "Should You Trade Your Products Or Services Locally, Or Online?",
    "chapter": "Business Spreads",
    "purpose": "This layout is most useful when you are weighing whether trade your products or services locally or online. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when you are weighing whether trade your products or services locally or online. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 211,
    "slug": "what-should-you-do-to-get-through-to-the-finals-of-a-major-talent-contest",
    "title": "What Should You Do To Get Through To The Finals Of A Major Talent Contest?",
    "chapter": "Spreads For Fame And Fortune",
    "purpose": "This 2-card spread is built for moments when you want a clearer read on what should you do to get through to the finals of a major talent contest. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: What do you need to know to get into the final?",
      "Card 2: How can you best overcome the competition of other entrants?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Come to this spread when you want a clearer read on what should you do to get through to the finals of a major talent contest. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 212,
    "slug": "if-you-want-to-win-a-tv-talent-show",
    "title": "If You Want To Win A TV Talent Show",
    "chapter": "Spreads For Fame And Fortune",
    "purpose": "Use this 5-card layout when you want to win a tv talent show. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Do you have an act that will make you stand out?",
      "Card 2: Are you used to showcasing your talents in public?",
      "Card 3: Do you want to practice more in front of strangers before applying?",
      "Card 4: Are you prepared to enter, even if you do not win this time?",
      "Card 5: Will/should you keep trying until you win?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Turn to it when you want to win a tv talent show. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 236,
    "slug": "will-the-person-of-your-dreams-agree-to-go-on-a-date-with-you-if-you-ask-now",
    "title": "Will The Person Of Your Dreams Agree To Go On A Date With You If You Ask Now?",
    "chapter": "Spreads For Making Your Dearest Wishes And Dreams Come True",
    "purpose": "A practical 6-card spread for times when the theme of will the person of your dreams agree to go on a date with you if you ask now is active in your life. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Use it when the theme of will the person of your dreams agree to go on a date with you if you ask now is active in your life. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 237,
    "slug": "should-you-spend-some-of-the-familys-future-inheritance-on-an-around",
    "title": "Should You Spend Some Of The Family'S Future Inheritance On An Around-The-World Trip Or Major Holiday For Yourself?",
    "chapter": "Spreads For Making Your Dearest Wishes And Dreams Come True",
    "purpose": "This layout is most useful when family dynamics are emotional, layered, and not easily solved by one conversation. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Are you entitled to spend your own money any way you wish?",
      "Card 2: Should you feel guilty if you follow your dream?",
      "Card 3: Will you regret it if you do not follow your dream?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Reach for it when family dynamics are emotional, layered, and not easily solved by one conversation. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 265,
    "slug": "will-you-like-a-new-prospective-family-member-when-you-meet-for-the-first-time",
    "title": "Will You Like A New Prospective Family Member When You Meet For The First Time?",
    "chapter": "Family Spreads",
    "purpose": "This 6-card spread is built for moments when family dynamics are emotional, layered, and not easily solved by one conversation. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when family dynamics are emotional, layered, and not easily solved by one conversation. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 266,
    "slug": "should-you-invite-a-particular-relative-to-a-family-gathering",
    "title": "Should You Invite A Particular Relative To A Family Gathering?",
    "chapter": "Family Spreads",
    "purpose": "Use this 3-card layout when family dynamics are emotional, layered, and not easily solved by one conversation. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Will the invitation lead to more trouble than it is worth?",
      "Card 2: If you do not invite the person, will it cause",
      "Card 2 as a tiebreaker."
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Turn to it when family dynamics are emotional, layered, and not easily solved by one conversation. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 293,
    "slug": "if-your-child-or-teenager-is-being-bullied-at-school",
    "title": "If Your Child Or Teenager Is Being Bullied At School",
    "chapter": "Spreads For Babies, Children, And Grandchildren Of All Ages",
    "purpose": "A practical 7-card spread for times when your situation involves child or teenager is being bullied at school. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
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
    "when": "Use it when your situation involves child or teenager is being bullied at school. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 294,
    "slug": "if-your-child-or-teenager-is-being-bullied-on-social-media",
    "title": "If Your Child Or Teenager Is Being Bullied On Social Media",
    "chapter": "Spreads For Babies, Children, And Grandchildren Of All Ages",
    "purpose": "This layout is most useful when friendship patterns or social distance are weighing on you. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when friendship patterns or social distance are weighing on you. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 321,
    "slug": "the-overcoming-anxiety-spread",
    "title": "The Overcoming-Anxiety Spread",
    "chapter": "Health And Healing Spreads",
    "purpose": "This 6-card spread is built for moments when fear, pressure, or social stress is shaping your choices more than you want it to. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: Is your anxiety triggered by external circumstances, or does it come from within?",
      "Card 2: Who or what situation makes it worse? Can you avoid these?",
      "Card 3: Who or what helps to calm the anxiety?",
      "Card 4: What instant strategies can you develop when you feel anxiety rising?",
      "Card 5: Would a change of lifestyle/location/career/relationship relieve the problem?",
      "Card 6: What new activity/desired situation suddenly becomes possible without the anxiety?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the six Court cards.",
    "when": "Come to this spread when fear, pressure, or social stress is shaping your choices more than you want it to. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 322,
    "slug": "will-your-health-improve",
    "title": "Will Your Health Improve?",
    "chapter": "Health And Healing Spreads",
    "purpose": "Use this 3-card layout when body confidence, wellbeing, or physical rhythm is part of the question. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Is there anything in your life/lifestyle causing undue stress?",
      "Card 2: Should you explore alternative energy therapies such as acupuncture, acupressure, reiki, kinesiology, or meditation classes to release blocks and restore energy?",
      "Card 3: Will your health improve naturally when your life is in balance?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Turn to it when body confidence, wellbeing, or physical rhythm is part of the question. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 354,
    "slug": "bringing-good-luck-into-your-life",
    "title": "Bringing Good Luck Into Your Life",
    "chapter": "Spreads For Good Luck",
    "purpose": "A practical 7-card spread for times when the theme of bringing good luck into your life is active in your life. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
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
    "when": "Use it when the theme of bringing good luck into your life is active in your life. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 355,
    "slug": "will-your-bad-luck-change-soon",
    "title": "Will Your Bad Luck Change Soon?",
    "chapter": "Spreads For Good Luck",
    "purpose": "This layout is most useful when the theme of will your bad luck change soon is active in your life. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Do you believe you are in the hands of fate? If so, is this true, or a perception?",
      "Card 2: Is anyone causing your misfortune?",
      "Card 3: Can you/how can you change your luck?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Reach for it when the theme of will your bad luck change soon is active in your life. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 382,
    "slug": "will-your-new-home-be-lucky-for-you",
    "title": "Will Your New Home Be Lucky For You?",
    "chapter": "Spreads For The Home And Property",
    "purpose": "This 4-card spread is built for moments when the theme of will your new home be lucky for you is active in your life. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: Did you feel when you first saw it that it was meant to be yours and that that was a valid feeling?",
      "Card 2: Will everything progress smoothly in negotiations/finance, etc., right through to the move?",
      "Card 3: Is this going to be a place of health, happiness, and prosperity?",
      "Card 4: Do you have any worries about the house/location and how can these be resolved?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Come to this spread when the theme of will your new home be lucky for you is active in your life. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 383,
    "slug": "will-you-ever-sell-your-home",
    "title": "Will You Ever Sell Your Home?",
    "chapter": "Spreads For The Home And Property",
    "purpose": "Use this 10-card layout when the theme of will you ever sell your home is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
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
    "when": "Turn to it when the theme of will you ever sell your home is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 411,
    "slug": "why-does-it-seem-so-hard-to-make-friends",
    "title": "Why Does It Seem So Hard To Make Friends?",
    "chapter": "Spreads For Friendships And Your Social Life",
    "purpose": "A practical 6-card spread for times when friendship patterns or social distance are weighing on you. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Are you naturally a loner who doesn't want company, but feel you ought to?",
      "Card 2: Would you like a few like-minded friends? How/where can you meet them?",
      "Card 3: If you want to socialize more, what deep down holds you back?",
      "Card 4: Should you seek friends online, enjoying online friendships rather than face-to-face?",
      "Card 5: Where should you go/what should you join/new activities to try to meet more people directly?",
      "Card 6: Are you in the wrong place/should you change jobs/relocate?"
    ],
    "use": "The full deck.",
    "when": "Use it when friendship patterns or social distance are weighing on you. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 412,
    "slug": "dealing-with-social-life-conflicts",
    "title": "Dealing With Social Life Conflicts",
    "chapter": "Spreads For Friendships And Your Social Life",
    "purpose": "This layout is most useful when friendship patterns or social distance are weighing on you. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when friendship patterns or social distance are weighing on you. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 441,
    "slug": "are-you-both-ready-for-the-life-changes-a-baby-will-bring",
    "title": "Are You Both Ready For The Life Changes A Baby Will Bring?",
    "chapter": "Spreads For Fertility, Conception, Pregnancy, And Babies",
    "purpose": "This 4-card spread is built for moments when the theme of are you both ready for the life changes a baby will bring is active in your life. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: What does your partner really feel?",
      "Card 2: What do you really feel?",
      "Card 3: Is this the right time/do you still have things to do as a couple first?",
      "Card 4: Are the advantages of having a family greater than the disadvantages?"
    ],
    "use": "The Major twenty-two cards.",
    "when": "Come to this spread when the theme of are you both ready for the life changes a baby will bring is active in your life. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 442,
    "slug": "is-my-partner-the-right-person-to-be-the-parent-of-my-child",
    "title": "Is My Partner The Right Person To Be The Parent Of My Child?",
    "chapter": "Spreads For Fertility, Conception, Pregnancy, And Babies",
    "purpose": "Use this 3-card layout when your heart is involved and you need clarity about connection, desire, or commitment. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Is s/he sufficiently mature, or does s/he need more time to grow up?",
      "Card 2: Would s/he be a loving supportive co-parent?",
      "Card 3: Should I go ahead and try for a baby with him/her, or move on to another relationship/go it alone?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Turn to it when your heart is involved and you need clarity about connection, desire, or commitment. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 467,
    "slug": "will-you-win-your-court-case",
    "title": "Will You Win Your Court Case?",
    "chapter": "Spreads For Justice, Truth, Compensation, And Inheritance",
    "purpose": "This one-card practice is for moments when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. It keeps the reading focused so one clear symbol can name the energy, lesson, or invitation most active right now.",
    "positions": [
      "Card 1: Will judgment go in your favor?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Use it when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 468,
    "slug": "is-it-more-advantageous-to-accept-an-out-of-court-settlement-or",
    "title": "Is It More Advantageous To Accept An Out-Of-Court Settlement Or To Go Ahead With The Court Case?",
    "chapter": "Spreads For Justice, Truth, Compensation, And Inheritance",
    "purpose": "This layout is most useful when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: What are the advantages of settling out of court?",
      "Card 2: What are the disadvantages of settling out of court?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Reach for it when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 493,
    "slug": "should-you-buy-a-pet",
    "title": "Should You Buy A Pet?",
    "chapter": "Spreads For Pets Large And Small",
    "purpose": "This 7-card spread is built for moments when you are weighing whether buy a pet. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when you are weighing whether buy a pet. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 494,
    "slug": "choosing-the-right-pet",
    "title": "Choosing The Right Pet",
    "chapter": "Spreads For Pets Large And Small",
    "purpose": "Use this 7-card layout when the theme of choosing the right pet is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
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
    "when": "Turn to it when the theme of choosing the right pet is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 520,
    "slug": "should-you-move-to-a-particular-neighborhood",
    "title": "Should You Move To A Particular Neighborhood?",
    "chapter": "Neighbors, Neighborhood, And Community Spreads",
    "purpose": "Use this single-card draw when you are weighing whether move to a particular neighborhood. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [
      "Card 1: Is this the right neighborhood for you? (answer depends on the strength of the positive feeling you get from the card)."
    ],
    "use": "The twenty-two Major cards.",
    "when": "Use it when you are weighing whether move to a particular neighborhood. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 521,
    "slug": "when-you-move-into-a-new-neighborhood-and-no-one-comes-to-greet-you",
    "title": "When You Move Into A New Neighborhood And No One Comes To Greet You",
    "chapter": "Neighbors, Neighborhood, And Community Spreads",
    "purpose": "This layout is most useful when when you move into a new neighborhood and no one comes to greet you. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Should you knock on a few doors to say",
      "Card 2: Should you wait for them to contact you?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Reach for it when when you move into a new neighborhood and no one comes to greet you. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 543,
    "slug": "should-you-and-your-partner-call-your-baby-the-name-you-want",
    "title": "Should You And Your Partner Call Your Baby The Name You Want, Or The One Your Families Want?",
    "chapter": "Spreads For Celebrations",
    "purpose": "This 2-card spread is built for moments when your heart is involved and you need clarity about connection, desire, or commitment. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: Should you call your baby by the name you want, one that will fit into the modern world?",
      "Card 2: Would it be possible/practical to use the desired family choice as a middle name to honor the family (and keep the peace)?"
    ],
    "use": "The forty Minor cards and the twenty-two Major cards.",
    "when": "Come to this spread when your heart is involved and you need clarity about connection, desire, or commitment. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 544,
    "slug": "how-can-you-decide-the-right-name-for-your-baby",
    "title": "How Can You Decide The Right Name For Your Baby?",
    "chapter": "Spreads For Celebrations",
    "purpose": "Use this 4-card layout when the theme of how can you decide the right name for your baby is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Will you know once your baby is born/comes home which names fit the personality?",
      "Card 2: Are the most likely names ones that will sound as good with a forty-year-old as a four-year-old?",
      "Card 3: Can you resist pressure from family to",
      "Card 3 . See which cards have the strongest positive meaning. If you need further guidance, see the Numerology Spread ("
    ],
    "use": "The full deck.",
    "when": "Turn to it when the theme of how can you decide the right name for your baby is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 566,
    "slug": "where-should-you-go-on-vacation",
    "title": "Where Should You Go On Vacation?",
    "chapter": "Spreads For Travel And Vacations",
    "purpose": "A practical 5-card spread for times when travel, distance, or relocation is part of the decision. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: What do you hope to gain most from your vacation?",
      "Card 2: What are the drawbacks of going on vacation, if any?",
      "Card 3: Is this/when is the right time to go on vacation?",
      "Card 4: Do you want to go far or near, or even vacation at home?",
      "Card 5: Will you have a happy vacation?"
    ],
    "use": "The full deck.",
    "when": "Use it when travel, distance, or relocation is part of the decision. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 567,
    "slug": "where-to-stay-when-theres-a-choice-between-two-in-any-question",
    "title": "Where To Stay When There'S A Choice Between Two In Any Question About Traveling Or Vacations",
    "chapter": "Spreads For Travel And Vacations",
    "purpose": "This one-card practice is for moments when travel, distance, or relocation is part of the decision. It keeps the reading focused so one clear symbol can name the energy, lesson, or invitation most active right now.",
    "positions": [
      "Card 1: What factors aren't yet known that might influence the benefits and drawbacks of each choice?"
    ],
    "use": "The whole deck.",
    "when": "Reach for it when travel, distance, or relocation is part of the decision. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 591,
    "slug": "if-you-face-challenges-and-obstacles-to-overcome-in-order-to-achieve-desired-change",
    "title": "If You Face Challenges And Obstacles To Overcome In Order To Achieve Desired Change",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "This 7-card spread is built for moments when you face challenges and obstacles to overcome in order to achieve desired change. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when you face challenges and obstacles to overcome in order to achieve desired change. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 592,
    "slug": "for-major-life-path-choices-and-transitions",
    "title": "For Major Life-Path Choices And Transitions",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "Use this 9-card layout when the theme of for major life path choices and transitions is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
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
    "when": "Turn to it when the theme of for major life path choices and transitions is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 593,
    "slug": "if-you-want-to-make-a-major-life-change-but-feel-stuck",
    "title": "If You Want To Make A Major Life Change But Feel Stuck",
    "chapter": "Spreads For Life Changes And Transitions, Both Natural And Planned",
    "purpose": "A practical 5-card spread for times when you want to make a major life change but feel stuck. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: What practical and underlying factors are holding you back from making those changes?",
      "Card 2: Do you really want change, or do you just feel you ought to?",
      "Card 3: Is now the right time for change? Do you have unfinished business? Are you not quite ready?",
      "Card 4: If you are patient, will outside circumstances bring the desired change?",
      "Card 5: If you go all out for change and do not let anyone or anything stand in your way, will you succeed?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Use it when you want to make a major life change but feel stuck. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 622,
    "slug": "a-fast-answer-sun-sign-spread",
    "title": "A Fast-Answer Sun Sign Spread",
    "chapter": "Astrological Spreads, Part 1",
    "purpose": "This layout is most useful when you want structured guidance around fast answer sun sign spread. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: The advantages of going ahead with what you are asking about.",
      "Card 2: The disadvantages of what you are asking about.",
      "Card 3: The outcome of acting/going forward."
    ],
    "use": "",
    "when": "Reach for it when you want structured guidance around fast answer sun sign spread. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 623,
    "slug": "the-aries-spread-of-action",
    "title": "The Aries Spread Of Action",
    "chapter": "Astrological Spreads, Part 1",
    "purpose": "This 8-card spread is built for moments when you are working with the theme of aries spread of action. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when you are working with the theme of aries spread of action. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 641,
    "slug": "the-seven-day-planet-spread",
    "title": "The Seven-Day Planet Spread",
    "chapter": "Astrological Spreads, Part 2: The Planetary Spreads",
    "purpose": "Use this 7-card layout when you are working with the theme of seven day planet spread. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
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
    "when": "Turn to it when you are working with the theme of seven day planet spread. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 642,
    "slug": "the-sun-spread-for-going-for-a-major-achievement-even-if-you",
    "title": "The Sun Spread For Going For A Major Achievement Even If You Suspect You May Be Out Of Your League",
    "chapter": "Astrological Spreads, Part 2: The Planetary Spreads",
    "purpose": "A practical 4-card spread for times when you are working with the theme of sun spread for going for a major achievement even if you suspect you may be out of your league. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Is it",
      "Card 2: What unique qualities do you have that make you stand out?",
      "Card 3: Will you succeed this time?",
      "Card 4: If not, will you know how to succeed next time you try?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Use it when you are working with the theme of sun spread for going for a major achievement even if you suspect you may be out of your league. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 657,
    "slug": "a-crescent-moon-spread-if-you-are-starting-a-new-phase-of-your-life",
    "title": "A Crescent Moon Spread If You Are Starting A New Phase Of Your Life",
    "chapter": "Moon Spreads",
    "purpose": "This layout is most useful when you want structured guidance around crescent moon spread if you are starting a new phase of your life. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: What do you hope for most from this new beginning, not just outwardly?",
      "Card 2: What are the outer and inner disadvantages/worries about this new phase?",
      "Card 3: Are you fully prepared for this new phase? What have you overlooked?",
      "Card 4: Is there anything/anyone you would like/need to take with you/leave behind?",
      "Card 5: Will your new beginning bring happiness soon, or take months?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Reach for it when you want structured guidance around crescent moon spread if you are starting a new phase of your life. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 658,
    "slug": "a-crescent-moon-spread-for-a-new-source-of-money-in-your-life-within-a-month",
    "title": "A Crescent Moon Spread For A New Source Of Money In Your Life Within A Month",
    "chapter": "Moon Spreads",
    "purpose": "This 6-card spread is built for moments when a work, money, or long-range practical decision needs a steadier reading. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: Could any of your existing sources of money offer short-term increase through extra hours/input?",
      "Card 2: Are there any sources/assets from which you could borrow extra money/sell to make up the shortfall?",
      "Card 3: Are/how are negotiations possible to take the immediate pressure off you?",
      "Card 4: Will this shortfall continue unless you find a more permanent/lucrative source of income/input?",
      "Card 5: Will there be unexpected help?",
      "Card 6: Will you get the money by the time of the next crescent moon?"
    ],
    "use": "The forty Minor cards and the sixteen Court cards.",
    "when": "Come to this spread when a work, money, or long-range practical decision needs a steadier reading. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 684,
    "slug": "a-waxing-moon-in-aries-spread-for-launching-a-self-employed-venture",
    "title": "A Waxing Moon In Aries Spread For Launching A Self-Employed Venture",
    "chapter": "Moon Zodiac Spreads",
    "purpose": "Use this 3-card layout when you want structured guidance around waxing moon in aries spread for launching a self employed venture. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: What advantages are there in your going for self-employment now?",
      "Card 2: What disadvantages are there in launching now?",
      "Card 3: Go for it, wait, or abandon the idea?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Turn to it when you want structured guidance around waxing moon in aries spread for launching a self employed venture. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 685,
    "slug": "a-full-moon-in-aries-spread-for-independence-from-an-over-possessive",
    "title": "A Full Moon In Aries Spread For Independence From An Over-Possessive Or Dominant Family",
    "chapter": "Moon Zodiac Spreads",
    "purpose": "A practical 8-card spread for times when family dynamics are emotional, layered, and not easily solved by one conversation. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
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
    "when": "Use it when family dynamics are emotional, layered, and not easily solved by one conversation. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 720,
    "slug": "a-new-moon-angel-spread-for-returning-to-life-after-hurt-betrayal-loss-or-illness",
    "title": "A New Moon-Angel Spread For Returning To Life After Hurt, Betrayal, Loss, Or Illness",
    "chapter": "Moon-Angel Spreads",
    "purpose": "This layout is most useful when grief, mourning, or the search for meaning after loss is active. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
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
    "when": "Reach for it when grief, mourning, or the search for meaning after loss is active. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 721,
    "slug": "a-crescent-moon-angel-spread-for-new-beginnings-in-any-part-of",
    "title": "A Crescent-Moon Angel Spread For New Beginnings In Any Part Of Your Life If You Are Unsure",
    "chapter": "Moon-Angel Spreads",
    "purpose": "This 7-card spread is built for moments when you want structured guidance around crescent moon angel spread for new beginnings in any part of your life if you are unsure. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when you want structured guidance around crescent moon angel spread for new beginnings in any part of your life if you are unsure. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 741,
    "slug": "a-guardian-angel-spread-if-you-are-feeling-alone-or-afraid",
    "title": "A Guardian-Angel Spread If You Are Feeling Alone Or Afraid",
    "chapter": "Angel And Archangel Spreads",
    "purpose": "Use this 6-card layout when you want structured guidance around guardian angel spread if you are feeling alone or afraid. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: How can you feel the presence of your guardian angel in your life at this time?",
      "Card 2: What sign in the everyday world can your angel reveal so you know you are not alone?",
      "Card 3: What is the help you most need from your angel, rather than what you think you need?",
      "Card 4: Will earthly help/support come to you?",
      "Card 5: How can you most help yourself?",
      "Card 6: What special blessings will your angel bring into your life?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Turn to it when you want structured guidance around guardian angel spread if you are feeling alone or afraid. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 742,
    "slug": "an-archangel-sachiel-spread-for-a-permanent-job-if-you-can-only-get-temporary-work",
    "title": "An Archangel Sachiel Spread For A Permanent Job If You Can Only Get Temporary Work",
    "chapter": "Angel And Archangel Spreads",
    "purpose": "A practical 5-card spread for times when a work, money, or long-range practical decision needs a steadier reading. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Will your current workplace offer more permanent employment if you ask?",
      "Card 2: Is there one particular place you have recently worked where you did especially well that would put you on a future vacancy list?",
      "Card 3: Is there an extra qualification/expertise that would make it easier to get a permanent job?",
      "Card 4: What special help would you ask of Archangel Sachiel to open the right doors to permanent employment?",
      "Card 5: Will you succeed?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Use it when a work, money, or long-range practical decision needs a steadier reading. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 773,
    "slug": "spread-of-the-fool-inner-child-if-you-seek-a-new-beginning",
    "title": "Spread Of The Fool/Inner Child If You Seek A New Beginning",
    "chapter": "Crystal Tarot Spreads",
    "purpose": "Use this single-card draw when the theme of spread of the fool inner child if you seek a new beginning is active in your life. Its power comes from simplicity: one card, one honest question, and one message you can carry straight into the day.",
    "positions": [
      "Card 1: What will be the results of your new beginning?"
    ],
    "use": "",
    "when": "Reach for it when the theme of spread of the fool inner child if you seek a new beginning is active in your life. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 774,
    "slug": "spread-of-the-magician-for-the-success-of-an-entrepreneurial-venture",
    "title": "Spread Of The Magician For The Success Of An Entrepreneurial Venture",
    "chapter": "Crystal Tarot Spreads",
    "purpose": "A one-card spread for times when the theme of spread of the magician for the success of an entrepreneurial venture is active in your life. Instead of multiplying possibilities, it asks the deck to speak with precision and economy.",
    "positions": [
      "Card 1: Will your venture succeed immediately/take longer to evolve?"
    ],
    "use": "",
    "when": "Come to this spread when the theme of spread of the magician for the success of an entrepreneurial venture is active in your life. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 796,
    "slug": "a-four-winds-spread-of-fate",
    "title": "A Four-Winds Spread Of Fate",
    "chapter": "Spreads For Foretelling Your Destiny",
    "purpose": "Use this 5-card layout when you want structured guidance around four winds spread of fate. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Boreas, the North Wind, the actual situation/the most likely effects if nothing changes/you do nothing.",
      "Card 2: Eurus, the East Wind, logically what can be done to positively affect matters.",
      "Card 3: Notus, the South Wind, what unexpected boost or mitigation exists of the situation from outside sources.",
      "Card 4: Zephyrus, the West Wind, what might blow you off course?",
      "Card 5: The result of all these factors coming together."
    ],
    "use": "The full deck.",
    "when": "Turn to it when you want structured guidance around four winds spread of fate. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 797,
    "slug": "the-ring-of-fate-pendulum-spread-for-asking-a-specific-question-about",
    "title": "The Ring-Of-Fate Pendulum Spread For Asking A Specific Question About An Unknown Aspect Of Your Future",
    "chapter": "Spreads For Foretelling Your Destiny",
    "purpose": "A practical 6-card spread for times when you are working with the theme of ring of fate pendulum spread for asking a specific question about an unknown aspect of your future. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [],
    "use": "The twenty-two Major cards.",
    "when": "Use it when you are working with the theme of ring of fate pendulum spread for asking a specific question about an unknown aspect of your future. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 820,
    "slug": "the-coming-into-balance-spread",
    "title": "The Coming-Into-Balance Spread",
    "chapter": "Spreads For Self-Awareness And Knowledge And Planning Your Life Path",
    "purpose": "This layout is most useful when you are working with the theme of coming into balance spread. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: What/who really caused/is causing the chaos?",
      "Card 2: Should you intervene, or wait for things to settle?",
      "Card 3: Who/what will prove most helpful in bringing peace to the situation?",
      "Card 4: How can you restore your own balance if others' behaviors are shaking it?",
      "Card 5: How can you prevent others' future chaos affecting your lasting harmony?"
    ],
    "use": "The twenty-two Major cards.",
    "when": "Reach for it when you are working with the theme of coming into balance spread. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 821,
    "slug": "the-hidden-self-spread",
    "title": "The Hidden-Self Spread",
    "chapter": "Spreads For Self-Awareness And Knowledge And Planning Your Life Path",
    "purpose": "This 3-card spread is built for moments when you are working with the theme of hidden self spread. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: How you are seen by the world.",
      "Card 2: The hidden self the world never sees.",
      "Card 3: How you can combine the two, so you feel at home in the world without becoming too vulnerable."
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Come to this spread when you are working with the theme of hidden self spread. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 848,
    "slug": "visualizing-your-chosen-card-in-your-minds-eye-for-an-in-depth",
    "title": "Visualizing Your Chosen Card In Your Mind'S Eye For An In-Depth Understanding Into The Card'S Relevance To Your Life",
    "chapter": "Combining Tarot Spreads And Psychic Powers",
    "purpose": "Use this 6-card layout when the theme of visualizing your chosen card in your mind s eye for an in depth understanding into the card s relevance to your life is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [],
    "use": "Twenty-two Major cards and thirty-six Minor cards, Twos to Tens (Aces aren't detailed enough).",
    "when": "Turn to it when the theme of visualizing your chosen card in your mind s eye for an in depth understanding into the card s relevance to your life is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 849,
    "slug": "a-tarot-spread-using-automatic-writing",
    "title": "A Tarot Spread Using Automatic Writing",
    "chapter": "Combining Tarot Spreads And Psychic Powers",
    "purpose": "A practical 6-card spread for times when you want the reading to reach hidden, symbolic, or intuitive layers of the question. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [],
    "use": "The full deck.",
    "when": "Use it when you want the reading to reach hidden, symbolic, or intuitive layers of the question. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 870,
    "slug": "a-four-seasons-spread",
    "title": "A Four-Seasons Spread",
    "chapter": "Spreads For Festivals And Seasons",
    "purpose": "This layout is most useful when you want to read a longer cycle rather than a single event. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Spring: What is growing/needs to grow in your life?",
      "Card 2: Summer: How can you best gain recognition/rewards for your efforts?",
      "Card 3: Fall: What has worked well and will continue to flourish in your life?",
      "Card 4: Winter: What needs preserving for longer-term results, and what to let go?",
      "Card 5: Which will be my best season in the year ahead?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Reach for it when you want to read a longer cycle rather than a single event. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 871,
    "slug": "a-month-by-month-spread-for-taking-advantage-of-the-underlying-energies",
    "title": "A Month-By-Month Spread For Taking Advantage Of The Underlying Energies Of Each Month",
    "chapter": "Spreads For Festivals And Seasons",
    "purpose": "This 12-card spread is built for moments when you want to read a longer cycle rather than a single event. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when you want to read a longer cycle rather than a single event. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 896,
    "slug": "a-st-joan-of-arc-spread-for-deciding-whether-to-continue-to",
    "title": "A St.-Joan-Of-Arc Spread For Deciding Whether To Continue To Seek Justice Or Accept A Compromise",
    "chapter": "Tarot Spreads And The Saints",
    "purpose": "Use this 5-card layout when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: If you carry on to the bitter end and win, will you recoup your expenses and more and be vindicated?",
      "Card 2: If you lose the case, will you suffer a severe financial loss because of court costs?",
      "Card 3: Should you transfer to a no-win/no-fee lawyer (also known as a contingency fee agreement), or do you want to stay with the lawyer you know and trust even if they do not work on a no-win/no-fee arrangement?",
      "Card 4: If partial compensation can be negotiated outside court, would that be enough to prove to the world that you were in the right?",
      "Card 5: Should you risk all?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Turn to it when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 897,
    "slug": "a-st-martha-dragon-slaying-spread-for-dealing-with-a-difficult-relative",
    "title": "A St.-Martha-Dragon-Slaying Spread For Dealing With A Difficult Relative Without Causing A Major Family Rift",
    "chapter": "Tarot Spreads And The Saints",
    "purpose": "A practical 3-card spread for times when family dynamics are emotional, layered, and not easily solved by one conversation. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Can/should you deal with the underlying unhappiness that is causing the problem, or try to resolve it once and for all?",
      "Card 2: Is anybody causing trouble behind the scenes and offloading the blame?",
      "Card 3: Is this a long-standing problem that can only have a temporary fix to avoid immediate disruption?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Use it when family dynamics are emotional, layered, and not easily solved by one conversation. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 921,
    "slug": "the-sports-and-fitness-spread",
    "title": "The Sports-And-Fitness Spread",
    "chapter": "The Go-For-It Spreads: Health, Fitness, Leisure, And Sports",
    "purpose": "This layout is most useful when body confidence, wellbeing, or physical rhythm is part of the question. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Should you undertake serious training with the aim of turning professional?",
      "Card 2: Would you be happier just getting fit or joining a team for pleasure?",
      "Card 3: Would gentle exercise for personal satisfaction and health be just one part of your many wider interests or occupations?",
      "Card 4: If you go for the top, will you succeed totally/partly/be happy?"
    ],
    "use": "The full deck.",
    "when": "Reach for it when body confidence, wellbeing, or physical rhythm is part of the question. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 922,
    "slug": "if-you-are-worried-about-the-way-other-people-perceive-your-appearance",
    "title": "If You Are Worried About The Way Other People Perceive Your Appearance And Feel Getting Fit Will Help",
    "chapter": "The Go-For-It Spreads: Health, Fitness, Leisure, And Sports",
    "purpose": "This 7-card spread is built for moments when body confidence, wellbeing, or physical rhythm is part of the question. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
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
    "when": "Come to this spread when body confidence, wellbeing, or physical rhythm is part of the question. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 951,
    "slug": "breaking-down-the-walls-that-stop-you-seeking-an-alternative-lifestyle",
    "title": "Breaking Down The Walls That Stop You Seeking An Alternative Lifestyle",
    "chapter": "Spreads For Alternative Lifestyles, Doing Your Own Thing, And Living Your Own Way",
    "purpose": "Use this 5-card layout when the theme of breaking down the walls that stop you seeking an alternative lifestyle is active in your life. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: The barriers of convention that may still hold you back through the disapproval of others and all those old voices from childhood.",
      "Card 2: The wall of economic stability: How you would manage financially if you gave up your steady day job to earn money based on your initiative and ingenuity.",
      "Card 3: The hidden fear: What has sometimes held you back because it hasn't been examined and faced or overcome.",
      "Card 4: The practical organization, selling up and finding somewhere new to live, maybe not even a house but a boat or recreational vehicle, where to go, what if you fall ill.",
      "Card 5: The way of freedom."
    ],
    "use": "The full deck.",
    "when": "Turn to it when the theme of breaking down the walls that stop you seeking an alternative lifestyle is active in your life. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 952,
    "slug": "if-you-are-offered-a-run-down-animal-sanctuary-or-indigenous-wildlife-center",
    "title": "If You Are Offered A Run-Down Animal Sanctuary Or Indigenous Wildlife Center",
    "chapter": "Spreads For Alternative Lifestyles, Doing Your Own Thing, And Living Your Own Way",
    "purpose": "A practical 4-card spread for times when a meaningful life change feels exciting but also logistically demanding. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
    "positions": [
      "Card 1: Could/should you take it over even though it would need time and resources to get it up and running?",
      "Card 2: Would it be better to turn the offer down and look for land/buildings suitable for conversion to fulfill your own blueprint?",
      "Card 3: Should you accept but keep your day job/give yourself a time limit to make it a viable enterprise?",
      "Card 4: Will your dreams of saving wildlife materialize?"
    ],
    "use": "The forty Minor cards, Aces to Tens.",
    "when": "Use it when a meaningful life change feels exciting but also logistically demanding. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 976,
    "slug": "when-a-relationship-is-all-about-sex-and-not-about-love",
    "title": "When A Relationship Is All About Sex And Not About Love",
    "chapter": "Passion And Temptation Spreads",
    "purpose": "This layout is most useful when your heart is involved and you need clarity about connection, desire, or commitment. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1: Are you happy with this arrangement for now/for the foreseeable future?",
      "Card 2: Do you want to spend time together/go on vacation, but your partner is not free?",
      "Card 3: Are you ready to risk the relationship by asking for more?",
      "Card 4: Are you outgrowing the relationship as fun but going nowhere?"
    ],
    "use": "The sixteen Court cards.",
    "when": "Reach for it when your heart is involved and you need clarity about connection, desire, or commitment. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
  },
  {
    "number": 977,
    "slug": "if-your-new-love-is-giving-mixed-messages-about-lovemaking",
    "title": "If Your New Love Is Giving Mixed Messages About Lovemaking",
    "chapter": "Passion And Temptation Spreads",
    "purpose": "This 6-card spread is built for moments when your heart is involved and you need clarity about connection, desire, or commitment. It separates the question into readable parts so the cards can show motive, pressure, and likely direction instead of offering a flat yes-or-no.",
    "positions": [
      "Card 1: Is your new love generally shy/finds it hard to show affection?",
      "Card 2: Has your love come out of a bad",
      "Card 3: Should you take the initiative?",
      "Card 4: Should you arrange a weekend vacation where it's obvious that you are sharing a room?",
      "Card 5: Should you talk about the subject generally, or would that send him/her heading for the hills fast?",
      "Card 6: If the relationship is otherwise good and sex is seen as a serious step to commitment by your partner, should you wait until your partner is ready?"
    ],
    "use": "The forty Minor cards, Aces to Tens, and the sixteen Court cards.",
    "when": "Come to this spread when your heart is involved and you need clarity about connection, desire, or commitment. It works best when you can stay with every position long enough to hear the full message."
  },
  {
    "number": 989,
    "slug": "when-a-relative-or-close-friend-dies-in-an-accident",
    "title": "When A Relative Or Close Friend Dies In An Accident",
    "chapter": "Spreads For Grief And Loss",
    "purpose": "Use this 6-card layout when friendship patterns or social distance are weighing on you. It gives the reading enough room to reveal what is driving the situation, what deserves attention first, and where the energy is trying to move.",
    "positions": [
      "Card 1: Do you have closure why/how the accident happened/justice against anyone to blame?",
      "Card 2: If not, can this/how can justice/closure be obtained, if necessary by increasing pressure for justice/an official inquiry?",
      "Card 3: How can you best remember the person at their most vibrant/collect memories in recordings/videos/photographs or a memory book so younger and future family members will know them?",
      "Card 4: What kind of a memorial would your relative have liked/at the place of the accident/in a favorite spot/a prize or trophy in their honor?",
      "Card 5: What can be done to campaign to prevent similar accidents/if, for example, it was a dangerous stretch of road or lack of safety measures in the workplace?",
      "Card 6: What can you do in your life that they planned to do in order to fulfill their wishes?"
    ],
    "use": "The twenty-two Major cards and the sixteen Court cards.",
    "when": "Turn to it when friendship patterns or social distance are weighing on you. Leave enough space afterward to notice what the cards are saying together, not just one by one."
  },
  {
    "number": 990,
    "slug": "when-a-relative-suffers-a-mysterious-death-and-you-cannot-get-justice",
    "title": "When A Relative Suffers A Mysterious Death And You Cannot Get Justice",
    "chapter": "Spreads For Grief And Loss",
    "purpose": "A practical 7-card spread for times when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. Rather than rushing to a verdict, it lets the cards map the deeper pattern underneath the question.",
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
    "when": "Use it when you need a steadier reading on justice, fairness, and what the cost of pursuing truth may be. Give yourself enough quiet to read the spread as a pattern rather than as isolated card meanings."
  },
  {
    "number": 1001,
    "slug": "your-personal-year-ahead-spread",
    "title": "Your Personal-Year-Ahead Spread",
    "chapter": "Spread 1001",
    "purpose": "This layout is most useful when you want to review the year ahead in a broad, structured way. Its strength is that it slows the reading down and makes each layer of the story easier to see clearly.",
    "positions": [
      "Card 1 that remains is your overall year theme;",
      "Card 2 is what is unexpected in the year ahead;",
      "Card 3 is a particular opportunity the year will bring; and",
      "Card 4 is the challenges to be overcome in the year ahead."
    ],
    "use": "Use the full deck, removing the Death and Devil cards before laying out the year review.",
    "when": "Reach for it when you want to review the year ahead in a broad, structured way. The reading becomes stronger when you can sit with the whole layout instead of chasing only the first dramatic answer."
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
    "upright": "Upright, Ace of Wands brings the first opening of the suit into contact with fire, appetite, and forward motion. The reading strengthens when you let the suit behave exactly as it is built to behave. With Ace of Wands, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Ace of Wands reversed suggests an opening that is present but not yet trusted under strain within impulse, frustration, and misdirected heat. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Ace of Wands, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "For relationships, Ace of Wands speaks to a beginning that changes the emotional tone between people within the field of desire, attraction, and chemistry. With Ace of Wands, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "Ace of Wands around career matters often reveals an opening, initiative, or first spark of possibility inside ambition, leadership, and enterprise. Ace of Wands often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "In health readings, Ace of Wands can describe a fresh chance to reset the body's direction around stamina, motivation, and burnout risk. The body-level lesson of Ace of Wands often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Ace of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-wands",
    "name": "Two of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "02",
    "upright": "Two of Wands upright shows a living balance between two forces working through fire, appetite, and forward motion. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Two of Wands is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Two of Wands shows indecision or imbalance between competing pulls getting tangled in the shadow side of impulse, frustration, and misdirected heat. Read it as a signal to reset the pace before the pattern hardens further. Two of Wands rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "Two of Wands in a love reading highlights mutual choice and the need to meet each other halfway shaped by desire, attraction, and chemistry. Two of Wands rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "In career readings, Two of Wands brings attention to competing priorities that need balancing or choosing within ambition, leadership, and enterprise. The work message in Two of Wands sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "For wellbeing, Two of Wands often reflects the need to rebalance two demands pulling on the system linked to stamina, motivation, and burnout risk. With Two of Wands, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Two of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-wands",
    "name": "Three of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "03",
    "upright": "Three of Wands upright highlights early growth that needs cooperation to flourish through fire, appetite, and forward motion. It reads best when you treat the card as a live pattern rather than a decorative mood. Three of Wands becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Three of Wands points to growth complicated by mixed signals or weak coordination running into difficulty inside impulse, frustration, and misdirected heat. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Three of Wands usually loosens once the suit is handled with less force and more accuracy.",
    "love": "In love, Three of Wands often reflects third influences, celebration, or the first visible growth of a bond around desire, attraction, and chemistry. Three of Wands usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "For work and money, Three of Wands points to teamwork, apprenticeship, and early proof of progress expressed through ambition, leadership, and enterprise. With Three of Wands, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "Three of Wands in a health context points toward supportive routines that grow stronger through cooperation affecting stamina, motivation, and burnout risk. Three of Wands asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Three of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-wands",
    "name": "Four of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "04",
    "upright": "When Four of Wands appears upright, a bid for stability that can either steady or stiffen meets fire, appetite, and forward motion in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Four of Wands instead of resisting it.",
    "reversed": "When Four of Wands turns reversed, stability turning into stagnation, defensiveness, or over-control becomes harder to handle cleanly through impulse, frustration, and misdirected heat. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Four of Wands improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "For relationships, Four of Wands speaks to the tension between safety and emotional aliveness within the field of desire, attraction, and chemistry. The lesson of Four of Wands in love is easier to read in timing and tone than in declarations alone.",
    "career": "Four of Wands around career matters often reveals holding ground, consolidating gains, or resisting change inside ambition, leadership, and enterprise. Four of Wands says as much about how you are working as about what you are working on.",
    "health": "In health readings, Four of Wands can describe the body's wish to stabilise, rest, or guard resources around stamina, motivation, and burnout risk. Four of Wands is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Four of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-wands",
    "name": "Five of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "05",
    "upright": "Upright, Five of Wands brings friction that demands adjustment into contact with fire, appetite, and forward motion. The reading strengthens when you let the suit behave exactly as it is built to behave. With Five of Wands, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Five of Wands reversed suggests conflict that is no longer productive under strain within impulse, frustration, and misdirected heat. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Five of Wands, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "Five of Wands in a love reading highlights conflict, mismatch, or the need to renegotiate expectations shaped by desire, attraction, and chemistry. With Five of Wands, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "In career readings, Five of Wands brings attention to pressure, rivalry, or a correction forced by friction within ambition, leadership, and enterprise. Five of Wands often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "For wellbeing, Five of Wands often reflects stress signals that show something must change linked to stamina, motivation, and burnout risk. The body-level lesson of Five of Wands often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Five of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-wands",
    "name": "Six of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "06",
    "upright": "Six of Wands upright shows movement that restores rhythm or support working through fire, appetite, and forward motion. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Six of Wands is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Six of Wands shows support that is uneven, delayed, or taken for granted getting tangled in the shadow side of impulse, frustration, and misdirected heat. Read it as a signal to reset the pace before the pattern hardens further. Six of Wands rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "In love, Six of Wands often reflects repair, reassurance, or an easier flow returning around desire, attraction, and chemistry. Six of Wands rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "For work and money, Six of Wands points to recognition, support, or movement after a stuck phase expressed through ambition, leadership, and enterprise. The work message in Six of Wands sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "Six of Wands in a health context points toward improvement, relief, or recovery aided by support affecting stamina, motivation, and burnout risk. With Six of Wands, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Six of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-wands",
    "name": "Seven of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "07",
    "upright": "Seven of Wands upright highlights a test of judgment, courage, or strategy through fire, appetite, and forward motion. It reads best when you treat the card as a live pattern rather than a decorative mood. Seven of Wands becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Seven of Wands points to strategy slipping into suspicion, fatigue, or second-guessing running into difficulty inside impulse, frustration, and misdirected heat. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Seven of Wands usually loosens once the suit is handled with less force and more accuracy.",
    "love": "For relationships, Seven of Wands speaks to tests of trust, discernment, or loyalty within the field of desire, attraction, and chemistry. Seven of Wands usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "Seven of Wands around career matters often reveals strategy, caution, and the need to read the field accurately inside ambition, leadership, and enterprise. With Seven of Wands, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "In health readings, Seven of Wands can describe trial, patience, and reading what the body is really asking for around stamina, motivation, and burnout risk. Seven of Wands asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Seven of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-wands",
    "name": "Eight of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "08",
    "upright": "When Eight of Wands appears upright, repetition that becomes momentum or skill meets fire, appetite, and forward motion in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Eight of Wands instead of resisting it.",
    "reversed": "When Eight of Wands turns reversed, momentum becoming compulsion, pressure, or tunnel vision becomes harder to handle cleanly through impulse, frustration, and misdirected heat. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Eight of Wands improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "Eight of Wands in a love reading highlights patterns that intensify quickly and reveal what each person keeps repeating shaped by desire, attraction, and chemistry. The lesson of Eight of Wands in love is easier to read in timing and tone than in declarations alone.",
    "career": "In career readings, Eight of Wands brings attention to skill-building, output, and disciplined repetition within ambition, leadership, and enterprise. Eight of Wands says as much about how you are working as about what you are working on.",
    "health": "For wellbeing, Eight of Wands often reflects habit, repetition, and the cumulative effect of small actions linked to stamina, motivation, and burnout risk. Eight of Wands is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Eight of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-wands",
    "name": "Nine of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "09",
    "upright": "Upright, Nine of Wands brings a late-stage lesson that asks for resilience into contact with fire, appetite, and forward motion. The reading strengthens when you let the suit behave exactly as it is built to behave. With Nine of Wands, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Nine of Wands reversed suggests resilience fraying under accumulated strain under strain within impulse, frustration, and misdirected heat. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Nine of Wands, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "In love, Nine of Wands often reflects private hopes and guarded fears coming to the surface around desire, attraction, and chemistry. With Nine of Wands, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "For work and money, Nine of Wands points to results earned through endurance and late-stage refinement expressed through ambition, leadership, and enterprise. Nine of Wands often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "Nine of Wands in a health context points toward resilience tested by fatigue, overvigilance, or lingering strain affecting stamina, motivation, and burnout risk. The body-level lesson of Nine of Wands often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Nine of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-wands",
    "name": "Ten of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "10",
    "upright": "Ten of Wands upright shows the full weight and consequence of the suit working through fire, appetite, and forward motion. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Ten of Wands is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Ten of Wands shows burden, excess, or the painful end state of the suit getting tangled in the shadow side of impulse, frustration, and misdirected heat. Read it as a signal to reset the pace before the pattern hardens further. Ten of Wands rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "For relationships, Ten of Wands speaks to the long-term consequences of how love has been built within the field of desire, attraction, and chemistry. Ten of Wands rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "Ten of Wands around career matters often reveals a peak responsibility, heavy load, or culmination with consequences inside ambition, leadership, and enterprise. The work message in Ten of Wands sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "In health readings, Ten of Wands can describe the point where load, symptoms, or consequences can no longer be ignored around stamina, motivation, and burnout risk. With Ten of Wands, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Ten of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-wands",
    "name": "Page of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "page",
    "upright": "Page of Wands upright highlights a message, mood, or beginner's encounter with the suit through fire, appetite, and forward motion. It reads best when you treat the card as a live pattern rather than a decorative mood. Page of Wands becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Page of Wands points to immaturity, avoidance, or a message that is not yet fully understood running into difficulty inside impulse, frustration, and misdirected heat. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Page of Wands usually loosens once the suit is handled with less force and more accuracy.",
    "love": "Page of Wands in a love reading highlights curiosity, flirtation, and a new emotional message shaped by desire, attraction, and chemistry. Page of Wands usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "In career readings, Page of Wands brings attention to news, learning, and the entry-level form of the suit's lesson within ambition, leadership, and enterprise. With Page of Wands, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "For wellbeing, Page of Wands often reflects sensitivity, early messages, and the need to listen sooner linked to stamina, motivation, and burnout risk. Page of Wands asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Page of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-wands",
    "name": "Knight of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "knight",
    "upright": "When Knight of Wands appears upright, the suit in motion, pursuit, and active expression meets fire, appetite, and forward motion in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Knight of Wands instead of resisting it.",
    "reversed": "When Knight of Wands turns reversed, energy that outruns wisdom, timing, or emotional intelligence becomes harder to handle cleanly through impulse, frustration, and misdirected heat. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Knight of Wands improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "In love, Knight of Wands often reflects active pursuit, urgency, and the style in which affection is expressed around desire, attraction, and chemistry. The lesson of Knight of Wands in love is easier to read in timing and tone than in declarations alone.",
    "career": "For work and money, Knight of Wands points to the way ambition advances, pursues, or pushes expressed through ambition, leadership, and enterprise. Knight of Wands says as much about how you are working as about what you are working on.",
    "health": "Knight of Wands in a health context points toward how energy is being spent, pushed, or driven affecting stamina, motivation, and burnout risk. Knight of Wands is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Knight of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-wands",
    "name": "Queen of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "queen",
    "upright": "Upright, Queen of Wands brings embodied mastery of the suit from the inside out into contact with fire, appetite, and forward motion. The reading strengthens when you let the suit behave exactly as it is built to behave. With Queen of Wands, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Queen of Wands reversed suggests inner authority disturbed by self-doubt, overprotection, or emotional leakage under strain within impulse, frustration, and misdirected heat. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Queen of Wands, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "For relationships, Queen of Wands speaks to emotional maturity and how love is held in the inner life within the field of desire, attraction, and chemistry. With Queen of Wands, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "Queen of Wands around career matters often reveals quiet competence, stewardship, and mature command of the craft inside ambition, leadership, and enterprise. Queen of Wands often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "In health readings, Queen of Wands can describe regulation through self-knowledge, embodied care, and pacing around stamina, motivation, and burnout risk. The body-level lesson of Queen of Wands often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Queen of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-wands",
    "name": "King of Wands",
    "arcana": "minor",
    "suit": "wands",
    "rank": "king",
    "upright": "King of Wands upright shows directed command of the suit and its responsibilities working through fire, appetite, and forward motion. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. King of Wands is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed King of Wands shows control problems, rigidity, or leadership without balance getting tangled in the shadow side of impulse, frustration, and misdirected heat. Read it as a signal to reset the pace before the pattern hardens further. King of Wands rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "King of Wands in a love reading highlights commitment, direction, and the standards guiding the bond shaped by desire, attraction, and chemistry. King of Wands rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "In career readings, King of Wands brings attention to decision-making authority, executive pressure, and long-view leadership within ambition, leadership, and enterprise. The work message in King of Wands sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "For wellbeing, King of Wands often reflects the discipline required to protect long-term strength linked to stamina, motivation, and burnout risk. With King of Wands, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "King of Wands uses the imagery of wands, sprouting wood, and flames point to drive and life force while the rank emphasises leadership, direction, and mature command."
  },
  {
    "slug": "ace-of-cups",
    "name": "Ace of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "ace",
    "upright": "Ace of Cups upright highlights the first opening of the suit through emotion, receptivity, and relational flow. It reads best when you treat the card as a live pattern rather than a decorative mood. Ace of Cups becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Ace of Cups points to an opening that is present but not yet trusted running into difficulty inside flooded feeling, emotional avoidance, or unclear receptivity. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Ace of Cups usually loosens once the suit is handled with less force and more accuracy.",
    "love": "In love, Ace of Cups often reflects a beginning that changes the emotional tone between people around emotion, intimacy, and receptivity. Ace of Cups usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "For work and money, Ace of Cups points to an opening, initiative, or first spark of possibility expressed through team harmony, creative work, and morale. With Ace of Cups, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "Ace of Cups in a health context points toward a fresh chance to reset the body's direction affecting nervous-system sensitivity and emotional wellbeing. Ace of Cups asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Ace of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-cups",
    "name": "Two of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "02",
    "upright": "When Two of Cups appears upright, a living balance between two forces meets emotion, receptivity, and relational flow in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Two of Cups instead of resisting it.",
    "reversed": "When Two of Cups turns reversed, indecision or imbalance between competing pulls becomes harder to handle cleanly through flooded feeling, emotional avoidance, or unclear receptivity. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Two of Cups improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "For relationships, Two of Cups speaks to mutual choice and the need to meet each other halfway within the field of emotion, intimacy, and receptivity. The lesson of Two of Cups in love is easier to read in timing and tone than in declarations alone.",
    "career": "Two of Cups around career matters often reveals competing priorities that need balancing or choosing inside team harmony, creative work, and morale. Two of Cups says as much about how you are working as about what you are working on.",
    "health": "In health readings, Two of Cups can describe the need to rebalance two demands pulling on the system around nervous-system sensitivity and emotional wellbeing. Two of Cups is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Two of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-cups",
    "name": "Three of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "03",
    "upright": "Upright, Three of Cups brings early growth that needs cooperation to flourish into contact with emotion, receptivity, and relational flow. The reading strengthens when you let the suit behave exactly as it is built to behave. With Three of Cups, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Three of Cups reversed suggests growth complicated by mixed signals or weak coordination under strain within flooded feeling, emotional avoidance, or unclear receptivity. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Three of Cups, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "Three of Cups in a love reading highlights third influences, celebration, or the first visible growth of a bond shaped by emotion, intimacy, and receptivity. With Three of Cups, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "In career readings, Three of Cups brings attention to teamwork, apprenticeship, and early proof of progress within team harmony, creative work, and morale. Three of Cups often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "For wellbeing, Three of Cups often reflects supportive routines that grow stronger through cooperation linked to nervous-system sensitivity and emotional wellbeing. The body-level lesson of Three of Cups often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Three of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-cups",
    "name": "Four of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "04",
    "upright": "Four of Cups upright shows a bid for stability that can either steady or stiffen working through emotion, receptivity, and relational flow. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Four of Cups is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Four of Cups shows stability turning into stagnation, defensiveness, or over-control getting tangled in the shadow side of flooded feeling, emotional avoidance, or unclear receptivity. Read it as a signal to reset the pace before the pattern hardens further. Four of Cups rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "In love, Four of Cups often reflects the tension between safety and emotional aliveness around emotion, intimacy, and receptivity. Four of Cups rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "For work and money, Four of Cups points to holding ground, consolidating gains, or resisting change expressed through team harmony, creative work, and morale. The work message in Four of Cups sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "Four of Cups in a health context points toward the body's wish to stabilise, rest, or guard resources affecting nervous-system sensitivity and emotional wellbeing. With Four of Cups, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Four of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-cups",
    "name": "Five of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "05",
    "upright": "Five of Cups upright highlights friction that demands adjustment through emotion, receptivity, and relational flow. It reads best when you treat the card as a live pattern rather than a decorative mood. Five of Cups becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Five of Cups points to conflict that is no longer productive running into difficulty inside flooded feeling, emotional avoidance, or unclear receptivity. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Five of Cups usually loosens once the suit is handled with less force and more accuracy.",
    "love": "For relationships, Five of Cups speaks to conflict, mismatch, or the need to renegotiate expectations within the field of emotion, intimacy, and receptivity. Five of Cups usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "Five of Cups around career matters often reveals pressure, rivalry, or a correction forced by friction inside team harmony, creative work, and morale. With Five of Cups, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "In health readings, Five of Cups can describe stress signals that show something must change around nervous-system sensitivity and emotional wellbeing. Five of Cups asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Five of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-cups",
    "name": "Six of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "06",
    "upright": "When Six of Cups appears upright, movement that restores rhythm or support meets emotion, receptivity, and relational flow in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Six of Cups instead of resisting it.",
    "reversed": "When Six of Cups turns reversed, support that is uneven, delayed, or taken for granted becomes harder to handle cleanly through flooded feeling, emotional avoidance, or unclear receptivity. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Six of Cups improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "Six of Cups in a love reading highlights repair, reassurance, or an easier flow returning shaped by emotion, intimacy, and receptivity. The lesson of Six of Cups in love is easier to read in timing and tone than in declarations alone.",
    "career": "In career readings, Six of Cups brings attention to recognition, support, or movement after a stuck phase within team harmony, creative work, and morale. Six of Cups says as much about how you are working as about what you are working on.",
    "health": "For wellbeing, Six of Cups often reflects improvement, relief, or recovery aided by support linked to nervous-system sensitivity and emotional wellbeing. Six of Cups is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Six of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-cups",
    "name": "Seven of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "07",
    "upright": "Upright, Seven of Cups brings a test of judgment, courage, or strategy into contact with emotion, receptivity, and relational flow. The reading strengthens when you let the suit behave exactly as it is built to behave. With Seven of Cups, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Seven of Cups reversed suggests strategy slipping into suspicion, fatigue, or second-guessing under strain within flooded feeling, emotional avoidance, or unclear receptivity. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Seven of Cups, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "In love, Seven of Cups often reflects tests of trust, discernment, or loyalty around emotion, intimacy, and receptivity. With Seven of Cups, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "For work and money, Seven of Cups points to strategy, caution, and the need to read the field accurately expressed through team harmony, creative work, and morale. Seven of Cups often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "Seven of Cups in a health context points toward trial, patience, and reading what the body is really asking for affecting nervous-system sensitivity and emotional wellbeing. The body-level lesson of Seven of Cups often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Seven of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-cups",
    "name": "Eight of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "08",
    "upright": "Eight of Cups upright shows repetition that becomes momentum or skill working through emotion, receptivity, and relational flow. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Eight of Cups is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Eight of Cups shows momentum becoming compulsion, pressure, or tunnel vision getting tangled in the shadow side of flooded feeling, emotional avoidance, or unclear receptivity. Read it as a signal to reset the pace before the pattern hardens further. Eight of Cups rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "For relationships, Eight of Cups speaks to patterns that intensify quickly and reveal what each person keeps repeating within the field of emotion, intimacy, and receptivity. Eight of Cups rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "Eight of Cups around career matters often reveals skill-building, output, and disciplined repetition inside team harmony, creative work, and morale. The work message in Eight of Cups sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "In health readings, Eight of Cups can describe habit, repetition, and the cumulative effect of small actions around nervous-system sensitivity and emotional wellbeing. With Eight of Cups, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Eight of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-cups",
    "name": "Nine of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "09",
    "upright": "Nine of Cups upright highlights a late-stage lesson that asks for resilience through emotion, receptivity, and relational flow. It reads best when you treat the card as a live pattern rather than a decorative mood. Nine of Cups becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Nine of Cups points to resilience fraying under accumulated strain running into difficulty inside flooded feeling, emotional avoidance, or unclear receptivity. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Nine of Cups usually loosens once the suit is handled with less force and more accuracy.",
    "love": "Nine of Cups in a love reading highlights private hopes and guarded fears coming to the surface shaped by emotion, intimacy, and receptivity. Nine of Cups usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "In career readings, Nine of Cups brings attention to results earned through endurance and late-stage refinement within team harmony, creative work, and morale. With Nine of Cups, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "For wellbeing, Nine of Cups often reflects resilience tested by fatigue, overvigilance, or lingering strain linked to nervous-system sensitivity and emotional wellbeing. Nine of Cups asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Nine of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-cups",
    "name": "Ten of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "10",
    "upright": "When Ten of Cups appears upright, the full weight and consequence of the suit meets emotion, receptivity, and relational flow in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Ten of Cups instead of resisting it.",
    "reversed": "When Ten of Cups turns reversed, burden, excess, or the painful end state of the suit becomes harder to handle cleanly through flooded feeling, emotional avoidance, or unclear receptivity. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Ten of Cups improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "In love, Ten of Cups often reflects the long-term consequences of how love has been built around emotion, intimacy, and receptivity. The lesson of Ten of Cups in love is easier to read in timing and tone than in declarations alone.",
    "career": "For work and money, Ten of Cups points to a peak responsibility, heavy load, or culmination with consequences expressed through team harmony, creative work, and morale. Ten of Cups says as much about how you are working as about what you are working on.",
    "health": "Ten of Cups in a health context points toward the point where load, symptoms, or consequences can no longer be ignored affecting nervous-system sensitivity and emotional wellbeing. Ten of Cups is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Ten of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-cups",
    "name": "Page of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "page",
    "upright": "Upright, Page of Cups brings a message, mood, or beginner's encounter with the suit into contact with emotion, receptivity, and relational flow. The reading strengthens when you let the suit behave exactly as it is built to behave. With Page of Cups, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Page of Cups reversed suggests immaturity, avoidance, or a message that is not yet fully understood under strain within flooded feeling, emotional avoidance, or unclear receptivity. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Page of Cups, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "For relationships, Page of Cups speaks to curiosity, flirtation, and a new emotional message within the field of emotion, intimacy, and receptivity. With Page of Cups, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "Page of Cups around career matters often reveals news, learning, and the entry-level form of the suit's lesson inside team harmony, creative work, and morale. Page of Cups often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "In health readings, Page of Cups can describe sensitivity, early messages, and the need to listen sooner around nervous-system sensitivity and emotional wellbeing. The body-level lesson of Page of Cups often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Page of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-cups",
    "name": "Knight of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "knight",
    "upright": "Knight of Cups upright shows the suit in motion, pursuit, and active expression working through emotion, receptivity, and relational flow. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Knight of Cups is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Knight of Cups shows energy that outruns wisdom, timing, or emotional intelligence getting tangled in the shadow side of flooded feeling, emotional avoidance, or unclear receptivity. Read it as a signal to reset the pace before the pattern hardens further. Knight of Cups rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "Knight of Cups in a love reading highlights active pursuit, urgency, and the style in which affection is expressed shaped by emotion, intimacy, and receptivity. Knight of Cups rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "In career readings, Knight of Cups brings attention to the way ambition advances, pursues, or pushes within team harmony, creative work, and morale. The work message in Knight of Cups sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "For wellbeing, Knight of Cups often reflects how energy is being spent, pushed, or driven linked to nervous-system sensitivity and emotional wellbeing. With Knight of Cups, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Knight of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-cups",
    "name": "Queen of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "queen",
    "upright": "Queen of Cups upright highlights embodied mastery of the suit from the inside out through emotion, receptivity, and relational flow. It reads best when you treat the card as a live pattern rather than a decorative mood. Queen of Cups becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Queen of Cups points to inner authority disturbed by self-doubt, overprotection, or emotional leakage running into difficulty inside flooded feeling, emotional avoidance, or unclear receptivity. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Queen of Cups usually loosens once the suit is handled with less force and more accuracy.",
    "love": "In love, Queen of Cups often reflects emotional maturity and how love is held in the inner life around emotion, intimacy, and receptivity. Queen of Cups usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "For work and money, Queen of Cups points to quiet competence, stewardship, and mature command of the craft expressed through team harmony, creative work, and morale. With Queen of Cups, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "Queen of Cups in a health context points toward regulation through self-knowledge, embodied care, and pacing affecting nervous-system sensitivity and emotional wellbeing. Queen of Cups asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Queen of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-cups",
    "name": "King of Cups",
    "arcana": "minor",
    "suit": "cups",
    "rank": "king",
    "upright": "When King of Cups appears upright, directed command of the suit and its responsibilities meets emotion, receptivity, and relational flow in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of King of Cups instead of resisting it.",
    "reversed": "When King of Cups turns reversed, control problems, rigidity, or leadership without balance becomes harder to handle cleanly through flooded feeling, emotional avoidance, or unclear receptivity. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. King of Cups improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "For relationships, King of Cups speaks to commitment, direction, and the standards guiding the bond within the field of emotion, intimacy, and receptivity. The lesson of King of Cups in love is easier to read in timing and tone than in declarations alone.",
    "career": "King of Cups around career matters often reveals decision-making authority, executive pressure, and long-view leadership inside team harmony, creative work, and morale. King of Cups says as much about how you are working as about what you are working on.",
    "health": "In health readings, King of Cups can describe the discipline required to protect long-term strength around nervous-system sensitivity and emotional wellbeing. King of Cups is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "King of Cups uses the imagery of chalices, flowing water, and moonlit scenes speak of feeling and intuition while the rank emphasises leadership, direction, and mature command."
  },
  {
    "slug": "ace-of-swords",
    "name": "Ace of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "ace",
    "upright": "Upright, Ace of Swords brings the first opening of the suit into contact with thought, language, and sharp discernment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Ace of Swords, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Ace of Swords reversed suggests an opening that is present but not yet trusted under strain within stress, overthinking, or conflict sharpened too far. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Ace of Swords, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "Ace of Swords in a love reading highlights a beginning that changes the emotional tone between people shaped by boundaries, truth, and mental distance. With Ace of Swords, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "In career readings, Ace of Swords brings attention to an opening, initiative, or first spark of possibility within strategy, conflict, and decision pressure. Ace of Swords often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "For wellbeing, Ace of Swords often reflects a fresh chance to reset the body's direction linked to stress, sleep quality, and cognitive overload. The body-level lesson of Ace of Swords often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Ace of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-swords",
    "name": "Two of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "02",
    "upright": "Two of Swords upright shows a living balance between two forces working through thought, language, and sharp discernment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Two of Swords is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Two of Swords shows indecision or imbalance between competing pulls getting tangled in the shadow side of stress, overthinking, or conflict sharpened too far. Read it as a signal to reset the pace before the pattern hardens further. Two of Swords rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "In love, Two of Swords often reflects mutual choice and the need to meet each other halfway around boundaries, truth, and mental distance. Two of Swords rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "For work and money, Two of Swords points to competing priorities that need balancing or choosing expressed through strategy, conflict, and decision pressure. The work message in Two of Swords sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "Two of Swords in a health context points toward the need to rebalance two demands pulling on the system affecting stress, sleep quality, and cognitive overload. With Two of Swords, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Two of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-swords",
    "name": "Three of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "03",
    "upright": "Three of Swords upright highlights early growth that needs cooperation to flourish through thought, language, and sharp discernment. It reads best when you treat the card as a live pattern rather than a decorative mood. Three of Swords becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Three of Swords points to growth complicated by mixed signals or weak coordination running into difficulty inside stress, overthinking, or conflict sharpened too far. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Three of Swords usually loosens once the suit is handled with less force and more accuracy.",
    "love": "For relationships, Three of Swords speaks to third influences, celebration, or the first visible growth of a bond within the field of boundaries, truth, and mental distance. Three of Swords usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "Three of Swords around career matters often reveals teamwork, apprenticeship, and early proof of progress inside strategy, conflict, and decision pressure. With Three of Swords, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "In health readings, Three of Swords can describe supportive routines that grow stronger through cooperation around stress, sleep quality, and cognitive overload. Three of Swords asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Three of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-swords",
    "name": "Four of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "04",
    "upright": "When Four of Swords appears upright, a bid for stability that can either steady or stiffen meets thought, language, and sharp discernment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Four of Swords instead of resisting it.",
    "reversed": "When Four of Swords turns reversed, stability turning into stagnation, defensiveness, or over-control becomes harder to handle cleanly through stress, overthinking, or conflict sharpened too far. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Four of Swords improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "Four of Swords in a love reading highlights the tension between safety and emotional aliveness shaped by boundaries, truth, and mental distance. The lesson of Four of Swords in love is easier to read in timing and tone than in declarations alone.",
    "career": "In career readings, Four of Swords brings attention to holding ground, consolidating gains, or resisting change within strategy, conflict, and decision pressure. Four of Swords says as much about how you are working as about what you are working on.",
    "health": "For wellbeing, Four of Swords often reflects the body's wish to stabilise, rest, or guard resources linked to stress, sleep quality, and cognitive overload. Four of Swords is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Four of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-swords",
    "name": "Five of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "05",
    "upright": "Upright, Five of Swords brings friction that demands adjustment into contact with thought, language, and sharp discernment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Five of Swords, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Five of Swords reversed suggests conflict that is no longer productive under strain within stress, overthinking, or conflict sharpened too far. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Five of Swords, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "In love, Five of Swords often reflects conflict, mismatch, or the need to renegotiate expectations around boundaries, truth, and mental distance. With Five of Swords, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "For work and money, Five of Swords points to pressure, rivalry, or a correction forced by friction expressed through strategy, conflict, and decision pressure. Five of Swords often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "Five of Swords in a health context points toward stress signals that show something must change affecting stress, sleep quality, and cognitive overload. The body-level lesson of Five of Swords often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Five of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-swords",
    "name": "Six of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "06",
    "upright": "Six of Swords upright shows movement that restores rhythm or support working through thought, language, and sharp discernment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Six of Swords is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Six of Swords shows support that is uneven, delayed, or taken for granted getting tangled in the shadow side of stress, overthinking, or conflict sharpened too far. Read it as a signal to reset the pace before the pattern hardens further. Six of Swords rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "For relationships, Six of Swords speaks to repair, reassurance, or an easier flow returning within the field of boundaries, truth, and mental distance. Six of Swords rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "Six of Swords around career matters often reveals recognition, support, or movement after a stuck phase inside strategy, conflict, and decision pressure. The work message in Six of Swords sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "In health readings, Six of Swords can describe improvement, relief, or recovery aided by support around stress, sleep quality, and cognitive overload. With Six of Swords, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Six of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-swords",
    "name": "Seven of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "07",
    "upright": "Seven of Swords upright highlights a test of judgment, courage, or strategy through thought, language, and sharp discernment. It reads best when you treat the card as a live pattern rather than a decorative mood. Seven of Swords becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Seven of Swords points to strategy slipping into suspicion, fatigue, or second-guessing running into difficulty inside stress, overthinking, or conflict sharpened too far. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Seven of Swords usually loosens once the suit is handled with less force and more accuracy.",
    "love": "Seven of Swords in a love reading highlights tests of trust, discernment, or loyalty shaped by boundaries, truth, and mental distance. Seven of Swords usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "In career readings, Seven of Swords brings attention to strategy, caution, and the need to read the field accurately within strategy, conflict, and decision pressure. With Seven of Swords, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "For wellbeing, Seven of Swords often reflects trial, patience, and reading what the body is really asking for linked to stress, sleep quality, and cognitive overload. Seven of Swords asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Seven of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-swords",
    "name": "Eight of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "08",
    "upright": "When Eight of Swords appears upright, repetition that becomes momentum or skill meets thought, language, and sharp discernment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Eight of Swords instead of resisting it.",
    "reversed": "When Eight of Swords turns reversed, momentum becoming compulsion, pressure, or tunnel vision becomes harder to handle cleanly through stress, overthinking, or conflict sharpened too far. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Eight of Swords improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "In love, Eight of Swords often reflects patterns that intensify quickly and reveal what each person keeps repeating around boundaries, truth, and mental distance. The lesson of Eight of Swords in love is easier to read in timing and tone than in declarations alone.",
    "career": "For work and money, Eight of Swords points to skill-building, output, and disciplined repetition expressed through strategy, conflict, and decision pressure. Eight of Swords says as much about how you are working as about what you are working on.",
    "health": "Eight of Swords in a health context points toward habit, repetition, and the cumulative effect of small actions affecting stress, sleep quality, and cognitive overload. Eight of Swords is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Eight of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-swords",
    "name": "Nine of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "09",
    "upright": "Upright, Nine of Swords brings a late-stage lesson that asks for resilience into contact with thought, language, and sharp discernment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Nine of Swords, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Nine of Swords reversed suggests resilience fraying under accumulated strain under strain within stress, overthinking, or conflict sharpened too far. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Nine of Swords, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "For relationships, Nine of Swords speaks to private hopes and guarded fears coming to the surface within the field of boundaries, truth, and mental distance. With Nine of Swords, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "Nine of Swords around career matters often reveals results earned through endurance and late-stage refinement inside strategy, conflict, and decision pressure. Nine of Swords often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "In health readings, Nine of Swords can describe resilience tested by fatigue, overvigilance, or lingering strain around stress, sleep quality, and cognitive overload. The body-level lesson of Nine of Swords often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Nine of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-swords",
    "name": "Ten of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "10",
    "upright": "Ten of Swords upright shows the full weight and consequence of the suit working through thought, language, and sharp discernment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Ten of Swords is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Ten of Swords shows burden, excess, or the painful end state of the suit getting tangled in the shadow side of stress, overthinking, or conflict sharpened too far. Read it as a signal to reset the pace before the pattern hardens further. Ten of Swords rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "Ten of Swords in a love reading highlights the long-term consequences of how love has been built shaped by boundaries, truth, and mental distance. Ten of Swords rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "In career readings, Ten of Swords brings attention to a peak responsibility, heavy load, or culmination with consequences within strategy, conflict, and decision pressure. The work message in Ten of Swords sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "For wellbeing, Ten of Swords often reflects the point where load, symptoms, or consequences can no longer be ignored linked to stress, sleep quality, and cognitive overload. With Ten of Swords, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Ten of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-swords",
    "name": "Page of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "page",
    "upright": "Page of Swords upright highlights a message, mood, or beginner's encounter with the suit through thought, language, and sharp discernment. It reads best when you treat the card as a live pattern rather than a decorative mood. Page of Swords becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Page of Swords points to immaturity, avoidance, or a message that is not yet fully understood running into difficulty inside stress, overthinking, or conflict sharpened too far. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Page of Swords usually loosens once the suit is handled with less force and more accuracy.",
    "love": "In love, Page of Swords often reflects curiosity, flirtation, and a new emotional message around boundaries, truth, and mental distance. Page of Swords usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "For work and money, Page of Swords points to news, learning, and the entry-level form of the suit's lesson expressed through strategy, conflict, and decision pressure. With Page of Swords, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "Page of Swords in a health context points toward sensitivity, early messages, and the need to listen sooner affecting stress, sleep quality, and cognitive overload. Page of Swords asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Page of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-swords",
    "name": "Knight of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "knight",
    "upright": "When Knight of Swords appears upright, the suit in motion, pursuit, and active expression meets thought, language, and sharp discernment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Knight of Swords instead of resisting it.",
    "reversed": "When Knight of Swords turns reversed, energy that outruns wisdom, timing, or emotional intelligence becomes harder to handle cleanly through stress, overthinking, or conflict sharpened too far. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Knight of Swords improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "For relationships, Knight of Swords speaks to active pursuit, urgency, and the style in which affection is expressed within the field of boundaries, truth, and mental distance. The lesson of Knight of Swords in love is easier to read in timing and tone than in declarations alone.",
    "career": "Knight of Swords around career matters often reveals the way ambition advances, pursues, or pushes inside strategy, conflict, and decision pressure. Knight of Swords says as much about how you are working as about what you are working on.",
    "health": "In health readings, Knight of Swords can describe how energy is being spent, pushed, or driven around stress, sleep quality, and cognitive overload. Knight of Swords is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Knight of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-swords",
    "name": "Queen of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "queen",
    "upright": "Upright, Queen of Swords brings embodied mastery of the suit from the inside out into contact with thought, language, and sharp discernment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Queen of Swords, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Queen of Swords reversed suggests inner authority disturbed by self-doubt, overprotection, or emotional leakage under strain within stress, overthinking, or conflict sharpened too far. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Queen of Swords, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "Queen of Swords in a love reading highlights emotional maturity and how love is held in the inner life shaped by boundaries, truth, and mental distance. With Queen of Swords, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "In career readings, Queen of Swords brings attention to quiet competence, stewardship, and mature command of the craft within strategy, conflict, and decision pressure. Queen of Swords often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "For wellbeing, Queen of Swords often reflects regulation through self-knowledge, embodied care, and pacing linked to stress, sleep quality, and cognitive overload. The body-level lesson of Queen of Swords often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Queen of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-swords",
    "name": "King of Swords",
    "arcana": "minor",
    "suit": "swords",
    "rank": "king",
    "upright": "King of Swords upright shows directed command of the suit and its responsibilities working through thought, language, and sharp discernment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. King of Swords is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed King of Swords shows control problems, rigidity, or leadership without balance getting tangled in the shadow side of stress, overthinking, or conflict sharpened too far. Read it as a signal to reset the pace before the pattern hardens further. King of Swords rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "In love, King of Swords often reflects commitment, direction, and the standards guiding the bond around boundaries, truth, and mental distance. King of Swords rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "For work and money, King of Swords points to decision-making authority, executive pressure, and long-view leadership expressed through strategy, conflict, and decision pressure. The work message in King of Swords sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "King of Swords in a health context points toward the discipline required to protect long-term strength affecting stress, sleep quality, and cognitive overload. With King of Swords, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "King of Swords uses the imagery of blades, clouds, and strong winds show thought, tension, and clarity while the rank emphasises leadership, direction, and mature command."
  },
  {
    "slug": "ace-of-pentacles",
    "name": "Ace of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "ace",
    "upright": "Ace of Pentacles upright highlights the first opening of the suit through material reality, craft, and steadier embodiment. It reads best when you treat the card as a live pattern rather than a decorative mood. Ace of Pentacles becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Ace of Pentacles points to an opening that is present but not yet trusted running into difficulty inside heaviness, scarcity pressure, or rigid practicality. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Ace of Pentacles usually loosens once the suit is handled with less force and more accuracy.",
    "love": "For relationships, Ace of Pentacles speaks to a beginning that changes the emotional tone between people within the field of reliability, practical care, and long-term building. Ace of Pentacles usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "Ace of Pentacles around career matters often reveals an opening, initiative, or first spark of possibility inside income, craft, and material progress. With Ace of Pentacles, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "In health readings, Ace of Pentacles can describe a fresh chance to reset the body's direction around body routines, recovery, and tangible habits. Ace of Pentacles asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Ace of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises beginnings and pure potential."
  },
  {
    "slug": "two-of-pentacles",
    "name": "Two of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "02",
    "upright": "When Two of Pentacles appears upright, a living balance between two forces meets material reality, craft, and steadier embodiment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Two of Pentacles instead of resisting it.",
    "reversed": "When Two of Pentacles turns reversed, indecision or imbalance between competing pulls becomes harder to handle cleanly through heaviness, scarcity pressure, or rigid practicality. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Two of Pentacles improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "Two of Pentacles in a love reading highlights mutual choice and the need to meet each other halfway shaped by reliability, practical care, and long-term building. The lesson of Two of Pentacles in love is easier to read in timing and tone than in declarations alone.",
    "career": "In career readings, Two of Pentacles brings attention to competing priorities that need balancing or choosing within income, craft, and material progress. Two of Pentacles says as much about how you are working as about what you are working on.",
    "health": "For wellbeing, Two of Pentacles often reflects the need to rebalance two demands pulling on the system linked to body routines, recovery, and tangible habits. Two of Pentacles is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Two of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises choice and balancing forces."
  },
  {
    "slug": "three-of-pentacles",
    "name": "Three of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "03",
    "upright": "Upright, Three of Pentacles brings early growth that needs cooperation to flourish into contact with material reality, craft, and steadier embodiment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Three of Pentacles, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Three of Pentacles reversed suggests growth complicated by mixed signals or weak coordination under strain within heaviness, scarcity pressure, or rigid practicality. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Three of Pentacles, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "In love, Three of Pentacles often reflects third influences, celebration, or the first visible growth of a bond around reliability, practical care, and long-term building. With Three of Pentacles, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "For work and money, Three of Pentacles points to teamwork, apprenticeship, and early proof of progress expressed through income, craft, and material progress. Three of Pentacles often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "Three of Pentacles in a health context points toward supportive routines that grow stronger through cooperation affecting body routines, recovery, and tangible habits. The body-level lesson of Three of Pentacles often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Three of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises collaboration and early growth."
  },
  {
    "slug": "four-of-pentacles",
    "name": "Four of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "04",
    "upright": "Four of Pentacles upright shows a bid for stability that can either steady or stiffen working through material reality, craft, and steadier embodiment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Four of Pentacles is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Four of Pentacles shows stability turning into stagnation, defensiveness, or over-control getting tangled in the shadow side of heaviness, scarcity pressure, or rigid practicality. Read it as a signal to reset the pace before the pattern hardens further. Four of Pentacles rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "For relationships, Four of Pentacles speaks to the tension between safety and emotional aliveness within the field of reliability, practical care, and long-term building. Four of Pentacles rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "Four of Pentacles around career matters often reveals holding ground, consolidating gains, or resisting change inside income, craft, and material progress. The work message in Four of Pentacles sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "In health readings, Four of Pentacles can describe the body's wish to stabilise, rest, or guard resources around body routines, recovery, and tangible habits. With Four of Pentacles, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Four of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises stability and the need to consolidate."
  },
  {
    "slug": "five-of-pentacles",
    "name": "Five of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "05",
    "upright": "Five of Pentacles upright highlights friction that demands adjustment through material reality, craft, and steadier embodiment. It reads best when you treat the card as a live pattern rather than a decorative mood. Five of Pentacles becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Five of Pentacles points to conflict that is no longer productive running into difficulty inside heaviness, scarcity pressure, or rigid practicality. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Five of Pentacles usually loosens once the suit is handled with less force and more accuracy.",
    "love": "Five of Pentacles in a love reading highlights conflict, mismatch, or the need to renegotiate expectations shaped by reliability, practical care, and long-term building. Five of Pentacles usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "In career readings, Five of Pentacles brings attention to pressure, rivalry, or a correction forced by friction within income, craft, and material progress. With Five of Pentacles, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "For wellbeing, Five of Pentacles often reflects stress signals that show something must change linked to body routines, recovery, and tangible habits. Five of Pentacles asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Five of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises friction, challenge, and adjustment."
  },
  {
    "slug": "six-of-pentacles",
    "name": "Six of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "06",
    "upright": "When Six of Pentacles appears upright, movement that restores rhythm or support meets material reality, craft, and steadier embodiment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Six of Pentacles instead of resisting it.",
    "reversed": "When Six of Pentacles turns reversed, support that is uneven, delayed, or taken for granted becomes harder to handle cleanly through heaviness, scarcity pressure, or rigid practicality. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Six of Pentacles improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "In love, Six of Pentacles often reflects repair, reassurance, or an easier flow returning around reliability, practical care, and long-term building. The lesson of Six of Pentacles in love is easier to read in timing and tone than in declarations alone.",
    "career": "For work and money, Six of Pentacles points to recognition, support, or movement after a stuck phase expressed through income, craft, and material progress. Six of Pentacles says as much about how you are working as about what you are working on.",
    "health": "Six of Pentacles in a health context points toward improvement, relief, or recovery aided by support affecting body routines, recovery, and tangible habits. Six of Pentacles is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Six of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises movement, support, and regained rhythm."
  },
  {
    "slug": "seven-of-pentacles",
    "name": "Seven of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "07",
    "upright": "Upright, Seven of Pentacles brings a test of judgment, courage, or strategy into contact with material reality, craft, and steadier embodiment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Seven of Pentacles, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Seven of Pentacles reversed suggests strategy slipping into suspicion, fatigue, or second-guessing under strain within heaviness, scarcity pressure, or rigid practicality. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Seven of Pentacles, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "For relationships, Seven of Pentacles speaks to tests of trust, discernment, or loyalty within the field of reliability, practical care, and long-term building. With Seven of Pentacles, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "Seven of Pentacles around career matters often reveals strategy, caution, and the need to read the field accurately inside income, craft, and material progress. Seven of Pentacles often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "In health readings, Seven of Pentacles can describe trial, patience, and reading what the body is really asking for around body routines, recovery, and tangible habits. The body-level lesson of Seven of Pentacles often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Seven of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises testing, discernment, and strategy."
  },
  {
    "slug": "eight-of-pentacles",
    "name": "Eight of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "08",
    "upright": "Eight of Pentacles upright shows repetition that becomes momentum or skill working through material reality, craft, and steadier embodiment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Eight of Pentacles is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Eight of Pentacles shows momentum becoming compulsion, pressure, or tunnel vision getting tangled in the shadow side of heaviness, scarcity pressure, or rigid practicality. Read it as a signal to reset the pace before the pattern hardens further. Eight of Pentacles rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "Eight of Pentacles in a love reading highlights patterns that intensify quickly and reveal what each person keeps repeating shaped by reliability, practical care, and long-term building. Eight of Pentacles rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "In career readings, Eight of Pentacles brings attention to skill-building, output, and disciplined repetition within income, craft, and material progress. The work message in Eight of Pentacles sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "For wellbeing, Eight of Pentacles often reflects habit, repetition, and the cumulative effect of small actions linked to body routines, recovery, and tangible habits. With Eight of Pentacles, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Eight of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises momentum, skill, and focused repetition."
  },
  {
    "slug": "nine-of-pentacles",
    "name": "Nine of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "09",
    "upright": "Nine of Pentacles upright highlights a late-stage lesson that asks for resilience through material reality, craft, and steadier embodiment. It reads best when you treat the card as a live pattern rather than a decorative mood. Nine of Pentacles becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Nine of Pentacles points to resilience fraying under accumulated strain running into difficulty inside heaviness, scarcity pressure, or rigid practicality. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Nine of Pentacles usually loosens once the suit is handled with less force and more accuracy.",
    "love": "In love, Nine of Pentacles often reflects private hopes and guarded fears coming to the surface around reliability, practical care, and long-term building. Nine of Pentacles usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "For work and money, Nine of Pentacles points to results earned through endurance and late-stage refinement expressed through income, craft, and material progress. With Nine of Pentacles, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "Nine of Pentacles in a health context points toward resilience tested by fatigue, overvigilance, or lingering strain affecting body routines, recovery, and tangible habits. Nine of Pentacles asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Nine of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises culmination, resilience, and hard-won perspective."
  },
  {
    "slug": "ten-of-pentacles",
    "name": "Ten of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "10",
    "upright": "When Ten of Pentacles appears upright, the full weight and consequence of the suit meets material reality, craft, and steadier embodiment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of Ten of Pentacles instead of resisting it.",
    "reversed": "When Ten of Pentacles turns reversed, burden, excess, or the painful end state of the suit becomes harder to handle cleanly through heaviness, scarcity pressure, or rigid practicality. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. Ten of Pentacles improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "For relationships, Ten of Pentacles speaks to the long-term consequences of how love has been built within the field of reliability, practical care, and long-term building. The lesson of Ten of Pentacles in love is easier to read in timing and tone than in declarations alone.",
    "career": "Ten of Pentacles around career matters often reveals a peak responsibility, heavy load, or culmination with consequences inside income, craft, and material progress. Ten of Pentacles says as much about how you are working as about what you are working on.",
    "health": "In health readings, Ten of Pentacles can describe the point where load, symptoms, or consequences can no longer be ignored around body routines, recovery, and tangible habits. Ten of Pentacles is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
    "imagery": "Ten of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises completion, weight, and full consequence."
  },
  {
    "slug": "page-of-pentacles",
    "name": "Page of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "page",
    "upright": "Upright, Page of Pentacles brings a message, mood, or beginner's encounter with the suit into contact with material reality, craft, and steadier embodiment. The reading strengthens when you let the suit behave exactly as it is built to behave. With Page of Pentacles, clarity arrives through participation, not through hovering at a distance.",
    "reversed": "Page of Pentacles reversed suggests immaturity, avoidance, or a message that is not yet fully understood under strain within heaviness, scarcity pressure, or rigid practicality. The card asks for correction, honesty, and a calmer relationship with the suit's pressure. With Page of Pentacles, the shadow softens as soon as the misused energy is brought back into proportion.",
    "love": "Page of Pentacles in a love reading highlights curiosity, flirtation, and a new emotional message shaped by reliability, practical care, and long-term building. With Page of Pentacles, affection becomes clearer once you watch what each person consistently does with vulnerability.",
    "career": "In career readings, Page of Pentacles brings attention to news, learning, and the entry-level form of the suit's lesson within income, craft, and material progress. Page of Pentacles often reveals whether effort is being invested in the right direction or only in the loudest demand.",
    "health": "For wellbeing, Page of Pentacles often reflects sensitivity, early messages, and the need to listen sooner linked to body routines, recovery, and tangible habits. The body-level lesson of Page of Pentacles often lives in rhythm, repetition, and the feedback loop you keep reinforcing.",
    "imagery": "Page of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises curiosity, learning, and a fresh message."
  },
  {
    "slug": "knight-of-pentacles",
    "name": "Knight of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "knight",
    "upright": "Knight of Pentacles upright shows the suit in motion, pursuit, and active expression working through material reality, craft, and steadier embodiment. Instead of overcomplicating the message, follow the simplest version of the suit's lesson first. Knight of Pentacles is easiest to read once you notice where this exact energy is already happening in real life.",
    "reversed": "Reversed Knight of Pentacles shows energy that outruns wisdom, timing, or emotional intelligence getting tangled in the shadow side of heaviness, scarcity pressure, or rigid practicality. Read it as a signal to reset the pace before the pattern hardens further. Knight of Pentacles rarely asks for drama; it asks for a more conscious use of the suit's power.",
    "love": "In love, Knight of Pentacles often reflects active pursuit, urgency, and the style in which affection is expressed around reliability, practical care, and long-term building. Knight of Pentacles rarely flatters; it shows the relationship exactly at the point where feeling becomes action.",
    "career": "For work and money, Knight of Pentacles points to the way ambition advances, pursues, or pushes expressed through income, craft, and material progress. The work message in Knight of Pentacles sharpens when you ask what this card is rewarding and what it is quietly taxing.",
    "health": "Knight of Pentacles in a health context points toward how energy is being spent, pushed, or driven affecting body routines, recovery, and tangible habits. With Knight of Pentacles, wellbeing improves once the underlying pattern is respected before the symptoms are argued with.",
    "imagery": "Knight of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises motion, pursuit, and committed effort."
  },
  {
    "slug": "queen-of-pentacles",
    "name": "Queen of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "queen",
    "upright": "Queen of Pentacles upright highlights embodied mastery of the suit from the inside out through material reality, craft, and steadier embodiment. It reads best when you treat the card as a live pattern rather than a decorative mood. Queen of Pentacles becomes strongest when the suit is allowed to do its natural work without apology.",
    "reversed": "Reversed, Queen of Pentacles points to inner authority disturbed by self-doubt, overprotection, or emotional leakage running into difficulty inside heaviness, scarcity pressure, or rigid practicality. The energy is not gone; it is knotted, delayed, or expressed in the wrong proportion. The knot in Queen of Pentacles usually loosens once the suit is handled with less force and more accuracy.",
    "love": "For relationships, Queen of Pentacles speaks to emotional maturity and how love is held in the inner life within the field of reliability, practical care, and long-term building. Queen of Pentacles usually tells the truth of the bond through behaviour before anyone says it out loud.",
    "career": "Queen of Pentacles around career matters often reveals quiet competence, stewardship, and mature command of the craft inside income, craft, and material progress. With Queen of Pentacles, career clarity usually arrives through standards, pacing, and the quality of your response under pressure.",
    "health": "In health readings, Queen of Pentacles can describe regulation through self-knowledge, embodied care, and pacing around body routines, recovery, and tangible habits. Queen of Pentacles asks you to notice what your system has been signalling long before it had words for it.",
    "imagery": "Queen of Pentacles uses the imagery of coins, gardens, and architecture point to growth in the physical world while the rank emphasises mastery through embodiment and inner authority."
  },
  {
    "slug": "king-of-pentacles",
    "name": "King of Pentacles",
    "arcana": "minor",
    "suit": "pentacles",
    "rank": "king",
    "upright": "When King of Pentacles appears upright, directed command of the suit and its responsibilities meets material reality, craft, and steadier embodiment in a way that wants expression. The card usually becomes clearest once you stop abstracting it and notice where the energy is already active. The card rewards a response that matches the tempo of King of Pentacles instead of resisting it.",
    "reversed": "When King of Pentacles turns reversed, control problems, rigidity, or leadership without balance becomes harder to handle cleanly through heaviness, scarcity pressure, or rigid practicality. Usually the remedy begins with noticing where the suit is being forced, avoided, or misread. King of Pentacles improves when the underlying pattern is named plainly instead of managed indirectly.",
    "love": "King of Pentacles in a love reading highlights commitment, direction, and the standards guiding the bond shaped by reliability, practical care, and long-term building. The lesson of King of Pentacles in love is easier to read in timing and tone than in declarations alone.",
    "career": "In career readings, King of Pentacles brings attention to decision-making authority, executive pressure, and long-view leadership within income, craft, and material progress. King of Pentacles says as much about how you are working as about what you are working on.",
    "health": "For wellbeing, King of Pentacles often reflects the discipline required to protect long-term strength linked to body routines, recovery, and tangible habits. King of Pentacles is most helpful when it is read as a pattern of regulation, depletion, recovery, or pacing.",
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
