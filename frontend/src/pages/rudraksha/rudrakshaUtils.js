export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api/rudraksha`;
export const SITE = 'https://www.everydayhoroscope.in';

export const ACTIVATION_STEPS = [
  {
    title: 'Cleanse',
    body: 'Rinse the bead gently with clean water and wipe it dry before wearing.',
  },
  {
    title: 'Energise',
    body: 'Sit quietly, hold the bead with intention, and invoke the deity or planetary current linked with it.',
  },
  {
    title: 'Mantra',
    body: 'Chant the suggested mantra with a calm and steady mind rather than rushing the process.',
  },
  {
    title: 'Wear',
    body: 'Wear it respectfully and keep your daily conduct aligned with the purpose for which you chose it.',
  },
];

export const HUB_FAQ = [
  {
    question: 'What is Rudraksha?',
    answer: 'Rudraksha refers to sacred seeds traditionally worn for spiritual practice, mental steadiness, and devotional support.',
  },
  {
    question: 'How many mukhis are there in this guide?',
    answer: 'This module covers the 21 classical mukhi Rudraksha types, plus a calculator that recommends a starting point from your birth chart.',
  },
  {
    question: 'Can I wear more than one Rudraksha?',
    answer: 'Many people do, but combinations are usually chosen around a main goal rather than collecting many beads at once.',
  },
  {
    question: 'Is 5 Mukhi suitable for most people?',
    answer: 'Yes. 5 Mukhi is commonly treated as the most universal everyday bead for calmness, discipline, and spiritual grounding.',
  },
  {
    question: 'Does the calculator replace personal guidance?',
    answer: 'No. It offers a chart-based starting recommendation for spiritual guidance, not a final verdict or medical remedy.',
  },
];

export const CALCULATOR_FAQ = [
  {
    question: 'How does the Rudraksha calculator work?',
    answer: 'It reads your Vedic birth chart signals such as Lagna, Moon sign, current Mahadasha, and planetary weakness before mapping them to traditional Rudraksha recommendations.',
  },
  {
    question: 'What if I do not know my birth time?',
    answer: 'You can still calculate with a default noon time, but the recommendation becomes broader because house positions may shift.',
  },
  {
    question: 'Is 5 Mukhi always included?',
    answer: 'Yes. The calculator keeps 5 Mukhi as a universal baseline note because it is widely considered supportive for most people.',
  },
  {
    question: 'Can this recommendation diagnose health or life outcomes?',
    answer: 'No. It is a spiritual guidance tool based on Vedic principles and should not be treated as medical, legal, or financial advice.',
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
      item: item.item,
    })),
  };
}

export function buildArticleSchema(mukhi) {
  return {
    '@type': 'Article',
    headline: `${mukhi.mukhi} Mukhi Rudraksha - Benefits, Who Should Wear & Mantra`,
    description: mukhi.meta_description,
    author: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
    publisher: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
    mainEntityOfPage: `${SITE}/rudraksha/${mukhi.slug}`,
  };
}

export function buildTopicArticleSchema({ headline, description, url }) {
  return {
    '@type': 'Article',
    headline,
    description,
    author: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
    publisher: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
    mainEntityOfPage: url,
  };
}

export function normalizeFaqItems(items) {
  return (items || []).map((item) => ({
    question: item.question || item.q || '',
    answer: item.answer || item.a || '',
  })).filter((item) => item.question && item.answer);
}

export function canonicalTitle(value) {
  return String(value || '')
    .replace(/\s+\|\s+EverydayHoroscope$/, '')
    .trim();
}
