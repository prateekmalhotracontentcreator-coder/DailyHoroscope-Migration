import React from 'react';
import { Card } from './ui/card';
import { Sparkles, Star } from 'lucide-react';

export const HoroscopeCard = ({ title, content, isLoading, type }) => {
  const typeStyles = {
    daily: 'border-gold/30',
    weekly: 'border-mustard/30',
    monthly: 'border-primary/30'
  };

  const typeIcons = {
    daily: <Star className="h-5 w-5" />,
    weekly: <Sparkles className="h-5 w-5" />,
    monthly: <Sparkles className="h-6 w-6" />
  };

  if (isLoading) {
    return (
      <Card className={`p-8 border-2 ${typeStyles[type]} bg-card min-h-[300px] flex flex-col items-center justify-center`}>
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <Star className="h-12 w-12 text-gold animate-pulse" />
            <Sparkles className="h-6 w-6 text-mustard absolute -top-1 -right-1 animate-pulse" style={{ animationDelay: '0.3s' }} />
          </div>
          <p className="text-lg font-playfair italic text-muted-foreground">
            Reading the stars...
          </p>
        </div>
      </Card>
    );
  }

  return (
    <Card className={`p-8 border-2 ${typeStyles[type]} bg-card hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.2)] transition-all duration-500`}>
      <div className="flex items-start space-x-3 mb-6">
        <div className="text-gold mt-1">{typeIcons[type]}</div>
        <h3 className="text-2xl md:text-3xl font-playfair font-semibold tracking-wide capitalize">
          {title}
        </h3>
      </div>
      <div className="prose prose-lg max-w-none">
        <p className="text-base md:text-lg leading-relaxed text-foreground/90 font-sans whitespace-pre-wrap">
          {content}
        </p>
      </div>
    </Card>
  );
};