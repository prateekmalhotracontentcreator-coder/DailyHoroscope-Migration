import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '◈',
  accentColor: '#dc2626',
  badge: 'Vedic Remedies · Premium',
  headline: 'Every planet has a remedy. Your chart has a protocol.',
  subline: 'A personalised Vedic ritual prescription engine - planetary mantras, gemstones, fasting, and behavioural practices calibrated to your specific chart afflictions.',
  primaryCta: {
    label: 'Build My Ritual Protocol',
    href: '/ritual-engine',
  },
  secondaryCta: {
    label: 'What It Prescribes',
  },
  seo: {
    title: 'Ritual Engine - Personalised Vedic Remedies & Mantra Protocol',
    description: 'Get a personalised Vedic ritual protocol based on your birth chart - gemstone recommendations, planetary mantras, fasting calendar, and behavioural remedies.',
    url: 'https://www.everydayhoroscope.in/the-ritual-engine',
  },
  features: [
    { title: 'Planetary Affliction Scan', body: 'Identifies which planets are combust, debilitated, in enemy signs, or under low Shadbala - the root causes of repeated obstacles.' },
    { title: 'Gemstone Protocol', body: 'Traditional Vedic gemstone recommendations matched to your strongest benefic planets, with metal, weight, and finger guidance.' },
    { title: 'Mantra & Puja Guidance', body: 'Planet-specific mantras, count, timing, and devotional context for maximum ritual coherence.' },
    { title: 'Fasting Calendar', body: 'Auspicious fasting days derived from your chart's planetary dominants and current Dasha pattern.' },
    { title: 'Behavioural Remedies', body: 'Practical daily and weekly actions - charity, diet, direction, and conduct shifts that reinforce remediation.' },
    { title: 'Knowledge Engine Personalisation', body: 'Powered by EverydayHoroscope's Vedic Knowledge Engine and applied to your exact planetary signature.' },
  ],
  steps: [
    { title: 'Your chart is scanned for afflictions', body: 'Debilitated planets, combust planets, and Dosha indicators are identified across all 9 Vedic planets.' },
    { title: 'Ritual protocol is assembled', body: 'Gemstone, mantra, fasting, and behavioural remedies are selected from the Knowledge Engine and matched to your chart.' },
    { title: 'Follow your personalised protocol', body: 'Your remediation schedule arrives in a structured format you can begin using immediately.' },
  ],
  preview: {
    title: 'Sample remedy protocol preview',
    subtitle: 'The final protocol combines symbolic remedies with practical habits so the guidance is actionable instead of decorative.',
    lines: [
      { label: 'Planet', value: 'Saturn - active friction in discipline, work pressure, and delayed results.' },
      { label: 'Gemstone', value: 'Blue Sapphire - shown with timing and caution notes, not as blind advice.' },
      { label: 'Mantra', value: 'Om Sham Shanicharaya Namah - count, weekday, and devotional context included.' },
    ],
    overlay: 'Premium - Unlock Ritual Protocol',
  },
  faqs: [
    { q: 'What is the Ritual Engine?', a: 'It is a personalised Vedic remediation system that identifies planetary afflictions in your chart and prescribes specific remedies - mantras, gemstones, fasting, and behavioural actions - to address them.' },
    { q: 'Are gemstone recommendations safe to follow?', a: 'The engine follows classical Vedic rules and avoids recommending strengthening stones for clearly harmful planets without context. When uncertain, mantra and fasting-based remedies are the safer first layer.' },
    { q: 'How is this different from a generic remedies page?', a: 'Generic remedies are grouped by planet or sign. The Ritual Engine starts from your chart - which planets are afflicted, by how much, and in which houses - then builds a protocol from that personalised data.' },
  ],
  banner: {
    kicker: 'Ready to prescribe the remedy?',
    title: 'Let the chart tell you which ritual actually belongs to you.',
    body: 'The point is not to collect remedies. It is to follow the ones your chart is actually asking for right now.',
  },
};

export default function RitualEngineLandingPage() {
  return <ModuleLandingPage config={config} />;
}
