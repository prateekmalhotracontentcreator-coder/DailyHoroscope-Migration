import React from 'react';
import { Card } from './ui/card';
import { Sparkles, Star, Heart, Briefcase, Activity, Clover, Calendar } from 'lucide-react';

// Clean markdown formatting from text
const cleanMarkdown = (text) => {
  if (!text) return '';
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')  // Remove **bold**
    .replace(/\*([^*]+)\*/g, '$1')       // Remove *italic*
    .replace(/#{1,6}\s?/g, '')           // Remove headings
    .replace(/`([^`]+)`/g, '$1')         // Remove inline code
    .replace(/\n{3,}/g, '\n\n')          // Reduce multiple newlines
    .trim();
};

// Parse horoscope content into sections
const parseHoroscopeContent = (content) => {
  if (!content) return null;
  
  const cleanedContent = cleanMarkdown(content);
  const sections = [];
  
  // Define section patterns with their styling
  const sectionConfig = [
    { 
      patterns: ['love', 'relationship', 'romance', 'partner', 'heart'], 
      title: 'Love & Relationships', 
      icon: 'heart', 
      color: 'pink' 
    },
    { 
      patterns: ['career', 'work', 'finance', 'money', 'professional', 'business', 'job'], 
      title: 'Career & Finances', 
      icon: 'briefcase', 
      color: 'blue' 
    },
    { 
      patterns: ['health', 'wellness', 'energy', 'physical', 'mental', 'body', 'exercise'], 
      title: 'Health & Wellness', 
      icon: 'activity', 
      color: 'green' 
    },
    { 
      patterns: ['lucky', 'number', 'color', 'time', 'tip', 'advice'], 
      title: 'Lucky Elements & Tips', 
      icon: 'clover', 
      color: 'purple' 
    }
  ];

  // Split content by common section indicators
  const lines = cleanedContent.split('\n').filter(line => line.trim());
  
  let generalContent = [];
  let currentSection = null;
  let currentContent = [];

  for (const line of lines) {
    const lowerLine = line.toLowerCase();
    let foundNewSection = false;

    // Check if this line starts a new section
    for (const config of sectionConfig) {
      const isHeader = config.patterns.some(p => {
        const regex = new RegExp(`^[\\s]*[•\\-\\d\\.]*[\\s]*(${p})`, 'i');
        return regex.test(lowerLine) || 
               (lowerLine.includes(p) && (lowerLine.includes(':') || line.length < 60));
      });

      if (isHeader) {
        // Save previous section
        if (currentSection && currentContent.length > 0) {
          sections.push({
            ...currentSection,
            content: currentContent.join(' ').trim()
          });
        } else if (currentContent.length > 0) {
          generalContent.push(...currentContent);
        }

        currentSection = config;
        currentContent = [];
        
        // Extract content after colon if present
        const colonIndex = line.indexOf(':');
        if (colonIndex !== -1 && colonIndex < line.length - 1) {
          const afterColon = line.substring(colonIndex + 1).trim();
          if (afterColon) currentContent.push(afterColon);
        }
        foundNewSection = true;
        break;
      }
    }

    if (!foundNewSection) {
      currentContent.push(line.trim());
    }
  }

  // Save last section
  if (currentSection && currentContent.length > 0) {
    sections.push({
      ...currentSection,
      content: currentContent.join(' ').trim()
    });
  } else if (currentContent.length > 0) {
    generalContent.push(...currentContent);
  }

  // Create result with general prediction first
  const result = [];
  
  if (generalContent.length > 0 || sections.length === 0) {
    result.push({
      title: 'General Prediction',
      icon: 'star',
      color: 'gold',
      content: generalContent.length > 0 ? generalContent.join(' ').trim() : cleanedContent
    });
  }

  // Add other sections
  result.push(...sections);

  return result;
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
    bg: 'bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/40 dark:to-orange-950/40',
    border: 'border-amber-300 dark:border-amber-700',
    icon: 'text-amber-600 dark:text-amber-400',
    title: 'text-amber-800 dark:text-amber-300',
    iconBg: 'bg-amber-100 dark:bg-amber-900/50'
  },
  pink: {
    bg: 'bg-gradient-to-br from-pink-50 to-rose-50 dark:from-pink-950/40 dark:to-rose-950/40',
    border: 'border-pink-300 dark:border-pink-700',
    icon: 'text-pink-600 dark:text-pink-400',
    title: 'text-pink-800 dark:text-pink-300',
    iconBg: 'bg-pink-100 dark:bg-pink-900/50'
  },
  blue: {
    bg: 'bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/40 dark:to-indigo-950/40',
    border: 'border-blue-300 dark:border-blue-700',
    icon: 'text-blue-600 dark:text-blue-400',
    title: 'text-blue-800 dark:text-blue-300',
    iconBg: 'bg-blue-100 dark:bg-blue-900/50'
  },
  green: {
    bg: 'bg-gradient-to-br from-emerald-50 to-teal-50 dark:from-emerald-950/40 dark:to-teal-950/40',
    border: 'border-emerald-300 dark:border-emerald-700',
    icon: 'text-emerald-600 dark:text-emerald-400',
    title: 'text-emerald-800 dark:text-emerald-300',
    iconBg: 'bg-emerald-100 dark:bg-emerald-900/50'
  },
  purple: {
    bg: 'bg-gradient-to-br from-purple-50 to-violet-50 dark:from-purple-950/40 dark:to-violet-950/40',
    border: 'border-purple-300 dark:border-purple-700',
    icon: 'text-purple-600 dark:text-purple-400',
    title: 'text-purple-800 dark:text-purple-300',
    iconBg: 'bg-purple-100 dark:bg-purple-900/50'
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
      <Card className="p-4 border-2 border-gold/40 bg-gradient-to-r from-gold/15 via-amber-500/10 to-gold/15 shadow-sm">
        <div className="flex items-center justify-center space-x-3">
          <Calendar className="h-5 w-5 text-gold" />
          <span className="text-lg font-playfair font-semibold text-amber-800 dark:text-amber-300">
            {formattedDate}
          </span>
        </div>
      </Card>

      {/* Title */}
      <div className="flex items-center space-x-3 pb-2">
        <div className="p-2 rounded-lg bg-gold/20">
          <Star className="h-6 w-6 text-gold" />
        </div>
        <h3 className="text-2xl md:text-3xl font-playfair font-semibold tracking-wide">
          {title}
        </h3>
      </div>

      {/* Horoscope Sections */}
      {sections && sections.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {sections.map((section, index) => {
            const colors = sectionColors[section.color] || sectionColors.gold;
            const isFullWidth = index === 0 || section.content.length > 200;
            
            return (
              <Card 
                key={index}
                className={`p-6 border-2 ${colors.border} ${colors.bg} transition-all duration-300 hover:shadow-md ${
                  isFullWidth ? 'md:col-span-2' : ''
                }`}
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className={`p-2 rounded-lg ${colors.iconBg}`}>
                    <SectionIcon icon={section.icon} className={`h-5 w-5 ${colors.icon}`} />
                  </div>
                  <h4 className={`font-semibold text-lg ${colors.title}`}>
                    {section.title}
                  </h4>
                </div>
                <p className="text-base leading-relaxed text-foreground/90 font-normal">
                  {section.content}
                </p>
              </Card>
            );
          })}
        </div>
      ) : (
        <Card className="p-6 border-2 border-gold/30 bg-card">
          <p className="text-base leading-relaxed text-foreground/90">
            {cleanMarkdown(content)}
          </p>
        </Card>
      )}
    </div>
  );
};
