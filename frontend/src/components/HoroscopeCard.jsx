import React from 'react';
import { Card } from './ui/card';
import { Sparkles, Star, Heart, Briefcase, Activity, Gem, Calendar } from 'lucide-react';

// Clean any residual markdown
const cleanMarkdown = (text) => {
  if (!text) return '';
  return text
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/#{1,6}\s?/g, '')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
};

// Parse structured horoscope into sections
// Handles the new prompt format: fixed headings on their own lines
const parseHoroscopeContent = (content) => {
  if (!content) return null;

  const cleaned = cleanMarkdown(content);

  // Extract sign name from first line if present (format: "Aries — ...")
  let signLine = '';
  let body = cleaned;
  const dashMatch = cleaned.match(/^([A-Za-z]+)\s*[—\-]+\s*(.*)/s);
  if (dashMatch) {
    signLine = dashMatch[1];
    body = dashMatch[2];
  }

  // Split on the 4 known section headings
  const SECTION_HEADINGS = [
    { key: 'love',    regex: /Love\s*[&and]+\s*Relationships\s*:/i,   title: 'Love & Relationships',  icon: 'heart',    color: 'pink'   },
    { key: 'career',  regex: /Career\s*[&and]+\s*Finances\s*:/i,      title: 'Career & Finances',     icon: 'briefcase',color: 'blue'   },
    { key: 'health',  regex: /Health\s*[&and]+\s*Wellness\s*:/i,       title: 'Health & Wellness',     icon: 'activity', color: 'green'  },
    { key: 'lucky',   regex: /Lucky\s*Elements?\s*:/i,                 title: 'Lucky Elements',        icon: 'gem',      color: 'purple' },
  ];

  const result = [];
  let remaining = body;

  // Extract general intro (text before first section heading)
  let introText = remaining;
  let earliestIdx = remaining.length;

  for (const sec of SECTION_HEADINGS) {
    const match = remaining.search(sec.regex);
    if (match !== -1 && match < earliestIdx) earliestIdx = match;
  }

  if (earliestIdx < remaining.length) {
    introText = remaining.substring(0, earliestIdx).trim();
    remaining = remaining.substring(earliestIdx);
  } else {
    // No structured sections found — return as single general block
    return [{
      title: 'Today\'s Reading',
      icon: 'star',
      color: 'gold',
      content: cleaned,
    }];
  }

  if (introText) {
    result.push({
      title: 'Overview',
      icon: 'star',
      color: 'gold',
      content: introText,
    });
  }

  // Extract each section
  for (let i = 0; i < SECTION_HEADINGS.length; i++) {
    const sec = SECTION_HEADINGS[i];
    const match = remaining.match(sec.regex);
    if (!match) continue;

    const start = remaining.search(sec.regex) + match[0].length;
    let end = remaining.length;

    // Find start of next section
    for (let j = i + 1; j < SECTION_HEADINGS.length; j++) {
      const nextMatch = remaining.search(SECTION_HEADINGS[j].regex);
      if (nextMatch !== -1 && nextMatch > start && nextMatch < end) {
        end = nextMatch;
      }
    }

    const sectionContent = remaining.substring(start, end).trim();
    if (sectionContent) {
      result.push({
        title: sec.title,
        icon: sec.icon,
        color: sec.color,
        content: sectionContent,
      });
    }
  }

  return result.length > 0 ? result : [{
    title: 'Today\'s Reading',
    icon: 'star',
    color: 'gold',
    content: cleaned,
  }];
};

const SectionIcon = ({ icon, className }) => {
  const icons = { star: Star, heart: Heart, briefcase: Briefcase, activity: Activity, gem: Gem };
  const Icon = icons[icon] || Star;
  return <Icon className={className} />;
};

const sectionColors = {
  gold: {
    bg: 'bg-amber-50/60 dark:bg-amber-950/30',
    border: 'border-amber-200 dark:border-amber-800',
    icon: 'text-amber-600 dark:text-amber-400',
    title: 'text-amber-800 dark:text-amber-300',
    iconBg: 'bg-amber-100 dark:bg-amber-900/50',
  },
  pink: {
    bg: 'bg-pink-50/60 dark:bg-pink-950/30',
    border: 'border-pink-200 dark:border-pink-800',
    icon: 'text-pink-600 dark:text-pink-400',
    title: 'text-pink-800 dark:text-pink-300',
    iconBg: 'bg-pink-100 dark:bg-pink-900/50',
  },
  blue: {
    bg: 'bg-blue-50/60 dark:bg-blue-950/30',
    border: 'border-blue-200 dark:border-blue-800',
    icon: 'text-blue-600 dark:text-blue-400',
    title: 'text-blue-800 dark:text-blue-300',
    iconBg: 'bg-blue-100 dark:bg-blue-900/50',
  },
  green: {
    bg: 'bg-emerald-50/60 dark:bg-emerald-950/30',
    border: 'border-emerald-200 dark:border-emerald-800',
    icon: 'text-emerald-600 dark:text-emerald-400',
    title: 'text-emerald-800 dark:text-emerald-300',
    iconBg: 'bg-emerald-100 dark:bg-emerald-900/50',
  },
  purple: {
    bg: 'bg-purple-50/60 dark:bg-purple-950/30',
    border: 'border-purple-200 dark:border-purple-800',
    icon: 'text-purple-600 dark:text-purple-400',
    title: 'text-purple-800 dark:text-purple-300',
    iconBg: 'bg-purple-100 dark:bg-purple-900/50',
  },
};

export const HoroscopeCard = ({ title, content, isLoading, type, signName, signSymbol }) => {
  const today = new Date();
  const formattedDate = today.toLocaleDateString('en-IN', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });

  if (isLoading) {
    return (
      <Card className="p-8 border border-gold/30 bg-card min-h-[300px] flex flex-col items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <Star className="h-12 w-12 text-gold animate-pulse" />
          <p className="text-lg font-playfair italic text-muted-foreground">
            Reading the cosmic energies...
          </p>
        </div>
      </Card>
    );
  }

  const sections = parseHoroscopeContent(content);

  return (
    <div className="space-y-5">
      {/* Sign heading */}
      {signName && (
        <div className="flex items-center gap-3 pb-2 border-b border-gold/20">
          <span className="text-3xl">{signSymbol}</span>
          <div>
            <h2 className="text-2xl font-playfair font-semibold">{signName}</h2>
            <p className="text-xs text-muted-foreground uppercase tracking-widest">
              {type === 'daily' ? 'Daily' : type === 'weekly' ? 'Weekly' : 'Monthly'} Horoscope
            </p>
          </div>
        </div>
      )}

      {/* Date bar */}
      <Card className="p-3 border border-gold/30 bg-gold/5">
        <div className="flex items-center justify-center gap-2">
          <Calendar className="h-4 w-4 text-gold" />
          <span className="text-sm font-medium text-amber-800 dark:text-amber-300">
            {formattedDate}
          </span>
        </div>
      </Card>

      {/* Sections grid */}
      {sections && sections.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {sections.map((section, index) => {
            const colors = sectionColors[section.color] || sectionColors.gold;
            const isFullWidth = index === 0;
            return (
              <Card
                key={index}
                className={`p-5 border ${colors.border} ${colors.bg} ${isFullWidth ? 'md:col-span-2' : ''}`}
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className={`p-1.5 rounded-sm ${colors.iconBg}`}>
                    <SectionIcon icon={section.icon} className={`h-4 w-4 ${colors.icon}`} />
                  </div>
                  <h4 className={`font-semibold text-sm uppercase tracking-wide ${colors.title}`}>
                    {section.title}
                  </h4>
                </div>
                <p className="text-sm leading-relaxed text-foreground/85">
                  {section.content}
                </p>
              </Card>
            );
          })}
        </div>
      ) : (
        <Card className="p-6 border border-gold/30">
          <p className="text-sm leading-relaxed">{cleanMarkdown(content)}</p>
        </Card>
      )}
    </div>
  );
};
