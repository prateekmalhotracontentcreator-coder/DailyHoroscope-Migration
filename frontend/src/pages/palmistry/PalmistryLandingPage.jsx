import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '◎',
  accentColor: '#c67444',
  badge: 'Vedic Palmistry · Premium',
  headline: "Your hand has been recording your life since birth. It's time to read what it says.",
  subline: 'A 12-question Vedic palmistry assessment - palm shape, major lines, mounts, and finger type - interpreted through Hasta Rekha tradition and AI analysis.',
  primaryCta: {
    label: 'Read My Palm',
    href: '/palmistry',
  },
  secondaryCta: {
    label: 'What We Analyse',
  },
  seo: {
    title: 'Palmistry Reading - Vedic Hasta Rekha Hand Analysis',
    description: 'A personalised Vedic palmistry reading. Answer 12 questions about your palm shape, major lines, mounts, and thumb type for a complete Hasta Rekha interpretation.',
    url: 'https://www.everydayhoroscope.in/the-palmistry',
  },
  features: [
    { title: 'Palm Shape & Element Type', body: "Earth, Air, Fire, or Water - your hand's elemental type sets the foundation for your character and life approach." },
    { title: 'Life, Heart & Head Lines', body: 'The three major lines analysed for length, depth, breaks, and forks - revealing vitality, emotional capacity, and intellectual style.' },
    { title: 'Fate Line Analysis', body: 'Present or absent, strong or faint - the Fate Line reveals career destiny, stability, and the role of external forces in your path.' },
    { title: 'Mount Dominance', body: 'Which planetary mount is most prominent - Jupiter, Saturn, Sun, Mercury, Venus, or Moon - and what it reveals about your dominant drive.' },
    { title: 'Thumb Character', body: 'Long or short, flexible or stiff, waisted or straight - the thumb is one of the most revealing features in Vedic palmistry.' },
    { title: 'Vedic Hasta Rekha Reading', body: 'A complete Hasta Rekha interpretation synthesising all 12 indicators into a coherent personalised reading in plain English.' },
  ],
  steps: [
    { title: 'Answer 12 questions about your hand', body: 'No photo upload required. Questions cover palm shape, major lines, mounts, finger type, and thumb form.' },
    { title: 'Hasta Rekha engine maps your signature', body: 'Your answers are translated into a palmistry profile using classical Vedic Hasta Rekha principles.' },
    { title: 'Receive your personalised reading', body: "Get a complete interpretation of your hand's signature, including strengths, challenges, and practical guidance." },
  ],
  preview: {
    title: 'Sample palmistry reading preview',
    subtitle: 'The unlocked reading turns your answers into a structured profile rather than a vague personality paragraph.',
    tabs: ['Life Line', 'Heart Line', 'Fate Line'],
    cards: [
      { title: 'Life Line', body: 'Vitality, stamina, and the way the body responds to stress and recovery.' },
      { title: 'Heart Line', body: 'Emotional style, affection patterns, and what intimacy asks of you.' },
      { title: 'Fate Line', body: 'Career direction, external pressure, and the degree of personal control over your path.' },
    ],
    overlay: 'Premium - Unlock Full Hasta Rekha Reading',
  },
  faqs: [
    { q: 'Do I need to upload a photo of my palm?', a: 'No. The assessment uses a 12-question format about observable hand features, so it works across devices without a photo upload.' },
    { q: 'How accurate is palmistry?', a: 'Hasta Rekha is a pattern-recognition tradition rather than a deterministic prediction engine. Accuracy improves when the hand features are answered carefully and honestly.' },
    { q: 'Which hand should I read?', a: 'For right-handed people, the dominant right hand usually reflects the active path and chosen life, while the left shows karmic tendency and inherited potential. The assessment asks for your dominant hand first.' },
  ],
  banner: {
    kicker: 'Ready to read your hand?',
    title: 'Answer the hand-shape questions and let the pattern speak.',
    body: 'This module works without a photo. What matters is careful observation of the palm features that Hasta Rekha has always treated as meaningful.',
  },
};

export default function PalmistryLandingPage() {
  return <ModuleLandingPage config={config} />;
}
