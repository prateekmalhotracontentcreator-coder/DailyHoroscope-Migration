import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Button } from '../components/ui/button';
import { Sparkles, ArrowLeft, Clock } from 'lucide-react';

export const ComingSoonPage = ({ title = 'Coming Soon', subtitle = '', eta = 'Coming Soon' }) => {
  const navigate = useNavigate();
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center px-4 text-center">
      <SEO title={`${title} — Everyday Horoscope`} description={subtitle} />
      <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-6">
        <Clock className="h-3 w-3" /> {eta}
      </div>
      <Sparkles className="h-14 w-14 text-gold mx-auto mb-4 opacity-60" />
      <h1 className="text-3xl font-playfair font-semibold mb-3">{title}</h1>
      {subtitle && <p className="text-muted-foreground max-w-md mb-8">{subtitle}</p>}
      <p className="text-sm text-muted-foreground mb-8 max-w-sm">
        This feature is being built. Return soon for the full experience.
      </p>
      <Button onClick={() => navigate(-1)} variant="outline" className="border-gold/40 hover:border-gold gap-2">
        <ArrowLeft className="h-4 w-4" /> Go Back
      </Button>
    </div>
  );
};
