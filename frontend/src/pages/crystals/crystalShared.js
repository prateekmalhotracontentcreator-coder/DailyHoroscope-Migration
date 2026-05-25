export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api/crystals`;
export const SITE = 'https://www.everydayhoroscope.in';

export const HUB_FAQS = [
  {
    question: 'How does crystal healing work?',
    answer: 'Crystal healing is usually approached as an intention-based practice. People work with stones to reinforce a desired emotional, spiritual, or environmental state through ritual, symbolism, and repeated attention.',
  },
  {
    question: 'Are Vedic gemstones and healing crystals the same thing?',
    answer: 'Not exactly. Vedic gemstones are traditionally chosen to strengthen specific grahas, while healing crystals are generally used more gently for intentions like calm, love, focus, protection, and meditation.',
  },
  {
    question: 'How do I choose the right crystal?',
    answer: 'Start with your current intention. If you want something more chart-specific, the crystal calculator can point you toward a Vedic gemstone plus softer support stones.',
  },
  {
    question: 'How often should I cleanse my crystals?',
    answer: 'Weekly cleansing is a good baseline for most people. You can do it more often after emotionally heavy periods, travel, or intense ritual work.',
  },
  {
    question: 'Can I use more than one crystal at a time?',
    answer: 'Yes, but simpler is usually better. One grounding stone and one support stone is often easier to feel and easier to keep consistent.',
  },
];

export const CALCULATOR_FAQS = [
  {
    question: 'How does the crystal calculator choose recommendations?',
    answer: 'It looks at your birth chart through the Vedic calculator, checks the active dasha and weaker planetary themes, then overlays the life intention you selected.',
  },
  {
    question: 'Is the result only about Vedic gemstones?',
    answer: 'No. The result includes one primary Vedic gemstone and a smaller set of healing crystals that support emotional, spiritual, or practical balance around your intention.',
  },
  {
    question: 'Do I need exact birth time?',
    answer: 'Exact birth time is best because house positions and dasha interpretation become more reliable. If you only know an approximate time, use the closest value you have.',
  },
  {
    question: 'Can I enter latitude and longitude instead of a city?',
    answer: 'Yes. The calculator accepts a plain city name or a simple `lat,lon` format such as `28.6139,77.2090`.',
  },
  {
    question: 'Does this replace a full gemstone consultation?',
    answer: 'No. This tool is a practical public recommendation engine, not a full personal prescription. Use it as guidance, especially for the softer healing crystal layer.',
  },
];

export function buildFaqSchema(faqItems) {
  return {
    '@type': 'FAQPage',
    mainEntity: faqItems.map((item) => ({
      '@type': 'Question',
      name: item.question || item.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer || item.a,
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

export function buildArticleSchema({ headline, description, url, image = `${SITE}/og-image.png` }) {
  return {
    '@type': 'Article',
    headline,
    description,
    url,
    image,
    author: {
      '@type': 'Organization',
      name: 'Everyday Horoscope',
    },
    publisher: {
      '@type': 'Organization',
      name: 'Everyday Horoscope',
      logo: {
        '@type': 'ImageObject',
        url: `${SITE}/og-image.png`,
      },
    },
  };
}
