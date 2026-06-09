import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '◌',
  accentColor: '#2dd4bf',
  badge: 'Vedic Life Map · Premium',
  headline: '12 areas of your life. Each one rated, timed, and ready for action.',
  subline: 'Arc Angel reads your Vedic birth chart across all 12 life domains - with live Dasha timing and questionnaire-enhanced precision for each area.',
  primaryCta: {
    label: 'Open My Life Map',
    href: '/arc-angel',
  },
  secondaryCta: {
    label: 'The 12 Domains',
  },
  seo: {
    title: 'Arc Angel - Vedic 12 Areas of Life Analysis',
    description: 'Get a live Vedic reading across all 12 areas of your life - health, career, love, finances, spirituality, family and more - with Dasha timing for each domain.',
    url: 'https://www.everydayhoroscope.in/the-arc-angel',
  },
  features: [
    { title: 'Health & Fitness', body: "Your body's astrological constitution, vulnerability windows, and best practices based on the 1st and 6th houses." },
    { title: 'Career & Finances', body: "10th house career strength, 2nd and 11th house wealth signals, and the current Dasha's professional influence." },
    { title: 'Love & Family', body: '7th house partnership indicators, 5th house love potential, 4th house domestic harmony - all with timing overlays.' },
    { title: 'Spirituality & Purpose', body: '9th house dharma, 12th house moksha potential, and which planetary period is spiritually active for you right now.' },
    { title: 'Live Dasha Timing', body: 'Each of the 12 domains is rated in context of your current Mahadasha and Antardasha - not static, but live against your life calendar.' },
    { title: 'Questionnaire-Enhanced Precision', body: 'Complete the optional questionnaire to unlock deeper beta and gamma layer analysis for each life area.' },
  ],
  steps: [
    { title: 'Enter your birth details', body: 'Date, time, and city. Log in to save your profile and unlock all 12 domains as a living life map.' },
    { title: 'Arc Angel computes your life map', body: 'All 12 domains are rated from your Vedic chart with Dasha timing applied to each area.' },
    { title: 'Review your personalised guidance', body: 'Each domain shows a rating, current Dasha influence, and specific action guidance for this phase of life.' },
  ],
  preview: {
    title: 'Sample life-domain grid preview',
    subtitle: 'The full view presents a live dashboard of your chart translated into real life areas, each with current timing and practical guidance.',
    cards: [
      { title: 'Health', body: 'Current vitality score, active Dasha pressure, and body-care guidance.' },
      { title: 'Career', body: 'Professional momentum, pressure windows, and opportunity timing.' },
      { title: 'Love', body: 'Relationship climate, partnership timing, and emotional support signals.' },
    ],
    overlay: 'Premium - Unlock Full Life Map',
  },
  faqs: [
    { q: 'What are the 12 life domains?', a: 'Arc Angel maps your chart into health and fitness, career and work, finances, intellectual life, emotional life, spirituality, love and relationships, family life, social life, adventure and travel, environment, and creativity and hobbies.' },
    { q: 'How is Arc Angel different from a birth chart?', a: 'A birth chart shows planetary placements. Arc Angel turns those placements into 12 rated action domains with live Dasha timing, so you can see where attention is needed right now.' },
    { q: 'Does it update as my Dasha changes?', a: 'Yes. As Mahadasha and Antardasha periods change, the domain emphasis and guidance shift with them.' },
  ],
  banner: {
    kicker: 'Ready to see the full map?',
    title: 'Open the twelve-domain reading of your life.',
    body: 'Arc Angel is built for people who want their chart translated into action areas, not left as abstract symbolism.',
  },
};

export default function ArcAngelLandingPage() {
  return <ModuleLandingPage config={config} />;
}
