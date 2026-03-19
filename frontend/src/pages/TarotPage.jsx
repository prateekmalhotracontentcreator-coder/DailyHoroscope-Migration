import React from 'react';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { BookOpen, Sparkles, Star } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const TarotPage = () => {
  const navigate = useNavigate();
  return (
    <div className="max-w-2xl mx-auto px-4 py-10 text-center">
      <SEO title="Tarot Reading — Everyday Horoscope" description="Free Tarot card reading powered by ancient symbolism and Vedic cross-reference. Discover what the cards and the stars say about your question." url="https://everydayhoroscope.in/tarot" />
      <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-6">
        <BookOpen className="h-3 w-3" /> Ancient Symbolism
      </div>
      <h1 className="text-3xl font-playfair font-semibold mb-3">Tarot Reading</h1>
      <p className="text-muted-foreground mb-8">What the cards AND the stars say about your question. Western Tarot interpreted through the lens of Vedic astrology — a combination no one else offers.</p>
      <div className="grid grid-cols-3 gap-3 mb-8">
        {['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor', 'The Hierophant'].map((card) => (
          <Card key={card} className="p-4 border border-gold/20 bg-gold/5 aspect-[2/3] flex flex-col items-center justify-center gap-2">
            <Star className="h-6 w-6 text-gold/40" />
            <p className="text-xs text-muted-foreground text-center">{card}</p>
          </Card>
        ))}
      </div>
      <Card className="p-6 border border-gold/30 bg-gold/5">
        <Sparkles className="h-8 w-8 text-gold mx-auto mb-3" />
        <p className="font-playfair text-lg font-semibold mb-2">Full Tarot Engine Coming Soon</p>
        <p className="text-sm text-muted-foreground mb-4">Daily card draw, 3-card spread, Celtic Cross — all cross-referenced with your Vedic birth chart for deeply personalised insights.</p>
        <Button onClick={() => navigate('/register')} className="bg-gold hover:bg-gold/90 text-primary-foreground">
          Get Notified at Launch
        </Button>
      </Card>
    </div>
  );
};
