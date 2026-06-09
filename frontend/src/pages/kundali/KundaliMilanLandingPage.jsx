import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '⚭',
  accentColor: '#e07080',
  badge: '₹999 one-time',
  headline: 'Before the wedding, ask the stars what they already know about you two.',
  subline: 'The classical Ashtakoot Guna Milan analysis - 36 compatibility points, Mangal Dosha assessment, and personalised remedies for both charts.',
  primaryCta: {
    label: 'Get Kundali Milan - ₹999',
    href: '/kundali-milan',
  },
  secondaryCta: {
    label: "See What's Included",
  },
  seo: {
    title: 'Kundali Milan - Vedic Marriage Compatibility Report',
    description: 'Classical Ashtakoot Guna Milan compatibility analysis for marriage. 36-point score, Mangal Dosha assessment, auspicious dates, and personalised remedies. ₹999 one-time.',
    url: 'https://www.everydayhoroscope.in/the-kundali-milan',
  },
  features: [
    { title: '36-Point Guna Milan', body: 'All 8 Kootas scored and explained with a total compatibility verdict across the classical Ashtakoot system.' },
    { title: 'Mangal Dosha Assessment', body: 'Both charts analysed for Mangal Dosha - identified, rated by severity, and remedied where applicable.' },
    { title: 'Both North Indian Charts', body: 'Full chart SVG for both persons - planetary positions and house placements side by side.' },
    { title: 'Relationship Strengths', body: 'The Koota scores that favour your partnership - communication, temperament alignment, sexual compatibility, and longevity indicators.' },
    { title: 'Auspicious Wedding Dates', body: 'Muhurat guidance for the most favourable dates based on combined chart analysis.' },
    { title: 'Personalised Dosha Remedies', body: 'Specific mantra, gemstone, and ritual remedies for any Doshas identified in either chart.' },
  ],
  steps: [
    { title: 'Enter birth details for both persons', body: 'Date, time, and city for Person 1 and Person 2. Both sets of details are needed for a full compatibility read.' },
    { title: 'Vedic engine computes both charts', body: 'Ashtakoot scoring, Mangal Dosha identification, planetary positions, and Muhurat windows are calculated together.' },
    { title: 'Receive your Kundali Milan report', body: 'A full compatibility analysis with PDF download, Dosha remedies, and marriage timing guidance.' },
  ],
  preview: {
    title: 'Sample compatibility scorecard',
    subtitle: 'The unlocked report shows a Koota table, combined verdict, and detailed explanations of what supports the match and what needs remedy.',
    columns: ['Koota', 'Score', 'Max', 'Reading'],
    rows: [
      ['Varna', '1', '1', 'Strong alignment'],
      ['Graha Maitri', '4', '5', 'Mostly supportive'],
      ['Nadi', '8', '8', 'Clear match'],
      ['Total', '27', '36', 'Good compatibility'],
    ],
    overlay: 'Premium - Unlock Full Milan Report',
  },
  faqs: [
    { q: 'What is Guna Milan?', a: 'Guna Milan is the traditional Ashtakoot compatibility system used in Vedic marriage matching. It evaluates eight qualities across both charts and assigns a score out of 36, with the full score read alongside Doshas and cancellation factors.' },
    { q: 'What score is considered a good match?', a: 'Traditionally, 18 to 24 is considered acceptable, 24 to 32 is strong, and 32 plus is excellent. Score alone is not final, because Nadi Dosha, Mangal Dosha, benefic aspects, and cancellations can significantly change the outcome.' },
    { q: 'What happens if Mangal Dosha is present?', a: 'Mangal Dosha is common and often manageable. The report checks severity, mutual cancellation, Jupiter or Venus protections, and gives remedies where the Dosha still matters.' },
  ],
  banner: {
    kicker: 'Ready to check the match?',
    title: 'Read the marriage promise before the ceremony begins.',
    body: 'Kundali Milan helps you see the strengths, pressure points, and remedy pathways in a relationship before major decisions are made.',
  },
};

export default function KundaliMilanLandingPage() {
  return <ModuleLandingPage config={config} />;
}
