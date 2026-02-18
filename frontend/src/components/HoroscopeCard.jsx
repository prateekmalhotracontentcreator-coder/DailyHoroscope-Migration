import React from 'react';
import { Card } from './ui/card';
import { Sparkles, Star, Heart, Briefcase, Activity, Clover, Calendar } from 'lucide-react';

// Parse horoscope content into sections
const parseHoroscopeContent = (content) => {
  if (!content) return null;
  
  const sections = [];
  const lines = content.split('\n').filter(line => line.trim());
  
  let currentSection = { title: 'General Prediction', content: [], icon: 'star', color: 'gold' };
  
  const sectionPatterns = [
    { patterns: ['love', 'relationship', 'romance', 'partner'], title: 'Love & Relationships', icon: 'heart', color: 'pink' },
    { patterns: ['career', 'work', 'finance', 'money', 'professional', 'business'], title: 'Career & Finances', icon: 'briefcase', color: 'blue' },
    { patterns: ['health', 'wellness', 'energy', 'physical', 'mental'], title: 'Health & Wellness', icon: 'activity', color: 'green' },
    { patterns: ['lucky', 'number', 'color', 'time', 'tip'], title: 'Lucky Elements', icon: 'clover', color: 'purple' }
  ];
  
  for (const line of lines) {
    const lowerLine = line.toLowerCase();
    let foundSection = false;
    
    for (const pattern of sectionPatterns) {
      if (pattern.patterns.some(p => lowerLine.includes(p) && (lowerLine.includes(':') || line.length < 50))) {
        // Save current section if it has content
        if (currentSection.content.length > 0) {
          sections.push({ ...currentSection });
        }
        currentSection = { title: pattern.title, content: [], icon: pattern.icon, color: pattern.color };
        
        // If the line has content after a colon, add it
        const colonIndex = line.indexOf(':');
        if (colonIndex !== -1 && colonIndex < line.length - 1) {
          currentSection.content.push(line.substring(colonIndex + 1).trim());
        }
        foundSection = true;
        break;
      }
    }
    
    if (!foundSection) {
      currentSection.content.push(line);
    }
  }
  
  // Add last section
  if (currentSection.content.length > 0) {
    sections.push(currentSection);
  }
  
  // If no sections were parsed, return the whole content as general
  if (sections.length === 0) {
    return [{ title: 'Your Horoscope', content: [content], icon: 'star', color: 'gold' }];
  }
  
  return sections;
};

const SectionIcon = ({ icon, className }) => {
  const icons = {
    star: Star,
    heart: Heart,
    briefcase: Briefcase,
    activity: Activity,
    clover: Clover
  };
  const Icon = icons[icon] || Star;
  return <Icon className={className} />;
};

const sectionColors = {
  gold: {
    bg: 'bg-gradient-to-br from-amber-50 to-yellow-50 dark:from-amber-950/30 dark:to-yellow-950/30',
    border: 'border-amber-200 dark:border-amber-800',
    icon: 'text-amber-500',
    title: 'text-amber-700 dark:text-amber-400'
  },
  pink: {
    bg: 'bg-gradient-to-br from-pink-50 to-rose-50 dark:from-pink-950/30 dark:to-rose-950/30',
    border: 'border-pink-200 dark:border-pink-800',
    icon: 'text-pink-500',
    title: 'text-pink-700 dark:text-pink-400'
  },
  blue: {
    bg: 'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30',
    border: 'border-blue-200 dark:border-blue-800',
    icon: 'text-blue-500',
    title: 'text-blue-700 dark:text-blue-400'
  },
  green: {
    bg: 'bg-gradient-to-br from-emerald-50 to-green-50 dark:from-emerald-950/30 dark:to-green-950/30',
    border: 'border-emerald-200 dark:border-emerald-800',
    icon: 'text-emerald-500',
    title: 'text-emerald-700 dark:text-emerald-400'
  },
  purple: {
    bg: 'bg-gradient-to-br from-purple-50 to-violet-50 dark:from-purple-950/30 dark:to-violet-950/30',
    border: 'border-purple-200 dark:border-purple-800',
    icon: 'text-purple-500',
    title: 'text-purple-700 dark:text-purple-400'
  }
};

export const HoroscopeCard = ({ title, content, isLoading, type, selectedSign }) => {
  const today = new Date();
  const formattedDate = today.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  if (isLoading) {
    return (
      <Card className="p-8 border-2 border-gold/30 bg-card min-h-[300px] flex flex-col items-center justify-center">
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

  const sections = parseHoroscopeContent(content);

  return (
    <div className="space-y-6">
      {/* Date Header */}
      <Card className="p-4 border-2 border-gold/30 bg-gradient-to-r from-gold/10 to-amber-500/10">
        <div className="flex items-center justify-center space-x-3">
          <Calendar className="h-5 w-5 text-gold" />
          <span className="text-lg font-playfair font-semibold text-gold">{formattedDate}</span>
        </div>
      </Card>

      {/* Title */}
      <div className="flex items-center space-x-3">
        <Star className="h-6 w-6 text-gold" />
        <h3 className="text-2xl md:text-3xl font-playfair font-semibold tracking-wide">
          {title}
        </h3>
      </div>

      {/* Horoscope Sections */}
      {sections && sections.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sections.map((section, index) => {
            const colors = sectionColors[section.color] || sectionColors.gold;
            return (
              <Card 
                key={index}
                className={`p-5 border-2 ${colors.border} ${colors.bg} transition-all duration-300 hover:shadow-lg ${
                  index === 0 ? 'md:col-span-2' : ''
                }`}
              >
                <div className="flex items-center space-x-2 mb-3">
                  <SectionIcon icon={section.icon} className={`h-5 w-5 ${colors.icon}`} />
                  <h4 className={`font-semibold ${colors.title}`}>{section.title}</h4>
                </div>
                <p className="text-sm md:text-base leading-relaxed text-foreground/85">
                  {section.content.join(' ')}
                </p>
              </Card>
            );
          })}
        </div>
      ) : (
        <Card className="p-6 border-2 border-gold/30 bg-card">
          <p className="text-base md:text-lg leading-relaxed text-foreground/90 whitespace-pre-wrap">
            {content}
          </p>
        </Card>
      )}
    </div>
  );
};
