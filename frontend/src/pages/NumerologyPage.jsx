import React, { useState } from 'react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Hash } from 'lucide-react';

const getLifePathNumber = (dob) => {
  const digits = dob.replace(/-/g, '').split('').map(Number);
  let sum = digits.reduce((a, b) => a + b, 0);
  while (sum > 9 && sum !== 11 && sum !== 22 && sum !== 33) {
    sum = String(sum).split('').map(Number).reduce((a, b) => a + b, 0);
  }
  return sum;
};

const MEANINGS = {
  1:  'The Leader — Independent, pioneering, self-reliant. You are destined to forge your own path.',
  2:  'The Diplomat — Sensitive, cooperative, intuitive. You thrive in partnerships and bring harmony.',
  3:  'The Creator — Expressive, joyful, communicative. Your gift is inspiring others through creativity.',
  4:  'The Builder — Practical, disciplined, hardworking. You create lasting foundations.',
  5:  'The Adventurer — Freedom-loving, versatile, curious. Change and travel are your teachers.',
  6:  'The Nurturer — Responsible, caring, artistic. Family and community are your calling.',
  7:  'The Seeker — Analytical, spiritual, introspective. Truth and wisdom guide your journey.',
  8:  'The Achiever — Ambitious, authoritative, abundant. Material and spiritual power are yours to master.',
  9:  'The Humanitarian — Compassionate, idealistic, generous. You are here to serve the world.',
  11: 'Master Number 11 — The Illuminator. Highly intuitive spiritual messenger.',
  22: 'Master Number 22 — The Master Builder. Greatest potential for achievement.',
  33: 'Master Number 33 — The Master Teacher. Pure compassion and healing.',
};

const schema = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Vedic Numerology — Free Life Path Number Calculator',
  description: 'Calculate your Moolank (Life Path) and Bhagyank (Destiny) numbers using Vedic Numerology. Free online calculator rooted in ancient Indian Ankjyotish.',
  url: 'https://everydayhoroscope.in/numerology',
  publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: 'https://everydayhoroscope.in' },
  mainEntity: {
    '@type': 'SoftwareApplication',
    name: 'Vedic Numerology Calculator',
    applicationCategory: 'LifestyleApplication',
    operatingSystem: 'Web',
    offers: { '@type': 'Offer', price: '0', priceCurrency: 'INR' },
  },
};

export const NumerologyPage = () => {
  const [dob, setDob] = useState('');
  const [result, setResult] = useState(null);

  const calculate = () => {
    if (!dob) return;
    const num = getLifePathNumber(dob);
    setResult(num);
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-10">
      <SEO
        title="Vedic Numerology — Free Life Path Number Calculator"
        description="Calculate your Moolank (Life Path) and Bhagyank (Destiny) numbers using Vedic Numerology. Free instant calculator rooted in ancient Indian Ankjyotish."
        url="https://everydayhoroscope.in/numerology"
        schema={schema}
      />
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Hash className="h-3 w-3" /> Engine 4 · Vedic Numerology
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">Vedic Numerology</h1>
        <p className="text-muted-foreground">Discover your Moolank (Life Path) and Bhagyank (Destiny) numbers</p>
      </div>
      <Card className="p-6 border border-gold/20">
        <div className="mb-5">
          <label className="block text-sm font-medium mb-2">Date of Birth</label>
          <input
            type="date"
            value={dob}
            onChange={e => { setDob(e.target.value); setResult(null); }}
            className="w-full px-3 py-2.5 rounded-sm border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
          />
        </div>
        <Button onClick={calculate} disabled={!dob} className="w-full bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2">
          <Hash className="h-4 w-4" /> Calculate My Numbers
        </Button>
      </Card>
      {result && (
        <Card className="mt-6 p-6 border border-gold/30 bg-gold/5 text-center">
          <p className="text-xs text-gold uppercase tracking-widest mb-2">Your Moolank (Life Path Number)</p>
          <p className="text-6xl font-playfair font-bold text-gold mb-3">{result}</p>
          <p className="text-sm text-foreground font-medium mb-2">{MEANINGS[result]?.split('—')[0]}</p>
          <p className="text-sm text-muted-foreground">{MEANINGS[result]?.split('—')[1]}</p>
          <div className="mt-4 pt-4 border-t border-gold/20">
            <p className="text-xs text-muted-foreground">Full Numerology report with Bhagyank, Name Number, Lucky Years, Colours and Remedies — coming in the premium report suite.</p>
          </div>
        </Card>
      )}
    </div>
  );
};
