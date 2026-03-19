import React from 'react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Layers, Sparkles, Camera } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const PalmistryPage = () => {
  const navigate = useNavigate();
  return (
    <div className="max-w-2xl mx-auto px-4 py-10 text-center">
      <SEO title="Hasta Rekha — Vedic Palmistry" description="India's first AI-powered Vedic palmistry. Analyse your palm lines, mounts, and hand shape through the lens of Samudrika Shastra — the ancient Indian science of body reading." url="https://everydayhoroscope.in/palmistry" />
      <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-6">
        <Layers className="h-3 w-3" /> Engine 5 · Samudrika Shastra
      </div>
      <h1 className="text-3xl font-playfair font-semibold mb-3">Hasta Rekha</h1>
      <p className="text-muted-foreground mb-3">Vedic Palmistry — Samudrika Shastra</p>
      <p className="text-sm text-muted-foreground mb-8 max-w-md mx-auto">India's first AI-powered Vedic palmistry analysis. Unlike Western palmistry, Samudrika Shastra connects your hand features directly to planetary mounts — giving astrological depth no other palmistry app offers.</p>
      <div className="grid grid-cols-2 gap-4 mb-8 text-left">
        {[
          { label: 'Heart Line', desc: 'Emotional nature and relationship patterns' },
          { label: 'Head Line', desc: 'Intelligence, logic, and communication style' },
          { label: 'Life Line', desc: 'Vitality, health, and major life changes' },
          { label: 'Fate Line', desc: 'Career path and life purpose' },
          { label: '7 Planetary Mounts', desc: 'Jupiter, Saturn, Sun, Mercury, Venus, Mars, Moon' },
          { label: 'Hand Shape', desc: 'Earth, Air, Fire, or Water — elemental personality' },
        ].map(item => (
          <Card key={item.label} className="p-4 border border-border">
            <p className="font-medium text-sm mb-1">{item.label}</p>
            <p className="text-xs text-muted-foreground">{item.desc}</p>
          </Card>
        ))}
      </div>
      <Card className="p-6 border border-gold/30 bg-gold/5">
        <Camera className="h-8 w-8 text-gold mx-auto mb-3" />
        <p className="font-playfair text-lg font-semibold mb-2">Phase 1 — Coming Soon</p>
        <p className="text-sm text-muted-foreground mb-4">Answer 10 questions about your hand features. Get a full Hasta Rekha report. Phase 2 adds palm photo upload with Claude Vision analysis.</p>
        <Button onClick={() => navigate('/register')} className="bg-gold hover:bg-gold/90 text-primary-foreground">
          Get Early Access
        </Button>
      </Card>
    </div>
  );
};
