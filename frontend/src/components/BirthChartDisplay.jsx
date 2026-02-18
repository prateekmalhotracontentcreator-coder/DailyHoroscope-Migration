import React from 'react';
import { Card } from './ui/card';
import { Star, Sparkles } from 'lucide-react';

export const BirthChartDisplay = ({ report, isLoading, profile }) => {
  if (isLoading) {
    return (
      <Card className="p-8 border-2 border-gold/30 bg-card min-h-[400px] flex flex-col items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="relative">
            <Star className="h-16 w-16 text-gold animate-pulse" />
            <Sparkles className="h-8 w-8 text-mustard absolute -top-2 -right-2 animate-pulse" style={{ animationDelay: '0.3s' }} />
          </div>
          <p className="text-xl font-playfair italic text-muted-foreground text-center">
            Calculating planetary positions...
          </p>
        </div>
      </Card>
    );
  }

  if (!report) return null;

  return (
    <Card className="p-8 border-2 border-gold/30 bg-card">
      <div className="mb-6">
        <div className="flex items-center space-x-3 mb-2">
          <Star className="h-6 w-6 text-gold" />
          <h3 className="text-3xl font-playfair font-semibold">
            Birth Chart Analysis
          </h3>
        </div>
        {profile && (
          <p className="text-muted-foreground text-base">
            For {profile.name} • Born on {profile.date_of_birth} at {profile.time_of_birth} in {profile.location}
          </p>
        )}
      </div>

      <div className="prose prose-lg max-w-none">
        <div className="text-base md:text-lg leading-relaxed text-foreground/90 whitespace-pre-wrap">
          {report.report_content}
        </div>
      </div>
    </Card>
  );
};