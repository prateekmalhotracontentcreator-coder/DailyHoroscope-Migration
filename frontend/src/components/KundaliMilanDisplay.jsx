import React from 'react';
import { Card } from './ui/card';
import { Heart, Sparkles, Star } from 'lucide-react';

export const KundaliMilanDisplay = ({ report, isLoading, person1, person2 }) => {
  if (isLoading) {
    return (
      <Card className="p-8 border-2 border-gold/30 bg-card min-h-[400px] flex flex-col items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <Heart className="h-16 w-16 text-gold animate-pulse" />
            <Sparkles className="h-8 w-8 text-mustard absolute -top-2 -right-2 animate-pulse" style={{ animationDelay: '0.3s' }} />
          </div>
          <p className="text-xl font-playfair italic text-muted-foreground text-center">
            Analyzing compatibility through the cosmic lens...
          </p>
        </div>
      </Card>
    );
  }

  if (!report) return null;

  const getScoreColor = (score) => {
    if (score >= 28) return 'text-green-600 dark:text-green-400';
    if (score >= 18) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-orange-600 dark:text-orange-400';
  };

  const getScoreLabel = (score) => {
    if (score >= 28) return 'Excellent Match';
    if (score >= 24) return 'Very Good Match';
    if (score >= 18) return 'Good Match';
    return 'Average Match';
  };

  return (
    <div className="space-y-6">
      {/* Score Card */}
      <Card className="p-8 border-2 border-gold bg-gradient-to-br from-card to-muted text-center">
        <div className="flex items-center justify-center mb-4">
          <Heart className="h-8 w-8 text-gold mr-3" />
          <h3 className="text-2xl font-playfair font-semibold">Compatibility Score</h3>
        </div>
        
        {person1 && person2 && (
          <p className="text-muted-foreground mb-6">
            {person1.name} & {person2.name}
          </p>
        )}
        
        <div className="flex items-center justify-center space-x-4 mb-4">
          <span className={`text-6xl font-playfair font-bold ${getScoreColor(report.compatibility_score)}`}>
            {report.compatibility_score}
          </span>
          <span className="text-3xl font-playfair text-muted-foreground">/ 36</span>
        </div>
        
        <div className="flex items-center justify-center space-x-2">
          <Star className="h-5 w-5 text-gold" />
          <span className="text-lg font-semibold text-gold">
            {getScoreLabel(report.compatibility_score)}
          </span>
        </div>
      </Card>

      {/* Detailed Analysis */}
      <Card className="p-8 border-2 border-gold/30 bg-card">
        <div className="mb-6">
          <h3 className="text-2xl font-playfair font-semibold mb-2">
            Detailed Compatibility Analysis
          </h3>
          <p className="text-muted-foreground text-sm">
            Based on Vedic Astrology & Ashtakoot Guna Milan System
          </p>
        </div>

        <div className="prose prose-lg max-w-none">
          <div className="text-base md:text-lg leading-relaxed text-foreground/90 whitespace-pre-wrap">
            {report.detailed_analysis}
          </div>
        </div>
      </Card>
    </div>
  );
};