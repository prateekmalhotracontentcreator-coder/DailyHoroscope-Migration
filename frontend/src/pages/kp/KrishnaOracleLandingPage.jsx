import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '◉',
  accentColor: '#d4a843',
  badge: 'Vedic Oracle · Premium',
  headline: "Ask one question with complete sincerity. Krishna's grid will answer.",
  subline: 'An ancient Vedic oracle rooted in the Bhagavad Gita - 324-cell grid, 36 sacred answers, and live astrological fingerprinting from your natal chart.',
  primaryCta: {
    label: 'Enter the Oracle',
    href: '/krishna-prashnavali',
  },
  secondaryCta: {
    label: 'How It Works',
  },
  seo: {
    title: 'Krishna Prashnavali Oracle - Vedic Oracle Rooted in Bhagavad Gita',
    description: 'Ask the Krishna Prashnavali oracle your most sincere question. 324-cell Bhagavad Gita grid, 36 sacred answers, live Dasha fingerprinting, and sacred remedy for every reading.',
    url: 'https://www.everydayhoroscope.in/the-krishna-oracle',
  },
  features: [
    { title: '18×18 Bhagavad Gita Grid', body: '324 cells drawn from Srimad Bhagavad Gita. Your selection is guided by sincere intent - not by chance or random number.' },
    { title: 'Four Sacred Verdicts', body: "YES, WAIT, NO, and PRAY - each drawn from Krishna's teachings and matched to a specific chaupai." },
    { title: 'Live Dasha Fingerprinting', body: 'Every reading carries your Mahadasha and Antardasha overlay - the planetary energy governing you at the exact moment of your question.' },
    { title: 'Planetary Transit Overlay', body: 'Current transits of major planets are factored into your reading context, deepening the astrological resonance of each answer.' },
    { title: 'Sacred Remedy per Reading', body: "Each of the 36 answers carries its own module-specific sacred remedy and behavioural practice drawn from Lord Krishna's teachings." },
    { title: 'KP Birth Chart Analysis', body: 'Built-in Krishnamurti Paddhati chart panel - your full natal chart computed with Swiss Ephemeris to sub-degree precision.' },
  ],
  steps: [
    { title: 'Form your question', body: 'Hold your question clearly in mind. The more specific and sincere you are, the more precise the guidance becomes.' },
    { title: 'Select your cell on the grid', body: 'Choose from the 18×18 Bhagavad Gita grid. Your live Dasha and transits are already overlaid in the reading context.' },
    { title: 'Receive your verdict and remedy', body: 'One of 36 canonical answers appears with a sacred chaupai, its meaning, and a personalised remedy for your situation.' },
  ],
  preview: {
    title: 'Sample oracle verdict preview',
    subtitle: 'The live module reveals a sacred verdict card, contextual reading, and remedy action once the grid selection is made.',
    lines: [
      { label: 'Verdict', value: 'WAIT - Dhairya' },
      { label: 'Chaupai', value: 'Act only after the planetary window steadies and the heart becomes clear again.' },
      { label: 'Remedy', value: 'Offer one quiet act of devotion before taking the next outer step.' },
    ],
    overlay: 'Premium - Unlock Sacred Verdict',
  },
  faqs: [
    { q: 'What is Krishna Prashnavali?', a: 'Krishna Prashnavali is a traditional oracle rooted in Srimad Bhagavad Gita and Prashna Shastra. The 18×18 grid maps to 36 canonical answers, and the final selection is guided by intent rather than random generation.' },
    { q: 'How is this different from a regular online oracle?', a: "This oracle overlays your live Vedic Dasha, planetary transits, and Yogas onto the answer context. That means the verdict isn't just symbolic - it carries your astrological fingerprint in the moment you ask." },
    { q: 'What does PRAY mean as a verdict?', a: 'PRAY, or Bhakti, signals surrender and alignment before action. It is not a negative verdict - it means inner preparation, devotion, and the prescribed sacred remedy must come first.' },
  ],
  banner: {
    kicker: 'Ready to ask clearly?',
    title: "Enter the grid with one sincere question.",
    body: "The oracle is most powerful when the question is real, the intent is focused, and you're willing to receive a verdict that includes both answer and remedy.",
  },
};

export default function KrishnaOracleLandingPage() {
  return <ModuleLandingPage config={config} />;
}
