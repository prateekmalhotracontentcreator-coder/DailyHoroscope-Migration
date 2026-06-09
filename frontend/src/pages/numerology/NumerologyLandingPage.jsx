import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '∞',
  accentColor: '#3b82f6',
  badge: '11 Personalised Reports · Premium',
  headline: 'Your name and birth date carry a frequency. Numerology decodes it.',
  subline: '11 personalised Vedic numerology reports - Life Path, Name Correction, Career Guidance, Relationship Compatibility, Karmic Debt, and more.',
  primaryCta: {
    label: 'Generate My Numerology Report',
    href: '/numerology',
  },
  secondaryCta: {
    label: 'All 11 Reports',
  },
  seo: {
    title: 'Vedic Numerology Reports - Life Path, Name, Career & More',
    description: 'Generate 11 personalised Vedic numerology reports. Life Path, Name Correction, Karmic Debt, Relationship Compatibility, Career Guidance and the advanced Ankjyotish synthesis.',
    url: 'https://www.everydayhoroscope.in/the-numerology',
  },
  features: [
    { title: 'Life Path & Soul Mission', body: 'Your core number derived from your birth date - the foundational vibration shaping purpose, personality, and life trajectory.' },
    { title: 'Name Correction & Alignment', body: 'See whether your current name is in harmony with your birth number and where realignment is recommended.' },
    { title: 'Karmic Debt & Lo Shu Grid', body: 'Missing numbers in the Lo Shu Grid reveal karmic patterns that may need deliberate cultivation and correction.' },
    { title: 'Relationship Compatibility', body: 'Numerological compatibility between two birth dates across communication style, life-path harmony, and karmic overlap.' },
    { title: 'Career Guidance & Timing', body: 'Favourable years, career number cycles, and the vibrations best aligned to different professional paths.' },
    { title: 'Premium Ankjyotish Report', body: 'The advanced synthesis combines numerology with Lagna, Moon sign, and Nakshatra for a deeply personalised reading.' },
  ],
  steps: [
    { title: 'Choose your report type', body: 'Select from 11 report tiles based on what you want to understand. Most need only your birth name and date of birth.' },
    { title: 'Enter your details', body: 'The advanced Ankjyotish report also asks for birth time and city so Lagna and Nakshatra can be layered in.' },
    { title: 'Receive your personalised numerology report', body: 'The report is generated and saved to your account, with Premium members unlocking the full suite repeatedly.' },
  ],
  preview: {
    title: 'Sample Life Path preview',
    subtitle: 'The numerology module moves from a headline number into the deeper report layers that explain why that vibration shows up the way it does.',
    lines: [
      { label: 'Life Path', value: '7 - analysis, contemplation, inner discipline, and pattern recognition.' },
      { label: 'Name Alignment', value: 'Current spelling partially matches birth vibration, but career-facing expression could strengthen.' },
      { label: 'Next Focus', value: 'Personal year cycle emphasises study, refinement, and deliberate long-term planning.' },
    ],
    overlay: 'Premium - Unlock Report',
  },
  faqs: [
    { q: 'What is Vedic numerology?', a: 'Vedic numerology, or Ankjyotish, reads the vibrational significance of numbers 1 to 9 through a Vedic lens and gives greater weight to birth name alignment than most Western numerology apps do.' },
    { q: 'What is the difference between Pythagorean and Vedic numerology?', a: 'Pythagorean numerology uses a linear Latin-letter assignment. Vedic numerology uses Chaldean or Sanskrit-derived values, places stronger emphasis on name vibration, and in advanced forms integrates Lagna and Nakshatra.' },
    { q: 'What is the Ankjyotish report?', a: 'The Premium Ankjyotish report combines your numerology numbers with your Lagna, Moon sign, and birth Nakshatra, creating a synthesis that is tied to your full birth moment rather than date alone.' },
  ],
  banner: {
    kicker: 'Ready to decode the frequency?',
    title: 'Open the report that starts with numbers and ends with pattern.',
    body: 'Numerology becomes useful when it moves past one lucky number and into timing, compatibility, correction, and deeper synthesis.',
  },
};

export default function NumerologyLandingPage() {
  return <ModuleLandingPage config={config} />;
}
