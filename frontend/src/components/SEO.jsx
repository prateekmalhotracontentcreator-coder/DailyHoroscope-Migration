import { useEffect } from 'react';

const DEFAULT = {
  title: 'Everyday Horoscope -- Free Daily, Weekly & Monthly Horoscope',
  description: 'Get your free daily, weekly, and monthly horoscope predictions. Explore Birth Chart Analysis, Kundali Milan, and Brihat Kundli Pro -- AI-powered Vedic astrology insights.',
  image: 'https://www.everydayhoroscope.in/og-image.png',
  url: 'https://www.everydayhoroscope.in',
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
  canonical,
  hreflang = null,
  type = 'website',
  noindex = false,
  schema = null,
  jsonLd = null,
}) => {
  useEffect(() => {
    const fullTitle = title
      ? `${title} | Everyday Horoscope`
      : DEFAULT.title;
    const desc = description || DEFAULT.description;
    const img = image || DEFAULT.image;
    const pageUrl = url || canonical || DEFAULT.url;
    const canonicalUrl = canonical || pageUrl;
    const structuredData = jsonLd || schema;

    document.title = fullTitle;

    setMeta('description', desc);
    setMeta('robots', noindex ? 'noindex, nofollow' : 'index, follow');

    setMeta('og:title', fullTitle, 'property');
    setMeta('og:description', desc, 'property');
    setMeta('og:image', img, 'property');
    setMeta('og:url', pageUrl, 'property');
    setMeta('og:type', type, 'property');

    setMeta('twitter:card', 'summary_large_image', 'name');
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
    canonical.setAttribute('href', canonicalUrl);

    const managedHreflangNodes = Array.from(document.querySelectorAll('link[data-seo-hreflang="true"]'));
    managedHreflangNodes.forEach((node) => node.remove());

    if (Array.isArray(hreflang)) {
      hreflang.forEach((item) => {
        if (!item?.lang || !item?.href) return;
        const link = document.createElement('link');
        link.setAttribute('rel', 'alternate');
        link.setAttribute('hrefLang', item.lang);
        link.setAttribute('href', item.href);
        link.setAttribute('data-seo-hreflang', 'true');
        document.head.appendChild(link);
      });
    }

    if (structuredData) {
      const existingSchema = document.getElementById('page-schema');
      if (existingSchema) existingSchema.remove();
      const script = document.createElement('script');
      script.id = 'page-schema';
      script.type = 'application/ld+json';
      script.text = JSON.stringify(structuredData);
      document.head.appendChild(script);
    }

    return () => {
      if (structuredData) {
        const s = document.getElementById('page-schema');
        if (s) s.remove();
      }
      const hreflangNodes = Array.from(document.querySelectorAll('link[data-seo-hreflang="true"]'));
      hreflangNodes.forEach((node) => node.remove());
    };
  }, [title, description, image, url, canonical, hreflang, type, noindex, schema, jsonLd]);

  return null;
};
