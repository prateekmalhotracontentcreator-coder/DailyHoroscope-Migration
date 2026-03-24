import React from 'react';
import { SEO } from '../components/SEO';
import { Gem, Sparkles } from 'lucide-react';

export const RemedyPage = () => (
  <div className="min-h-screen flex flex-col items-center justify-center px-4 py-20 text-center">
    <SEO
      title="Vedic Remedies — Coming Soon"
      description="Gemstones, Mantras, Yantras, Feng Shui, and Crystal Therapy — personalised Vedic remedies coming soon to Everyday Horoscope."
      url="https://everydayhoroscope.in/remedies"
    />
    <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-6">
      <Gem className="h-3 w-3" /> Vedic Remedies
    </div>
    <h1 className="font-playfair text-4xl font-semibold mb-4">Remedies</h1>
    <p className="text-muted-foreground max-w-md mb-3 text-lg">
      Gemstones, Mantras, Yantras, Feng Shui &amp; Crystal Therapy —
      personalised Vedic remedies are coming soon.
    </p>
    <p className="text-sm text-muted-foreground/60 flex items-center gap-1.5">
      <Sparkles className="h-3.5 w-3.5 text-gold/60" /> Sprint 2
    </p>
  </div>
);
