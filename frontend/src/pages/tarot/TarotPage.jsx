import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { SEO } from '../../components/SEO';
import { PremiumGateCard } from '../../components/PremiumRoute';
import { Card } from '../../components/ui/card';
import { Button } from '../../components/ui/button';
import { Drawer } from 'vaul';
import {
  BookOpen, Sparkles, Star, Loader2,
  Bookmark, BookmarkCheck, Zap, Crown, RotateCcw, NotebookPen, Flame,
  X, Share2, Eye, Heart, Briefcase, Moon, Brain, ChevronRight,
} from 'lucide-react';
import axios from 'axios';
import { toast } from 'sonner';
import { safeClaimPunyaAction } from '../../lib/punyaRewards';

const API  = `${process.env.REACT_APP_BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const FOCUS_AREAS = [
  { value: 'guidance', label: 'Guidance', emoji: '🔮', planet: 'Rahu/Ketu insight', Icon: Eye },
  { value: 'love',     label: 'Love',     emoji: '❤️', planet: 'Venus (Shukra) energy', Icon: Heart },
  { value: 'career',   label: 'Career',   emoji: '⭐', planet: 'Saturn (Shani) karma', Icon: Briefcase },
  { value: 'healing',  label: 'Healing',  emoji: '🌿', planet: 'Moon (Chandra) nourishment', Icon: Moon },
  { value: 'clarity',  label: 'Clarity',  emoji: '✨', planet: 'Mercury (Budha) wisdom', Icon: Brain },
];

const WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

const schema = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Tarot Card Reading -- Vedic Cross-Reference',
  description: 'Daily Tarot card draw and premium spreads, cross-referenced with Vedic astrology.',
  url: `${SITE}/tarot`,
  publisher: { '@type': 'Organization', name: 'Everyday Horoscope', url: SITE },
};

function TarotV4Styles() {
  return (
    <style>{`
      @keyframes tarotBurst {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.25); }
        18% { opacity: 1; }
        100% { opacity: 0; transform: translate(calc(-50% + var(--tx)), calc(-50% + var(--ty))) scale(1); }
      }
      @keyframes tarotGlow {
        0% { box-shadow: 0 0 0 rgba(197,160,89,0); }
        20% { box-shadow: 0 0 32px rgba(197,160,89,0.65); }
        100% { box-shadow: 0 0 0 rgba(197,160,89,0); }
      }
      @keyframes tarotFloat {
        0%, 100% { transform: translateY(0); opacity: 0.35; }
        50% { transform: translateY(-10px); opacity: 0.9; }
      }
      @keyframes tarotFadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .tarot-burst-dot {
        animation: tarotBurst 650ms ease-out forwards;
      }
      .tarot-reveal-glow {
        animation: tarotGlow 1100ms ease-out;
      }
      .tarot-fade-up {
        animation: tarotFadeUp 420ms ease-out both;
      }
      .tarot-star {
        animation: tarotFloat var(--dur) ease-in-out infinite;
        animation-delay: var(--delay);
      }
    `}</style>
  );
}

const getCardKeywords = (card, fallbackFocus = 'guidance') => {
  if (!card) return [];
  if (Array.isArray(card.keywords) && card.keywords.length) return card.keywords.slice(0, 5);
  const seeds = [card.arcana, card.suit, card.orientation, fallbackFocus, card.position_label]
    .filter(Boolean)
    .map(v => String(v).replace(/_/g, ' '));
  return [...new Set(seeds)].slice(0, 5);
};

const getCardMeaning = (card, reading) => {
  if (!card) return '';
  return card.meaning || card.meaning_full || card.full_meaning || card.interpretation ||
    reading?.guidance || card.meaning_snippet || 'The card opens a reflective message for this moment.';
};

const getReadingGuidance = (reading, card) => {
  return reading?.guidance || reading?.interpretation || card?.guidance ||
    'Pause before acting. Let the card name one practical step, one feeling to honor, and one pattern to release today.';
};

const getCardDate = (item) => {
  if (!item?.created_at) return '';
  return new Date(item.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
};

const getMonthLabel = (item) => {
  if (!item?.created_at) return 'Earlier';
  return new Date(item.created_at).toLocaleDateString('en-IN', { month: 'long', year: 'numeric' });
};

const computeStreakStats = (history = [], gamification) => {
  const dateSet = new Set(
    history
      .map(item => item.created_at ? new Date(item.created_at).toISOString().slice(0, 10) : null)
      .filter(Boolean),
  );
  const today = new Date();
  let streak = Number(gamification?.daily_streak || 0);
  if (!streak) {
    for (let i = 0; i < 60; i++) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      if (dateSet.has(d.toISOString().slice(0, 10))) streak += 1;
      else if (i > 0) break;
    }
  }
  const weekFilled = WEEK_DAYS.map((_, index) => {
    const d = new Date(today);
    const mondayOffset = (today.getDay() + 6) % 7;
    d.setDate(today.getDate() - mondayOffset + index);
    return dateSet.has(d.toISOString().slice(0, 10));
  });
  const xp = Number(gamification?.total_xp || gamification?.xp || 0);
  const xpProgress = Math.min(100, Number(gamification?.level_progress || xp % 100));
  return { streak, weekFilled, xpProgress, level: gamification?.level || Math.floor(xp / 100) + 1 };
};

// ── Card visuals ────────────────────────────────────────────────────────────

function CardBack({ className = '' }) {
  return (
    <div className={`aspect-[2/3] rounded-xl border border-gold/30 bg-gradient-to-b from-neutral-900 to-neutral-950 flex items-center justify-center ${className}`}>
      <div className="w-12 h-12 rounded-full border border-gold/30 flex items-center justify-center">
        <Star className="h-5 w-5 text-gold/30" />
      </div>
    </div>
  );
}

function CardFace({ svgData, cardName, orientation, className = '' }) {
  if (!svgData) {
    return (
      <div className={`aspect-[2/3] rounded-xl bg-gold/5 border border-gold/20 flex items-center justify-center ${className}`}>
        <Star className="h-6 w-6 text-gold/30" />
      </div>
    );
  }
  const svgUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgData)}`;
  return (
    <div className={`aspect-[2/3] rounded-xl overflow-hidden ${orientation === 'reversed' ? 'rotate-180' : ''} ${className}`}>
      <img src={svgUrl} alt={cardName} className="w-full h-full object-cover" />
    </div>
  );
}

function FlippingCard({ cardId, cardName, orientation, svgData, flipped, onClick }) {
  // w-40 = 160px → height = 160 × 3/2 = 240px
  const particles = [
    [-56, -42], [-24, -64], [18, -58], [52, -34],
    [66, 4], [46, 42], [12, 64], [-28, 58],
    [-62, 22], [-70, -12], [0, -78], [74, -58],
    [82, 34], [-82, 38],
  ];
  return (
    <button
      type="button"
      onClick={onClick}
      className={`relative block w-40 mx-auto ${flipped && onClick ? 'cursor-pointer' : 'cursor-default'}`}
      style={{ perspective: '1200px' }}
      aria-label={flipped ? `Open details for ${cardName}` : 'Tarot card'}
    >
      {flipped && particles.map(([tx, ty], index) => (
        <span
          key={`${cardId || cardName}-${index}`}
          className="tarot-burst-dot pointer-events-none absolute left-1/2 top-1/2 z-20 h-1.5 w-1.5 rounded-full bg-gold"
          style={{
            '--tx': `${tx}px`,
            '--ty': `${ty}px`,
            animationDelay: `${index * 18}ms`,
          }}
        />
      ))}
      <div
        className={`relative transition-all duration-700 ${flipped ? 'tarot-reveal-glow rounded-xl' : ''}`}
        style={{ transformStyle: 'preserve-3d', transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)', height: '240px' }}
      >
        <div className="absolute inset-0" style={{ backfaceVisibility: 'hidden' }}>
          <CardBack />
        </div>
        <div className="absolute inset-0" style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}>
          <CardFace svgData={svgData} cardName={cardName} orientation={orientation} />
        </div>
      </div>
    </button>
  );
}

function OrientationBadge({ orientation }) {
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
      orientation === 'upright' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-orange-500/10 text-orange-400'
    }`}>
      {orientation === 'upright' ? '↑ Upright' : '↓ Reversed'}
    </span>
  );
}

function TarotHero({ onDrawClick }) {
  const stars = Array.from({ length: 52 }, (_, index) => ({
    left: `${(index * 37) % 100}%`,
    top: `${(index * 53) % 78}%`,
    dur: `${3 + (index % 5)}s`,
    delay: `${(index % 9) * 0.35}s`,
  }));
  return (
    <section className="relative mb-8 overflow-hidden rounded-3xl border border-gold/20 bg-gradient-to-br from-neutral-950 via-purple-950/20 to-neutral-950 px-5 py-10 text-center shadow-2xl shadow-black/20">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_20%,rgba(197,160,89,0.18),transparent_32%),radial-gradient(circle_at_15%_80%,rgba(232,201,122,0.10),transparent_24%)]" />
      {stars.map((star, index) => (
        <span
          key={index}
          className="tarot-star absolute h-0.5 w-0.5 rounded-full bg-white/80"
          style={{ left: star.left, top: star.top, '--dur': star.dur, '--delay': star.delay }}
        />
      ))}
      <div className="relative z-10 mx-auto max-w-xl">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full border border-gold/40 bg-gold/10 px-4 py-1.5 text-[11px] font-semibold uppercase tracking-[0.32em] text-gold">
          <Sparkles className="h-3.5 w-3.5" /> Vedic Tarot
        </div>
        <h1 className="font-playfair text-4xl font-semibold tracking-tight text-white md:text-6xl">
          The Cards Know
        </h1>
        <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-white/70 md:text-base">
          Draw your card. Receive your message. Trust the cosmos.
        </p>
        <div className="group relative mx-auto mt-8 h-36 w-64">
          <div className="absolute left-10 top-3 w-24 origin-bottom -rotate-8 translate-x-[-10px] transition-transform duration-300 group-hover:-translate-x-8 group-hover:-rotate-12">
            <CardBack className="shadow-xl shadow-black/40" />
          </div>
          <div className="absolute left-20 top-0 z-10 w-24 transition-transform duration-300 group-hover:-translate-y-2">
            <CardBack className="shadow-xl shadow-gold/10" />
          </div>
          <div className="absolute right-10 top-3 w-24 origin-bottom rotate-8 translate-x-[10px] transition-transform duration-300 group-hover:translate-x-8 group-hover:rotate-12">
            <CardBack className="shadow-xl shadow-black/40" />
          </div>
        </div>
        <Button
          onClick={onDrawClick}
          className="mt-2 bg-gold px-6 py-5 text-sm font-semibold text-primary-foreground hover:bg-gold/90"
        >
          Draw Today's Card <ChevronRight className="ml-1 h-4 w-4" />
        </Button>
      </div>
    </section>
  );
}

function FocusAreaCards({ value, onChange }) {
  return (
    <div className="grid grid-cols-2 gap-2 md:grid-cols-5">
      {FOCUS_AREAS.map(({ value: itemValue, label, emoji, planet, Icon }) => {
        const selected = value === itemValue;
        return (
          <button
            key={itemValue}
            type="button"
            onClick={() => onChange(itemValue)}
            className={`rounded-xl border p-3 text-left transition-all duration-200 hover:scale-[1.02] ${
              selected
                ? 'border-gold bg-gold/10 text-foreground shadow-sm shadow-gold/10'
                : 'border-border bg-card/70 text-muted-foreground hover:border-gold/50'
            }`}
          >
            <div className="mb-2 flex items-center justify-between">
              <span className="text-2xl">{emoji}</span>
              <Icon className={`h-4 w-4 ${selected ? 'text-gold' : 'text-muted-foreground/60'}`} />
            </div>
            <p className="text-sm font-semibold text-foreground">{label}</p>
            <p className="mt-1 text-[11px] leading-4 text-muted-foreground">{planet}</p>
          </button>
        );
      })}
    </div>
  );
}

function StreakWidget({ history, gamification }) {
  const stats = computeStreakStats(history, gamification);
  return (
    <Card className="mb-5 overflow-hidden border border-gold/20 bg-gold/[0.04] p-4">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <div className="flex items-center gap-2">
            <Flame className="h-4 w-4 text-orange-500" />
            <p className="text-sm font-semibold">
              {stats.streak >= 3 ? `${stats.streak}-day streak!` : `${stats.streak || 0}-day Tarot rhythm`}
            </p>
          </div>
          <p className="mt-1 text-xs text-muted-foreground">Return daily to keep your oracle thread alive.</p>
        </div>
        <div className="flex items-center gap-1.5">
          {WEEK_DAYS.map((day, index) => (
            <div key={day} className="text-center">
              <div className={`mx-auto mb-1 flex h-7 w-7 items-center justify-center rounded-full border text-[10px] font-semibold transition-transform ${
                stats.weekFilled[index] ? 'scale-105 border-gold bg-gold text-primary-foreground' : 'border-gold/20 bg-background text-muted-foreground'
              }`}>
                {day.slice(0, 1)}
              </div>
              <span className="text-[10px] text-muted-foreground">{day}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="mt-4">
        <div className="mb-1 flex items-center justify-between text-[11px] text-muted-foreground">
          <span>Level {stats.level}</span>
          <span>{Math.round(stats.xpProgress)}% to next level</span>
        </div>
        <div className="h-2 rounded-full bg-muted/50">
          <div className="h-full rounded-full bg-gold transition-all duration-500" style={{ width: `${stats.xpProgress}%` }} />
        </div>
      </div>
    </Card>
  );
}

function FadeInOnView({ children, delay = 0 }) {
  const ref = useRef(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return undefined;
    if (!('IntersectionObserver' in window)) {
      setVisible(true);
      return undefined;
    }
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setVisible(true);
        observer.disconnect();
      }
    }, { threshold: 0.16 });
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`transition-all duration-500 ${visible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
}

function ReadingDetailsContent({ card, reading, svgData, onShare }) {
  const keywords = getCardKeywords(card, reading?.focus_area);
  return (
    <div className="grid gap-6 md:grid-cols-[0.8fr_1.2fr]">
      <div>
        <CardFace svgData={svgData} cardName={card?.name} orientation={card?.orientation} className="mx-auto max-w-[240px] shadow-2xl shadow-black/40" />
      </div>
      <div className="space-y-4">
        <div>
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <h2 className="font-playfair text-3xl font-semibold">{card?.name || 'Your Card'}</h2>
            {card?.orientation && <OrientationBadge orientation={card.orientation} />}
          </div>
          <p className="text-sm leading-7 text-muted-foreground">{getCardMeaning(card, reading)}</p>
        </div>
        {keywords.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {keywords.map(keyword => (
              <span key={keyword} className="rounded-full border border-gold/20 bg-gold/10 px-2.5 py-1 text-xs capitalize text-gold">
                {keyword}
              </span>
            ))}
          </div>
        )}
        <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-4">
          <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-gold">Vedic Cross-Reference</p>
          <p className="text-sm leading-6 text-muted-foreground">
            Read this card as a mirror for your current karma: the symbol speaks first, then your focus area and timing reveal where its energy wants expression.
          </p>
        </div>
        {reading?.affirmation && (
          <blockquote className="border-l-4 border-gold bg-gold/5 px-4 py-3 font-playfair text-base italic">
            "{reading.affirmation}"
          </blockquote>
        )}
        <div>
          <p className="mb-1 text-xs font-semibold uppercase tracking-widest text-muted-foreground">How to apply this today</p>
          <p className="text-sm leading-7">{getReadingGuidance(reading, card)}</p>
        </div>
        <Button onClick={onShare} variant="outline" className="border-gold/30 text-gold hover:bg-gold/10">
          <Share2 className="mr-2 h-4 w-4" /> Share Reading
        </Button>
      </div>
    </div>
  );
}

function ReadingModal({ open, onClose, card, reading, svgData, onShare }) {
  if (!open || !card) return null;
  return (
    <div className="fixed inset-0 z-50 hidden items-end justify-center bg-black/80 p-4 backdrop-blur-sm md:flex" role="dialog" aria-modal="true">
      <div className="tarot-fade-up relative max-h-[90vh] w-full max-w-5xl overflow-y-auto rounded-3xl border border-gold/20 bg-background p-6 shadow-2xl">
        <button
          type="button"
          onClick={onClose}
          className="absolute right-4 top-4 rounded-full border border-border bg-card p-2 text-muted-foreground transition-colors hover:text-foreground"
          aria-label="Close reading details"
        >
          <X className="h-4 w-4" />
        </button>
        <ReadingDetailsContent card={card} reading={reading} svgData={svgData} onShare={onShare} />
      </div>
    </div>
  );
}

function CardDrawer({ open, onOpenChange, card, reading, svgData, onShare }) {
  return (
    <Drawer.Root open={open} onOpenChange={onOpenChange}>
      <Drawer.Portal>
        <Drawer.Overlay className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm md:hidden" />
        <Drawer.Content className="fixed inset-x-0 bottom-0 z-50 max-h-[88vh] rounded-t-3xl border border-gold/20 bg-background p-4 shadow-2xl md:hidden">
          <div className="mx-auto mb-4 h-1.5 w-12 rounded-full bg-muted" />
          <div className="max-h-[78vh] overflow-y-auto pb-4">
            {card && <ReadingDetailsContent card={card} reading={reading} svgData={svgData} onShare={onShare} />}
          </div>
        </Drawer.Content>
      </Drawer.Portal>
    </Drawer.Root>
  );
}

function CelticCrossLayout({ cards, cardSVGs, onCardClick }) {
  if (!cards?.length) return null;
  const labels = [
    'The Heart', 'The Cross', 'Foundation', 'Recent Past', 'Crown', 'Near Future',
    'Self', 'Others', 'Hopes & Fears', 'Final Outcome',
  ];
  const positionClass = [
    'left-[38%] top-[34%] z-20 w-20',
    'left-[38%] top-[34%] z-30 w-20 rotate-90',
    'left-[38%] top-[62%] w-20',
    'left-[13%] top-[34%] w-20',
    'left-[38%] top-[6%] w-20',
    'left-[63%] top-[34%] w-20',
    'right-0 top-[68%] w-16',
    'right-0 top-[47%] w-16',
    'right-0 top-[26%] w-16',
    'right-0 top-[5%] w-16',
  ];
  return (
    <Card className="overflow-hidden border border-gold/20 bg-gold/[0.03] p-4">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Premium Celtic Cross</p>
          <p className="text-sm text-muted-foreground">Ten positions revealed as one complete oracle map.</p>
        </div>
        <span className="rounded-full border border-gold/30 bg-gold/10 px-2 py-1 text-xs font-semibold text-gold">Premium</span>
      </div>
      <div className="relative mx-auto h-[420px] max-w-md">
        {cards.slice(0, 10).map((card, index) => (
          <button
            key={`${card.card_id}-${card.position_code || index}`}
            type="button"
            onClick={() => onCardClick(card)}
            className={`tarot-fade-up group absolute ${positionClass[index] || 'w-20'}`}
            style={{ animationDelay: `${index * 90}ms` }}
          >
            <CardFace svgData={cardSVGs[card.card_id]} cardName={card.name} orientation={card.orientation} className="shadow-lg shadow-black/25" />
            <span className="mt-1 block rounded-full bg-background/90 px-1.5 py-0.5 text-[10px] text-gold opacity-90">
              {index + 1}
            </span>
          </button>
        ))}
      </div>
      <div className="grid gap-2 md:grid-cols-2">
        {cards.slice(0, 10).map((card, index) => (
          <div key={`${card.card_id}-label-${index}`} className="rounded-lg border border-border bg-card/70 p-2 text-xs">
            <span className="font-semibold text-gold">{index + 1}. {card.position_label || labels[index]}</span>
            <span className="ml-1 text-muted-foreground">{card.name}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}

function DefaultSpreadGrid({ cards, cardSVGs, onCardClick }) {
  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
      {cards.map(card => (
        <button
          key={card.card_id + card.position_code}
          type="button"
          onClick={() => onCardClick(card)}
          className="text-center transition-transform hover:scale-[1.02]"
        >
          <CardFace
            svgData={cardSVGs[card.card_id]}
            cardName={card.name}
            orientation={card.orientation}
            className="mb-2"
          />
          <p className="text-xs text-muted-foreground mb-0.5">{card.position_label}</p>
          <p className="text-xs font-semibold mb-1 leading-tight">{card.name}</p>
          <OrientationBadge orientation={card.orientation} />
          <p className="text-xs text-muted-foreground mt-1">{card.meaning_snippet}</p>
        </button>
      ))}
    </div>
  );
}

function HistoryTimeline({ history, cardSVGs, onBookmark, onCardClick }) {
  const groups = history.reduce((acc, item) => {
    const label = getMonthLabel(item);
    if (!acc[label]) acc[label] = [];
    acc[label].push(item);
    return acc;
  }, {});
  return (
    <div className="space-y-8">
      {Object.entries(groups).map(([month, items]) => (
        <section key={month}>
          <p className="mb-4 text-xs font-semibold uppercase tracking-widest text-gold/70">{month}</p>
          <div className="relative space-y-4 border-l-2 border-gold/20 pl-5">
            {items.map((item, index) => {
              const card = item.cards?.[0];
              return (
                <FadeInOnView key={item.id || item.report_id} delay={index * 80}>
                  <Card className="relative border border-border p-4 hover:border-gold/30">
                    <span className="absolute -left-[27px] top-5 h-3 w-3 rounded-full bg-gold/50 ring-4 ring-background" />
                    <div className="flex items-start gap-3">
                      <button type="button" onClick={() => card && onCardClick(card, item)} className="w-12 flex-shrink-0 transition-transform hover:scale-105">
                        {card && cardSVGs[card.card_id]
                          ? <CardFace svgData={cardSVGs[card.card_id]} cardName={card.name} orientation={card.orientation} />
                          : <CardBack />}
                      </button>
                      <div className="min-w-0 flex-1">
                        <div className="mb-1 flex flex-wrap items-center gap-2">
                          <span className="text-xs text-muted-foreground">{getCardDate(item)}</span>
                          {card && <OrientationBadge orientation={card.orientation} />}
                        </div>
                        <p className="font-semibold text-sm">{card?.name || item.spread_name || 'Tarot Reading'}</p>
                        {item.affirmation && (
                          <p className="mt-1 line-clamp-2 text-xs italic text-muted-foreground">"{item.affirmation}"</p>
                        )}
                      </div>
                      <button
                        type="button"
                        onClick={() => onBookmark(item.report_id, item.bookmarked)}
                        className="text-muted-foreground transition-colors hover:text-gold"
                        aria-label={item.bookmarked ? 'Remove bookmark' : 'Bookmark reading'}
                      >
                        {item.bookmarked ? <BookmarkCheck className="h-4 w-4 text-gold" /> : <Bookmark className="h-4 w-4" />}
                      </button>
                    </div>
                  </Card>
                </FadeInOnView>
              );
            })}
          </div>
        </section>
      ))}
    </div>
  );
}

// ── Main component ──────────────────────────────────────────────────────────

export const TarotPage = () => {
  const { user }   = useAuth();
  const navigate   = useNavigate();
  const sceneTimer = useRef(null);

  const [cardSVGs,       setCardSVGs]       = useState({});
  const [activeTab,      setActiveTab]      = useState('daily');
  const [focusArea,      setFocusArea]      = useState('guidance');
  const [question,       setQuestion]       = useState('');
  const [reading,        setReading]        = useState(null);
  const [spreads,        setSpreads]        = useState([]);
  const [history,        setHistory]        = useState([]);
  const [loading,        setLoading]        = useState(false);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [sceneIndex,     setSceneIndex]     = useState(0);
  const [playing,        setPlaying]        = useState(false);
  const [cardFlipped,    setCardFlipped]    = useState(false);
  const [spreadQuestion, setSpreadQuestion] = useState('');
  const [selectedSpreadId, setSelectedSpreadId] = useState(null);
  const [premiumState,    setPremiumState]    = useState({ checked: false, hasAccess: false, reason: '' });
  const [periods,         setPeriods]         = useState([]);
  const [offers,          setOffers]          = useState([]);
  const [gamification,    setGamification]    = useState(null);
  const [journalEntries,  setJournalEntries]  = useState([]);
  const [journalStats,    setJournalStats]    = useState(null);
  const [journalLoading,  setJournalLoading]  = useState(false);
  const [newIntention,    setNewIntention]    = useState('');
  const [savingIntention, setSavingIntention] = useState(false);
  const [detailCard,      setDetailCard]      = useState(null);
  const [detailReading,   setDetailReading]   = useState(null);
  const [detailOpen,      setDetailOpen]      = useState(false);

  // Load card SVG bundle from frontend/public/tarot_cards.json
  useEffect(() => {
    fetch('/tarot_cards.json').then(r => r.json()).then(setCardSVGs).catch(() => {});
  }, []);

  useEffect(() => {
    fetchSpreads();
    if (user) {
      checkTodayReading();
      fetchHistory({ silent: true });
    }
  }, [user]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (activeTab === 'history' && user) fetchHistory();
    if (activeTab === 'journal' && user) fetchJournal();
  }, [activeTab, user]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => () => clearTimeout(sceneTimer.current), []);

  // Flip card after scene sequence ends
  useEffect(() => {
    if (!playing && reading && !cardFlipped) {
      setTimeout(() => setCardFlipped(true), 400);
    }
  }, [playing, reading]); // eslint-disable-line react-hooks/exhaustive-deps

  // ── API helpers ───────────────────────────────────────────────────────────

  const fetchSpreads = async () => {
    try {
      const res = await axios.get(`${API}/tarot/spreads`);
      const nextSpreads = res.data.spreads || [];
      setSpreads(nextSpreads);
      if (nextSpreads.length && user) {
        try {
          const firstId = nextSpreads[0].spread_id;
          const accessRes = await axios.get(`${API}/tarot/spreads/${firstId}/access`, { withCredentials: true });
          const hasAccess = Boolean(accessRes.data?.has_access);
          setPremiumState({ checked: true, hasAccess, reason: accessRes.data?.reason || '' });
          if (hasAccess) {
            const [periodsRes, offersRes] = await Promise.all([
              axios.get(`${API}/tarot/favorable-periods`, { withCredentials: true }),
              axios.get(`${API}/tarot/offers`, { withCredentials: true }),
            ]);
            setPeriods(periodsRes.data?.periods || []);
            setOffers(offersRes.data?.offers || []);
          }
        } catch {
          setPremiumState({ checked: true, hasAccess: false, reason: '' });
        }
      } else {
        setPremiumState({ checked: true, hasAccess: false, reason: 'Sign in to access premium features.' });
      }
    } catch {}
  };

  const checkTodayReading = async () => {
    try {
      const res = await axios.get(`${API}/tarot/daily/today`, { withCredentials: true });
      if (res.data.already_drawn && res.data.reading) {
        setReading(res.data.reading);
        setSceneIndex((res.data.reading.scenes?.length || 1) - 1);
        setCardFlipped(true);
      }
    } catch {}
  };

  const fetchHistory = async (options = {}) => {
    setHistoryLoading(true);
    try {
      const res = await axios.get(`${API}/tarot/history`, { withCredentials: true });
      setHistory(res.data.items || []);
    } catch {
      if (!options.silent) toast.error('Could not load history');
    } finally {
      setHistoryLoading(false);
    }
  };

  const fetchJournal = async () => {
    setJournalLoading(true);
    try {
      const [journalRes, statsRes] = await Promise.all([
        axios.get(`${API}/tarot/manifestations`, { withCredentials: true }),
        axios.get(`${API}/tarot/manifestation/stats`, { withCredentials: true }),
      ]);
      setJournalEntries(journalRes.data?.items || []);
      setJournalStats(statsRes.data || null);
    } catch {
      toast.error('Could not load journal');
    } finally {
      setJournalLoading(false);
    }
  };

  const saveIntention = async () => {
    if (!newIntention.trim()) return;
    setSavingIntention(true);
    try {
      const today = new Date().toISOString().slice(0, 10);
      await axios.post(`${API}/tarot/manifestation`, {
        date: today,
        intention_text: newIntention.trim(),
        linked_reading_id: reading?.id || null,
        card_name: reading?.cards?.[0]?.name || null,
      }, { withCredentials: true });
      setNewIntention('');
      toast.success('Intention saved to your journal');
      fetchJournal();
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not save intention');
    } finally {
      setSavingIntention(false);
    }
  };

  const startSceneSequence = (scenes) => {
    setSceneIndex(0);
    setPlaying(true);
    setCardFlipped(false);
    let idx = 0;
    const advance = () => {
      idx++;
      if (idx < scenes.length) {
        setSceneIndex(idx);
        sceneTimer.current = setTimeout(advance, scenes[idx]?.duration_ms || 2500);
      } else {
        setPlaying(false);
      }
    };
    sceneTimer.current = setTimeout(advance, scenes[0]?.duration_ms || 2500);
  };

  const handleDraw = async () => {
    if (!user) { navigate('/login'); return; }
    setLoading(true);
    setReading(null);
    setCardFlipped(false);
    try {
      const res = await axios.post(`${API}/tarot/daily/draw`, {
        focus_area: focusArea,
        question: question || null,
        depth_level: 'simple',
      }, { withCredentials: true });
      const r = res.data.reading;
      setReading(r);
      if (res.data.gamification) setGamification(res.data.gamification);
      safeClaimPunyaAction('tarot_daily_draw', { referenceId: r.report_id });
      if (res.data.message === 'Already drawn today.') {
        toast.info("Today's card already drawn -- showing your reading.");
        setSceneIndex((r.scenes?.length || 1) - 1);
        setCardFlipped(true);
      } else {
        const xp = res.data.gamification?.xp_awarded || res.data.xp_earned || 0;
        if (xp) toast.success(`+${xp} XP earned!`);
        startSceneSequence(r.scenes || []);
      }
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not draw card');
    } finally {
      setLoading(false);
    }
  };

  const handleSpreadGenerate = async (spread) => {
    if (!user) { navigate('/login'); return; }
    setSelectedSpreadId(spread.spread_id);
    setLoading(true);
    setReading(null);
    setCardFlipped(false);
    try {
      const res = await axios.post(`${API}/tarot/spread/generate`, {
        spread_id: spread.spread_id,
        focus_area: focusArea,
        question: spreadQuestion || null,
      }, { withCredentials: true });
      setReading(res.data.reading);
      setActiveTab('daily');
      safeClaimPunyaAction('tarot_spread_complete', { referenceId: res.data.reading.report_id });
      toast.success(`+${res.data.xp_earned} XP earned!`);
      startSceneSequence(res.data.reading.scenes || []);
    } catch (e) {
      toast.error(e.response?.data?.detail || 'Could not generate spread');
    } finally {
      setLoading(false);
      setSelectedSpreadId(null);
    }
  };

  const toggleBookmark = async (reportId, current) => {
    try {
      await axios.post(`${API}/tarot/bookmark`,
        { report_id: reportId, bookmarked: !current },
        { withCredentials: true },
      );
      if (reading?.report_id === reportId) setReading(r => ({ ...r, bookmarked: !current }));
      setHistory(h => h.map(i => i.report_id === reportId ? { ...i, bookmarked: !current } : i));
      if (!current) safeClaimPunyaAction('tarot_bookmark', { referenceId: reportId });
      toast.success(!current ? 'Bookmarked' : 'Removed bookmark');
    } catch {
      toast.error('Could not update bookmark');
    }
  };

  const resetDraw = () => {
    clearTimeout(sceneTimer.current);
    setReading(null);
    setCardFlipped(false);
    setPlaying(false);
  };

  const openCardDetails = (card, sourceReading = reading) => {
    if (!card) return;
    setDetailCard(card);
    setDetailReading(sourceReading || reading);
    setDetailOpen(true);
  };

  const shareReading = async () => {
    const shareText = detailCard
      ? `${detailCard.name} ${detailCard.orientation ? `(${detailCard.orientation})` : ''} - ${getCardMeaning(detailCard, detailReading)}`
      : 'My Tarot reading from EverydayHoroscope';
    try {
      if (navigator.share) {
        await navigator.share({ title: 'My Tarot Reading', text: shareText, url: `${SITE}/tarot` });
      } else {
        await navigator.clipboard.writeText(`${shareText}\n${SITE}/tarot`);
        toast.success('Reading copied to clipboard');
      }
    } catch {}
  };

  // ── Derived ───────────────────────────────────────────────────────────────

  const currentScene = reading?.scenes?.[sceneIndex];
  const primaryCard  = reading?.cards?.[0];
  const primarySVG   = primaryCard ? cardSVGs[primaryCard.card_id] : null;
  const isCelticCross = reading?.cards?.length === 10 || reading?.layout === 'celtic_cross' || reading?.meta?.layout === 'celtic_cross';
  const detailSVG = detailCard ? cardSVGs[detailCard.card_id] : null;

  // ── Premium gate -- logged-in non-premium users ────────────────────────────
  if (user && !user.is_premium) return (
    <PremiumGateCard
      feature="Tarot Reading"
      description="Daily tarot draws, card spreads, and reading history are exclusive to Premium subscribers. Upgrade to unlock full tarot guidance."
    />
  );

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <TarotV4Styles />
      <SEO
        title="Free Tarot Reading -- Daily Draw & Spreads | EverydayHoroscope"
        description="Get your free daily tarot card draw and multi-card spreads. Cosmic guidance powered by the 78-card Rider-Waite deck. EverydayHoroscope."
        url={`${SITE}/tarot`}
        schema={schema}
      />

      <TarotHero
        onDrawClick={() => {
          setActiveTab('daily');
          setTimeout(() => document.getElementById('tarot-draw-panel')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50);
        }}
      />

      <StreakWidget history={history} gamification={gamification} />

      {/* Gamification bar -- shown after a draw */}
      {gamification && (
        <div className="flex flex-wrap items-center gap-3 rounded-xl border border-gold/20 bg-gold/[0.04] px-4 py-2 text-xs mb-2">
          <span className="flex items-center gap-1 font-semibold text-gold">
            <Zap className="h-3.5 w-3.5" /> {gamification.xp_awarded > 0 ? `+${gamification.xp_awarded} XP` : `Lv ${gamification.level}`}
          </span>
          {gamification.daily_streak > 0 && (
            <span className="flex items-center gap-1 text-orange-500 font-semibold">
              <Flame className="h-3.5 w-3.5" /> {gamification.daily_streak}-day streak
            </span>
          )}
          {gamification.new_badges?.map(b => (
            <span key={b} className="rounded-full border border-gold/30 bg-gold/10 px-2 py-0.5 text-gold">{b}</span>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-1 border-b border-border mb-8 overflow-x-auto">
        {[
          { key: 'daily',   label: 'Daily Draw' },
          { key: 'spreads', label: 'Spreads' },
          { key: 'timing',  label: 'Favorable Periods', disabled: !user },
          { key: 'journal', label: 'Journal', disabled: !user },
          { key: 'history', label: 'History', disabled: !user },
        ].map(t => (
          <button key={t.key} onClick={() => !t.disabled && setActiveTab(t.key)} disabled={t.disabled}
            className={`px-4 py-2.5 text-sm font-medium whitespace-nowrap transition-colors ${
              activeTab === t.key ? 'border-b-2 border-gold text-gold' :
              t.disabled ? 'text-muted-foreground/40 cursor-not-allowed' : 'text-muted-foreground hover:text-foreground'
            }`}>{t.label}
          </button>
        ))}
      </div>

      {/* ── DAILY DRAW TAB ── */}
      {activeTab === 'daily' && (
        <div id="tarot-draw-panel" className="space-y-5 scroll-mt-6">

          {/* Scene player (shown while playing) */}
          {reading && currentScene && playing && (
            <Card className="p-6 border border-gold/30 bg-gold/5 text-center">
              <p className="text-xs text-gold uppercase tracking-widest mb-3">
                {currentScene.scene_type.replace('_', ' ')}
              </p>
              {currentScene.title && (
                <p className="font-playfair text-xl font-semibold mb-3">{currentScene.title}</p>
              )}
              <p className="text-sm text-foreground leading-relaxed">{currentScene.text}</p>
              <div className="flex justify-center gap-1.5 mt-4">
                {reading.scenes.map((_, i) => (
                  <div key={i} className={`rounded-full transition-all ${
                    i === sceneIndex ? 'bg-gold w-4 h-1.5' : 'bg-muted-foreground/30 w-1.5 h-1.5'
                  }`} />
                ))}
              </div>
            </Card>
          )}

          {/* Card reveal (shown after scene sequence) */}
          {reading && !playing && primaryCard && (
            <>
              <FlippingCard
                cardId={primaryCard.card_id}
                cardName={primaryCard.name}
                orientation={primaryCard.orientation}
                svgData={primarySVG}
                flipped={cardFlipped}
                onClick={cardFlipped ? () => openCardDetails(primaryCard) : undefined}
              />

              <Card className="p-5 border border-border">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2 flex-wrap">
                      <Star className="h-4 w-4 text-gold flex-shrink-0" />
                      <p className="font-semibold">{primaryCard.name}</p>
                      <OrientationBadge orientation={primaryCard.orientation} />
                      {reading.moon_phase && (
                        <span className="rounded-full border border-border bg-muted/40 px-2 py-0.5 text-[11px] text-muted-foreground">
                          {reading.moon_phase}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground mb-1">{primaryCard.position_label}</p>
                    <p className="text-sm">{primaryCard.meaning_snippet}</p>
                  </div>
                  <button onClick={() => toggleBookmark(reading.report_id, reading.bookmarked)}
                    className="text-muted-foreground hover:text-gold transition-colors flex-shrink-0">
                    {reading.bookmarked
                      ? <BookmarkCheck className="h-4 w-4 text-gold" />
                      : <Bookmark className="h-4 w-4" />}
                  </button>
                </div>
                {reading.affirmation && (
                  <div className="mt-4 pt-4 border-t border-border">
                    <p className="text-xs text-gold uppercase tracking-widest mb-1">Affirmation</p>
                    <p className="text-sm italic">"{reading.affirmation}"</p>
                  </div>
                )}
              </Card>

              {/* Multi-card spread grid */}
              {reading.cards?.length > 1 && (
                <Card className="p-5 border border-border">
                  <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mb-4">The Spread</p>
                  {isCelticCross ? (
                    <CelticCrossLayout cards={reading.cards} cardSVGs={cardSVGs} onCardClick={openCardDetails} />
                  ) : (
                    <DefaultSpreadGrid cards={reading.cards} cardSVGs={cardSVGs} onCardClick={openCardDetails} />
                  )}
                </Card>
              )}
            </>
          )}

          {/* Draw controls (no reading yet) */}
          {!reading && !loading && (
            <>
              <Card className="p-5 border border-border">
                <p className="text-sm font-medium mb-3">Focus Area</p>
                <div className="mb-4">
                  <FocusAreaCards value={focusArea} onChange={setFocusArea} />
                </div>
                <input
                  type="text"
                  value={question}
                  onChange={e => setQuestion(e.target.value)}
                  placeholder="Optional: ask the cards a specific question..."
                  className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
                />
              </Card>

              {/* Face-down card grid */}
              <div className="grid grid-cols-3 gap-3">
                {[0, 1, 2, 3, 4, 5].map(i => <CardBack key={i} />)}
              </div>
            </>
          )}

          {loading && (
            <div className="text-center py-12">
              <Loader2 className="h-8 w-8 animate-spin text-gold mx-auto mb-3" />
              <p className="text-sm text-muted-foreground">The cards are being drawn...</p>
            </div>
          )}

          {/* CTA button */}
          {!loading && (
            <div className="space-y-3">
              {!reading ? (
                <Button onClick={handleDraw}
                  className="w-full bg-gold hover:bg-gold/90 text-primary-foreground font-semibold gap-2">
                  <Sparkles className="h-4 w-4" />
                  {user ? "Draw Today's Card" : 'Sign In to Draw'}
                </Button>
              ) : (
                <Button onClick={resetDraw} variant="outline" className="w-full border-border gap-2">
                  <RotateCcw className="h-4 w-4" />
                  Draw Again Tomorrow
                </Button>
              )}
              {!user && (
                <p className="text-center text-xs text-muted-foreground">
                  Free account required to save your readings
                </p>
              )}
            </div>
          )}
        </div>
      )}

      {/* ── SPREADS TAB ── */}
      {activeTab === 'spreads' && (
        <div className="space-y-4">
          <p className="text-sm text-muted-foreground">
            Premium 3-card spreads -- deeper readings for specific areas of life.
          </p>

          {/* Premium access gate */}
          {!premiumState.checked && user && (
            <div className="text-center py-3">
              <Loader2 className="h-5 w-5 animate-spin text-gold mx-auto" />
            </div>
          )}
          {premiumState.checked && premiumState.hasAccess && (
            <div className="flex items-center gap-2 pb-1">
              <Crown className="h-4 w-4 text-gold" />
              <p className="text-sm font-semibold">Begin Premium Reading</p>
            </div>
          )}
          {premiumState.checked && !premiumState.hasAccess && user && (
            <Card className="p-4 border border-gold/30 bg-gold/5">
              <div className="flex items-center gap-3">
                <Crown className="h-5 w-5 text-gold flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm font-semibold">Premium spreads are waiting</p>
                  <p className="text-xs text-muted-foreground">
                    {premiumState.reason || 'Unlock multi-card spreads and timing guidance.'}
                  </p>
                </div>
                <Button onClick={() => navigate('/pricing?source=tarot-spreads')} size="sm"
                  className="bg-gold hover:bg-gold/90 text-primary-foreground flex-shrink-0">
                  Unlock
                </Button>
              </div>
            </Card>
          )}

          <input
            type="text"
            value={spreadQuestion}
            onChange={e => setSpreadQuestion(e.target.value)}
            placeholder="Your question for the spread..."
            className="w-full px-3 py-2.5 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-gold/40"
          />

          <div>
            <p className="text-xs text-muted-foreground mb-2">Focus Area</p>
            <FocusAreaCards value={focusArea} onChange={setFocusArea} />
          </div>

          {spreads.map(spread => (
            <Card key={spread.spread_id} className="p-5 border border-border hover:border-gold/30 transition-all">
              <div className="flex items-start gap-3">
                <div className="w-9 h-9 rounded-lg bg-gold/10 flex items-center justify-center flex-shrink-0">
                  <Crown className="h-4 w-4 text-gold" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <p className="font-semibold text-sm">{spread.name}</p>
                    <span className="text-xs border border-gold/30 text-gold px-2 py-0.5 rounded-full">
                      {spread.card_count} cards
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mb-1">{spread.description}</p>
                  <p className="text-xs text-muted-foreground mb-3">
                    {spread.positions.join(' · ')}
                  </p>
                  {spread.ritual_note && (
                    <p className="text-xs text-muted-foreground/70 italic mb-3 leading-5">
                      ✦ {spread.ritual_note}
                    </p>
                  )}
                  <Button
                    onClick={() => handleSpreadGenerate(spread)}
                    disabled={loading}
                    size="sm"
                    className="bg-gold hover:bg-gold/90 text-primary-foreground gap-1.5"
                  >
                    {loading && selectedSpreadId === spread.spread_id
                      ? <><Loader2 className="h-3 w-3 animate-spin" /> Drawing...</>
                      : <><Zap className="h-3 w-3" /> Draw Spread</>}
                  </Button>
                </div>
              </div>
            </Card>
          ))}

          {!user && (
            <div className="text-center py-6">
              <p className="text-sm text-muted-foreground mb-3">Sign in to draw a spread</p>
              <Button onClick={() => navigate('/login')} variant="outline" size="sm">Sign In</Button>
            </div>
          )}
        </div>
      )}

      {/* ── TIMING TAB ── */}
      {activeTab === 'timing' && user && (
        <div className="space-y-4">
          {!premiumState.hasAccess ? (
            <Card className="p-6 border border-gold/30 text-center">
              <Crown className="h-8 w-8 text-gold/40 mx-auto mb-3" />
              <p className="font-semibold mb-2">Timing guidance is a premium layer</p>
              <p className="text-sm text-muted-foreground mb-4">
                {premiumState.reason || 'Unlock favorable periods, personalized next steps, and deeper timing-based Tarot guidance.'}
              </p>
              <Button onClick={() => navigate('/pricing?source=tarot-timing')} size="sm"
                className="bg-gold hover:bg-gold/90 text-primary-foreground">
                Unlock Premium
              </Button>
            </Card>
          ) : (
            <>
              <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground">Favorable Periods</p>
              {periods.length ? periods.map(period => (
                <Card key={period.id} className="p-4 border border-border">
                  <div className="flex items-center gap-2 mb-2 flex-wrap">
                    <span className="text-xs px-2 py-0.5 rounded-full border border-gold/30 text-gold capitalize">{period.type}</span>
                    <span className="text-xs text-muted-foreground">{period.window_label}</span>
                    <span className="text-xs text-muted-foreground">{Math.round(Number(period.confidence || 0) * 100)}% confidence</span>
                  </div>
                  <p className="text-sm mb-1">{period.summary}</p>
                  {period.recommendation && (
                    <p className="text-xs text-gold italic">{period.recommendation}</p>
                  )}
                </Card>
              )) : (
                <p className="text-sm text-muted-foreground">Your next favorable windows will appear here once available.</p>
              )}
              {offers.length > 0 && (
                <>
                  <p className="text-xs font-semibold uppercase tracking-widest text-muted-foreground mt-2">Recommended Next Steps</p>
                  {offers.map(offer => (
                    <Card key={offer.id} className="p-4 border border-border">
                      <p className="font-semibold text-sm mb-1">{offer.title}</p>
                      <p className="text-xs text-muted-foreground mb-3">{offer.description}</p>
                      <Button onClick={() => navigate(offer.destination || '/pricing')} size="sm"
                        variant="outline" className="border-gold/30 text-gold hover:bg-gold/10">
                        {offer.cta_label}
                      </Button>
                    </Card>
                  ))}
                </>
              )}
            </>
          )}
        </div>
      )}

      {/* ── JOURNAL TAB ── */}
      {activeTab === 'journal' && (
        <div className="space-y-5">

          {/* Stats bar */}
          {journalStats && (
            <div className="flex flex-wrap gap-4 rounded-xl border border-gold/20 bg-gold/[0.04] px-5 py-3">
              <div className="flex items-center gap-2">
                <Flame className="h-4 w-4 text-orange-500" />
                <span className="text-sm font-semibold">{journalStats.streak_days}-day streak</span>
              </div>
              <div className="flex items-center gap-2">
                <NotebookPen className="h-4 w-4 text-gold" />
                <span className="text-sm font-semibold">{journalStats.total_intentions} intentions set</span>
              </div>
              {journalStats.most_drawn_card && (
                <div className="flex items-center gap-2">
                  <Star className="h-4 w-4 text-gold" />
                  <span className="text-sm text-muted-foreground">Most drawn: <strong>{journalStats.most_drawn_card}</strong></span>
                </div>
              )}
            </div>
          )}

          {/* New intention form */}
          <Card className="p-5 border border-gold/20">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-gold">Set Today's Intention</p>
            {reading && (
              <p className="mb-2 text-xs text-muted-foreground">
                Linked to today's draw: <strong>{reading.cards?.[0]?.name}</strong>
              </p>
            )}
            <textarea
              value={newIntention}
              onChange={e => setNewIntention(e.target.value)}
              rows={3}
              placeholder="What do you intend to manifest or release today?"
              className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/60 outline-none focus:ring-1 focus:ring-gold/40 resize-none"
            />
            <Button
              onClick={saveIntention}
              disabled={savingIntention || !newIntention.trim()}
              className="mt-3 bg-gold hover:bg-gold/90 text-primary-foreground"
              size="sm"
            >
              {savingIntention ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" /> : <NotebookPen className="h-3.5 w-3.5 mr-1.5" />}
              Save Intention
            </Button>
          </Card>

          {/* Journal entries */}
          {journalLoading && (
            <div className="py-8 text-center">
              <Loader2 className="h-6 w-6 animate-spin text-gold mx-auto" />
            </div>
          )}
          {!journalLoading && journalEntries.length === 0 && (
            <div className="py-10 text-center">
              <NotebookPen className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
              <p className="text-muted-foreground text-sm">No journal entries yet. Set your first intention above.</p>
            </div>
          )}
          {journalEntries.map(entry => (
            <Card key={entry.id} className="p-4 border border-border hover:border-gold/30 transition-colors">
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <span className="text-xs text-muted-foreground">{entry.date}</span>
                    {entry.moon_phase && (
                      <span className="text-xs rounded-full border border-border px-2 py-0.5 text-muted-foreground">{entry.moon_phase}</span>
                    )}
                    {entry.card_name && (
                      <span className="text-xs text-gold">{entry.card_name}</span>
                    )}
                  </div>
                  <p className="text-sm leading-6 text-foreground">{entry.intention_text}</p>
                  {(entry.tasks_total > 0 || entry.reminders_count > 0) && (
                    <p className="mt-1 text-xs text-muted-foreground">
                      {entry.tasks_done}/{entry.tasks_total} tasks · {entry.reminders_count} reminders
                    </p>
                  )}
                </div>
                <button
                  className="text-muted-foreground hover:text-gold transition-colors flex-shrink-0"
                  aria-label={entry.bookmarked ? "Bookmarked" : "Bookmark"}
                >
                  {entry.bookmarked
                    ? <BookmarkCheck className="h-4 w-4 text-gold" />
                    : <Bookmark className="h-4 w-4" />}
                </button>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* ── HISTORY TAB ── */}
      {activeTab === 'history' && (
        <div className="space-y-3">
          {historyLoading && (
            <div className="text-center py-12">
              <Loader2 className="h-6 w-6 animate-spin text-gold mx-auto" />
            </div>
          )}
          {!historyLoading && history.length === 0 && (
            <div className="text-center py-12">
              <BookOpen className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
              <p className="text-muted-foreground">No readings yet. Draw your first card.</p>
              <Button onClick={() => setActiveTab('daily')}
                className="mt-4 bg-gold hover:bg-gold/90 text-primary-foreground" size="sm">
                Draw Now
              </Button>
            </div>
          )}
          {history.length > 0 && (
            <HistoryTimeline
              history={history}
              cardSVGs={cardSVGs}
              onBookmark={toggleBookmark}
              onCardClick={openCardDetails}
            />
          )}
        </div>
      )}

      {/* ── On-page SEO content ──────────────────────────────────────────── */}
      <div className="mt-12 space-y-8 border-t border-border pt-10 text-sm text-muted-foreground">
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">What is Tarot?</h2>
          <p className="leading-7">Tarot is a system of 78 illustrated cards used for reflective guidance, spiritual insight, and decision-making. Dating back to 15th-century Europe and deeply enriched by Hermetic, Kabbalistic, and astrological traditions, Tarot is not fortune-telling -- it is a mirror for the subconscious. Each card carries archetypal energy that, when drawn at a sincere moment, surfaces what the intuitive mind already knows.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">The 78-Card Rider-Waite Deck</h2>
          <p className="leading-7">The Rider-Waite deck -- illustrated by Pamela Colman Smith in 1909 -- is the most widely used Tarot system. It divides into 22 Major Arcana cards (the Fool through the World -- representing life's universal themes) and 56 Minor Arcana across four suits: Wands (fire, ambition), Cups (water, emotion), Swords (air, intellect), and Pentacles (earth, material). Every card carries distinct symbolism, numerological significance, and planetary correspondence.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">How a Daily Draw Works</h2>
          <p className="leading-7">A daily draw selects one card from the full 78-card deck to represent the energy, theme, or lesson most relevant to your current moment. EverydayHoroscope contextualises your draw within your Vedic birth chart -- your Lagna, Moon sign, and Mahadasha cycle inform the interpretation, giving the pull personal resonance rather than a generic reading.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Upright vs Reversed Cards</h2>
          <p className="leading-7">When a Tarot card is drawn in reverse (inverted orientation), its energy is considered internalised, blocked, or in shadow form. A reversed card does not mean a negative outcome -- it signals that the card's theme needs inward attention rather than outward action. For example, reversed Strength suggests self-doubt to be overcome, not weakness itself. EverydayHoroscope reads both orientations with full nuance.</p>
        </div>
        <div>
          <h2 className="mb-2 text-base font-semibold text-foreground">Tarot Spreads & Multi-Card Readings</h2>
          <p className="leading-7">Beyond single-card draws, structured spreads place multiple cards in positional relationships -- Past / Present / Future, Situation / Action / Outcome, or the classic Celtic Cross. Each position in the spread has a defined meaning, and the cards interact to form a narrative. EverydayHoroscope supports multiple spread types so you can explore both quick daily guidance and in-depth situational readings.</p>
        </div>
      </div>

      <ReadingModal
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
        card={detailCard}
        reading={detailReading}
        svgData={detailSVG}
        onShare={shareReading}
      />
      <CardDrawer
        open={detailOpen}
        onOpenChange={setDetailOpen}
        card={detailCard}
        reading={detailReading}
        svgData={detailSVG}
        onShare={shareReading}
      />

    </div>
  );
};
