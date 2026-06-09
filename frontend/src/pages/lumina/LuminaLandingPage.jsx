import React from 'react';

import ModuleLandingPage from '../../components/landing/ModuleLandingPage';

const config = {
  icon: '✦',
  accentColor: '#8b5cf6',
  badge: 'Multi-Faith Companion · Premium',
  headline: 'Scripture, manifestation, and sacred devotion - in one consecrated space.',
  subline: 'Lumina is your daily spiritual companion - Bible and Bhagavad Gita readings, manifestation confessions, devotion streaks, scripture-grounded AI chat, and a personal spiritual journal.',
  primaryCta: {
    label: 'Open Lumina',
    href: '/lumina',
  },
  secondaryCta: {
    label: "What's Inside",
  },
  seo: {
    title: 'Lumina - Bible, Bhagavad Gita & Spiritual Companion App',
    description: 'Your daily spiritual companion. Bible and Bhagavad Gita readings, manifestation confessions, devotion streaks, scripture-grounded AI chat, and a personal spiritual journal.',
    url: 'https://www.everydayhoroscope.in/the-lumina',
  },
  features: [
    { title: 'Bible & Bhagavad Gita Reader', body: 'Read from the full Bible or all 18 chapters of the Bhagavad Gita, with multiple translations available.' },
    { title: 'Manifestation Confessions', body: 'Speak affirmations aligned to scripture across healing, peace, prosperity, and spiritual authority themes.' },
    { title: 'Devotion Streaks & Rewards', body: 'Build daily practice streaks and earn devotion points redeemable for real-world rewards and gifted Premium time.' },
    { title: 'Scripture-Grounded AI Chat', body: 'Share what is on your heart and receive scripture-anchored guidance instead of generic self-help language.' },
    { title: 'Spiritual Journal', body: 'Record daily reflections, intentions, and scripture insights to build a personal spiritual archive over time.' },
    { title: 'Sacred Marketplace', body: 'Tools and resources for spiritual practice, curated and contextualised to the stage of practice you are in.' },
  ],
  steps: [
    { title: 'Choose your tradition', body: 'Begin with the Bible, Bhagavad Gita, or both. Lumina is built to hold both traditions with equal care.' },
    { title: 'Build your practice', body: 'Daily reading, manifestation confessions, devotion streaks, and journal entries become a steady living rhythm.' },
    { title: 'Grow in community and wisdom', body: 'Use scripture chat, track milestones, and earn rewards for consistency instead of approaching spiritual life only in crisis.' },
  ],
  preview: {
    title: 'Sample spiritual dashboard preview',
    subtitle: 'Lumina is designed like a companion space, not just a reading pane: scripture, practice, reflection, and support all live in one flow.',
    tabs: ['Home', 'Bible', 'Manifest', 'Devotion'],
    cards: [
      { title: 'Daily Verse', body: 'A focused scripture prompt tied to the part of practice you are building today.' },
      { title: 'Manifestation Track', body: 'Confessions, repetitions, and progress markers gathered into one daily practice panel.' },
      { title: 'Journal Entry', body: 'Private reflection space for what you noticed, asked, and learned in your practice.' },
    ],
    overlay: 'Premium - Open Lumina',
  },
  faqs: [
    { q: 'What makes Lumina different from a Bible app?', a: 'Lumina combines Bible and Bhagavad Gita reading, scripture-grounded AI chat, manifestation practice, devotion streaks, and journaling. It is built as a complete spiritual companion, not only as a text reader.' },
    { q: 'Which scriptures are supported?', a: 'The full Bible in multiple translations and the complete 18-chapter Bhagavad Gita in multiple editions are supported today, with more traditions planned.' },
    { q: 'Do I need to be religious to use Lumina?', a: 'No. Lumina is designed for people on a spiritual path of many kinds - faith-based, philosophical, devotional, or contemplative.' },
  ],
  banner: {
    kicker: 'Ready to build the practice?',
    title: 'Open the companion that keeps scripture and devotion in one place.',
    body: 'Lumina is strongest when it becomes part of a daily rhythm: reading, reflection, confession, and steady return.',
  },
};

export default function LuminaLandingPage() {
  return <ModuleLandingPage config={config} />;
}
