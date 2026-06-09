import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '◈',
  accentColor: '#9b59b6',
  badge: '₹1,499 one-time',
  headline: 'A 40-page life map drawn entirely from your birth moment - every domain, every planet, every Dasha.',
  subline: 'The most comprehensive Vedic report available. Career, love, health, wealth, Dasha timeline, Yogas, Doshas, and full remedies - all in a single PDF.',
  primaryCta: {
    label: 'Get Brihat Kundli Pro - ₹1,499',
    href: '/brihat-kundli',
  },
  secondaryCta: {
    label: "See What's Inside",
  },
  seo: {
    title: 'Brihat Kundli Pro - 40-Page Vedic Life Report',
    description: 'The most comprehensive Vedic birth report. Career, love, wealth, health, Dasha timeline, Yogas, Doshas, and full remedies in a 40+ page PDF. ₹1,499 one-time.',
    url: 'https://www.everydayhoroscope.in/the-brihat-kundli',
  },
  features: [
    { title: '40+ Page Report', body: 'The most comprehensive Vedic life report on EverydayHoroscope - substantially deeper than the standard Birth Chart.' },
    { title: 'All 9 Planetary Positions', body: 'Sign, house, dignity, strength, combust or retrograde status, and Shadbala scores for all 9 Vedic planets.' },
    { title: 'Career, Love & Wealth Deep Dive', body: 'Three full-section analyses covering career fields, wealth signals, relationship indicators, health vulnerabilities, and more.' },
    { title: 'Full Dasha Timeline', body: 'Current Mahadasha and Antardasha with period predictions, plus the upcoming Dasha sequence for forward planning.' },
    { title: 'Yoga & Dosha Analysis', body: 'Raj Yogas, Dhana Yogas, Mangal Dosha, Kaal Sarp, and other significant combinations identified and interpreted.' },
    { title: 'Gemstone, Mantra & Numerology', body: 'A complete remediation protocol plus a numerology reading derived from your birth name and date.' },
  ],
  steps: [
    { title: 'Enter your birth details', body: 'Date, time, and city. Precise birth time is especially important here because it determines Lagna and every house cusp.' },
    { title: 'Full Vedic computation runs', body: 'Lagna, all 9 planets, divisional charts, Shadbala scores, Yoga identification, Dosha detection, and Dasha calculation are all included.' },
    { title: '40+ page report generated', body: 'Every major life domain is analysed in plain English with actionable remedies and a downloadable PDF.' },
  ],
  preview: {
    title: 'Sample multi-section report preview',
    subtitle: 'The final PDF is designed like a structured life manual: deep sections, timing chapters, and remedy plans in one long-form document.',
    tabs: ['Career', 'Love', 'Health', 'Wealth', 'Dasha'],
    cards: [
      { title: 'Career Window', body: 'Mahadasha and 10th house indicators combine into a timing-based professional reading.' },
      { title: 'Relationship Layer', body: '7th house, Venus, Moon, and family factors explain compatibility and timing pressure.' },
      { title: 'Remedy Protocol', body: 'Gemstones, mantras, and practical behavioural remedies align with the chart profile.' },
    ],
    overlay: 'Premium - Unlock 40+ Page Report',
  },
  faqs: [
    { q: 'How is Brihat Kundli different from the Birth Chart?', a: 'The standard Birth Chart gives a structured overview. Brihat Kundli is a much deeper multi-section reading with timelines, Yogas, Doshas, and full remedy guidance across all major life domains.' },
    { q: 'Do I need a precise birth time?', a: 'Yes, especially for Brihat Kundli. Lagna changes roughly every two hours, and even a 15-minute improvement can sharpen house lordship and life-domain interpretation significantly.' },
    { q: 'Is the PDF download included?', a: 'Yes. Your complete Brihat Kundli PDF is included with the one-time purchase and remains available from your account after generation.' },
  ],
  banner: {
    kicker: 'Ready for the full life map?',
    title: 'Go beyond overview into a report you can keep for years.',
    body: 'Brihat Kundli Pro is built for people who want the most complete chart-based reading on the platform - not a teaser, but a full reference document.',
  },
};

export default function BrihatKundliLandingPage() {
  return <ModuleLandingPage config={config} />;
}
