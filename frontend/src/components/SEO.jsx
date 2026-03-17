import { useEffect } from 'react';

const DEFAULT = {
  title: 'Everyday Horoscope — Free Daily, Weekly & Monthly Horoscope',
  description: 'Get your free daily, weekly, and monthly horoscope predictions. Explore Birth Chart Analysis, Kundali Milan, and Brihat Kundli Pro — AI-powered Vedic astrology insights.',
  image: 'https://everydayhoroscope.in/og-image.png',
  url: 'https://everydayhoroscope.in',
};

const setMeta = (name, content, attr = 'name') => {
  if (!content) return;
  let el = document.querySelector(`meta[${attr}="${name}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attr, name);
    document.head.appendChild(el);
  }
  el.setAttribute('content', content);
};

export const SEO = ({
  title,
  description,
  image,
  url,
  type = 'website',
  noindex = false,
  schema = null,
}) => {
  useEffect(() => {
    const fullTitle = title
      ? `${title} | Everyday Horoscope`
      : DEFAULT.title;
    const desc = description || DEFAULT.description;
    const img = image || DEFAULT.image;
    const pageUrl = url || DEFAULT.url;

    document.title = fullTitle;

    setMeta('description', desc);
    setMeta('robots', noindex ? 'noindex, nofollow' : 'index, follow');

    setMeta('og:title', fullTitle, 'property');
    setMeta('og:description', desc, 'property');
    setMeta('og:image', img, 'property');
    setMeta('og:url', pageUrl, 'property');
    setMeta('og:type', type, 'property');

    setMeta('twitter:title', fullTitle, 'property');
    setMeta('twitter:description', desc, 'property');
    setMeta('twitter:image', img, 'property');
    setMeta('twitter:url', pageUrl, 'property');

    let canonical = document.querySelector('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', pageUrl);

    if (schema) {
      const existingSchema = document.getElementById('page-schema');
      if (existingSchema) existingSchema.remove();
      const script = document.createElement('script');
      script.id = 'page-schema';
      script.type = 'application/ld+json';
      script.text = JSON.stringify(schema);
      document.head.appendChild(script);
    }

    return () => {
      if (schema) {
        const s = document.getElementById('page-schema');
        if (s) s.remove();
      }
    };
  }, [title, description, image, url, type, noindex, schema]);

  return null;
};
