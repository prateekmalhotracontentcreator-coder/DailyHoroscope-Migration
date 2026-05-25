export const SITE = 'https://www.everydayhoroscope.in';

export const GRID_LAYOUT = [
  [4, 9, 2],
  [3, 5, 7],
  [8, 1, 6],
];

export const GRID_CELL_DETAILS = {
  1: { label: 'Identity', note: 'self-belief, initiative, leadership' },
  2: { label: 'Emotion', note: 'intuition, cooperation, sensitivity' },
  3: { label: 'Expression', note: 'optimism, voice, creativity' },
  4: { label: 'Structure', note: 'discipline, systems, stability' },
  5: { label: 'Balance', note: 'adaptability, communication, agility' },
  6: { label: 'Harmony', note: 'relationships, beauty, responsibility' },
  7: { label: 'Insight', note: 'reflection, depth, spiritual instinct' },
  8: { label: 'Endurance', note: 'patience, realism, material discipline' },
  9: { label: 'Drive', note: 'courage, action, intensity' },
};

export const MISSING_NUMBER_LINKS = Array.from({ length: 9 }, (_, index) => {
  const number = index + 1;
  return {
    number,
    href: `/lo-shu-grid/missing-${number}`,
    label: `Missing ${number}`,
  };
});

export const ARROW_LINKS = [
  { slug: 'intellect', name: 'Arrow of Intellect', numbers: [4, 9, 2], theme: 'Mind plane' },
  { slug: 'spirituality', name: 'Arrow of Spirituality', numbers: [3, 5, 7], theme: 'Soul plane' },
  { slug: 'prosperity', name: 'Arrow of Prosperity', numbers: [8, 1, 6], theme: 'Practical plane' },
  { slug: 'planner', name: 'Arrow of Planner', numbers: [4, 3, 8], theme: 'Thought column' },
  { slug: 'will-power', name: 'Arrow of Will Power', numbers: [9, 5, 1], theme: 'Will column' },
  { slug: 'action', name: 'Arrow of Action', numbers: [2, 7, 6], theme: 'Action column' },
  { slug: 'emotional-balance', name: 'Arrow of Emotional Balance', numbers: [4, 5, 6], theme: 'Rajayoga diagonal' },
  { slug: 'determination', name: 'Arrow of Determination', numbers: [2, 5, 8], theme: 'Rajayoga diagonal' },
];

export const HUB_FAQ_ITEMS = [
  {
    question: 'What is Lo Shu Grid in numerology?',
    answer: 'Lo Shu Grid is a 3x3 numerology chart that maps the digits 1 to 9 into a fixed square. The presence or absence of numbers is then used to read natural strengths, weaker zones, and repeating patterns.',
  },
  {
    question: 'How is the Lo Shu Grid calculated?',
    answer: 'This module uses the date of birth digits, the reduced day number, Destiny number, Kua number, and full name number to mark which cells are present in the grid.',
  },
  {
    question: 'What does a missing number mean in Lo Shu Grid?',
    answer: 'A missing number points to an energy that may need conscious development. It is not a verdict, but it often describes a trait that grows more through practice than instinct.',
  },
  {
    question: 'What are Lo Shu arrows?',
    answer: 'Arrows are complete rows, columns, or diagonals inside the grid. When all three numbers of a line are present, the pattern is treated as a stronger operating tendency.',
  },
  {
    question: 'Is Lo Shu Grid accurate?',
    answer: 'Lo Shu Grid is best used as a reflective numerology framework. It can be insightful when read with honesty, but it should not be treated as a substitute for practical judgment or professional advice.',
  },
];

export const CALCULATOR_FAQ_ITEMS = [
  {
    question: 'Why does the calculator ask for gender?',
    answer: 'Gender is used only for the Kua number step in this commission, because the male and female calculation paths differ in the decoded Lo Shu rules.',
  },
  {
    question: 'Does the calculator use my full name?',
    answer: 'Yes. It reduces the full name into a Pythagorean name number and adds that value to the grid build.',
  },
  {
    question: 'Do missing numbers mean something is wrong with me?',
    answer: 'No. Missing numbers are better understood as developmental themes. They highlight where effort and awareness usually matter more.',
  },
  {
    question: 'What is Rajayoga in this Lo Shu module?',
    answer: 'Rajayoga here refers to the two highlighted diagonals, 4-5-6 and 2-5-8, which the decoded source marks as stronger success patterns.',
  },
];

export function buildFaqSchema(items) {
  return {
    '@type': 'FAQPage',
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  };
}

export function buildBreadcrumbSchema(items) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}
