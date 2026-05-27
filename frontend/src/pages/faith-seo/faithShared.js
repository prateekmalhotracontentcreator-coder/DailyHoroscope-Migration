export const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api/faith`;
export const SITE = 'https://www.everydayhoroscope.in';

export function titleCaseSlug(value) {
  return String(value || '')
    .split('-')
    .map((item) => item.charAt(0).toUpperCase() + item.slice(1))
    .join(' ');
}

export function buildBreadcrumbSchema(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

export function buildFaqSchema(items, questionKey = 'q', answerKey = 'a') {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: (items || []).map((item) => ({
      '@type': 'Question',
      name: item[questionKey],
      acceptedAnswer: {
        '@type': 'Answer',
        text: item[answerKey],
      },
    })),
  };
}

export function buildArticleSchema({ headline, description, url, about = null }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline,
    description,
    url,
    author: {
      '@type': 'Organization',
      name: 'Everyday Horoscope',
    },
    publisher: {
      '@type': 'Organization',
      name: 'Everyday Horoscope',
    },
    inLanguage: 'en',
  };
  if (about) {
    schema.about = about;
  }
  return schema;
}

export function buildCollectionSchema({ name, description, url, items = [] }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name,
    description,
    url,
    mainEntity: {
      '@type': 'ItemList',
      itemListElement: items.map((item, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        name: item.name,
        url: item.url,
      })),
    },
  };
}
