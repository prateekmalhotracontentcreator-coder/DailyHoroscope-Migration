import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '⊕',
  accentColor: '#c5a059',
  badge: '₹799 one-time',
  headline: 'Every planet at the moment you were born placed itself somewhere for a reason.',
  subline: 'A full Vedic birth chart analysis - planetary positions, Dasha timing, career and wealth insights, and personalised remedies.',
  primaryCta: {
    label: 'Generate My Birth Chart - ₹799',
    href: '/birth-chart',
  },
  secondaryCta: {
    label: "See What's Included",
  },
  seo: {
    title: 'Vedic Birth Chart Analysis - Planetary Positions, Dasha & Remedies',
    description: 'Generate your personalised Vedic birth chart. All 9 planetary positions, Vimshottari Dasha timeline, career and wealth signals, and gemstone remedies. ₹799 one-time.',
    url: 'https://www.everydayhoroscope.in/the-birth-chart',
  },
  features: [
    { title: 'Ascendant & Lagna', body: 'Your rising sign and its lord - the foundation of your Vedic identity, health signposts, and physical constitution.' },
    { title: 'All 9 Planetary Positions', body: 'Sign, house, dignity, strength, and retrograde status for Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu.' },
    { title: 'Career & Wealth Signals', body: '10th house analysis, Dhana Yoga indicators, and the professional strengths written into your planetary placements.' },
    { title: 'Love & Relationships', body: '7th house lord analysis, compatible and challenging signs, and timing windows most favourable for partnership.' },
    { title: 'Vimshottari Dasha Timeline', body: 'Your current Mahadasha and Antardasha period - what planetary energy is governing your life right now and when it transitions.' },
    { title: 'Personalised Remedies', body: "Gemstone recommendations, Vedic mantras, and behavioural remedies calibrated to your chart's specific afflictions." },
  ],
  steps: [
    { title: 'Enter your birth details', body: 'Date of birth, time, and city. The more precise your birth time, the more accurate your Lagna and house cusps.' },
    { title: 'Swiss Ephemeris computes your chart', body: 'Planetary longitudes, house cusps, dignities, and Dasha balance calculated to sub-degree precision using pyswisseph.' },
    { title: 'Receive your Vedic Birth Chart', body: 'A full chart with planetary table, PDF download, and personalised interpretation across career, love, health, and wealth.' },
  ],
  preview: {
    title: 'Sample planetary table preview',
    subtitle: 'The unlocked report shows a complete planetary table, house placements, and interpretation blocks built from your exact birth moment.',
    columns: ['Planet', 'Sign', 'House', 'Status', 'Strength'],
    rows: [
      ['Sun', 'Taurus', '10th', 'Direct', 'High'],
      ['Moon', 'Cancer', '12th', 'Waxing', 'Medium'],
      ['Saturn', 'Aquarius', '7th', 'Own sign', 'High'],
    ],
    overlay: 'Premium - Unlock Full Chart',
  },
  faqs: [
    { q: 'What is a Vedic birth chart?', a: 'A Vedic birth chart is a Jyotish map of the sky at your birth using the sidereal zodiac and the Lagna, or rising sign, as the primary lens. It reads planets, houses, Dashas, and Yogas together rather than focusing only on a Sun sign profile.' },
    { q: 'How is this different from a Western birth chart?', a: 'Western astrology usually uses the tropical zodiac, while Vedic astrology uses the sidereal zodiac. Vedic analysis also includes Vimshottari Dasha periods - planetary time cycles that show when different parts of life become more active.' },
    { q: "What if I don't know my exact birth time?", a: 'Approximate time still gives meaningful planetary positions, but Lagna and house accuracy may reduce. If your birth time is unknown, Moon-based analysis can still reveal useful emotional and life-pattern insight.' },
  ],
  banner: {
    kicker: 'Ready to decode your chart?',
    title: 'Start with the exact sky you were born under.',
    body: 'Your Vedic chart is the foundation for career timing, relationship insight, and the remedies that actually match your planetary signature.',
  },
};

export default function BirthChartLandingPage() {
  return <ModuleLandingPage config={config} />;
}
