import React from 'react';
import { SEO } from '../components/SEO';
import { Sparkles, Calendar, Sun, Moon, Star, Shield, Zap } from 'lucide-react';
import { Card } from '../components/ui/card';

const TYPE_CONFIG = {
  today:      { title: "Today's Panchang",    icon: Sun,      desc: "Complete Vedic almanac for today — Tithi, Nakshatra, Yoga, Karana, Sunrise & Sunset" },
  tomorrow:   { title: "Tomorrow's Panchang", icon: Sun,      desc: "Plan ahead with tomorrow's complete Vedic almanac" },
  tithi:      { title: "Tithi",               icon: Moon,     desc: "Today's lunar day — the foundation of all Vedic timing" },
  muhurat:    { title: "Shubh Muhurat",       icon: Star,     desc: "Auspicious times for important activities today" },
  nakshatra:  { title: "Nakshatra",           icon: Sparkles, desc: "Today's birth star and its cosmic influence" },
  choghadiya: { title: "Choghadiya",          icon: Zap,      desc: "Vedic time periods — auspicious and inauspicious windows" },
  rahukaal:   { title: "Rahu Kaal",           icon: Shield,   desc: "Today's Rahu Kaal — the inauspicious period to avoid for new beginnings" },
};

const PANCHANG_ITEMS = [
  { label: 'Tithi',      value: 'Navami (9th lunar day)',     sub: 'Shukla Paksha (Waxing Moon)' },
  { label: 'Nakshatra',  value: 'Hasta',                      sub: 'Moon in Virgo — Lord: Moon' },
  { label: 'Yoga',       value: 'Siddha',                     sub: 'Auspicious for new beginnings' },
  { label: 'Karana',     value: 'Bava',                       sub: 'First half of the day' },
  { label: 'Vara',       value: 'Guruvaar (Thursday)',        sub: 'Lord: Jupiter (Brihaspati)' },
  { label: 'Sunrise',    value: '06:24 AM IST',               sub: 'New Delhi' },
  { label: 'Sunset',     value: '06:47 PM IST',               sub: 'New Delhi' },
  { label: 'Rahu Kaal',  value: '01:30 PM – 03:00 PM',       sub: 'Avoid important activities' },
  { label: 'Shubh Muhurat', value: '10:15 AM – 11:45 AM',   sub: 'Abhijit Muhurat — most auspicious' },
];

export const PanchangPage = ({ type = 'today' }) => {
  const config = TYPE_CONFIG[type] || TYPE_CONFIG.today;
  const Icon = config.icon;
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <SEO title={`${config.title} — Everyday Horoscope`} description={config.desc} />
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Calendar className="h-3 w-3" /> Vedic Panchang
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
        <p className="text-muted-foreground">{config.desc}</p>
      </div>
      <Card className="border border-gold/20 overflow-hidden">
        <div className="bg-gold/5 border-b border-gold/20 px-6 py-4 flex items-center gap-3">
          <Icon className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold">Thursday, 19 March 2026</span>
          <span className="ml-auto text-xs text-muted-foreground">New Delhi, India</span>
        </div>
        <div className="divide-y divide-border">
          {PANCHANG_ITEMS.map((item) => (
            <div key={item.label} className="flex items-center justify-between px-6 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              <p className="text-xs text-muted-foreground text-right max-w-[140px]">{item.sub}</p>
            </div>
          ))}
        </div>
      </Card>
      <p className="text-center text-xs text-muted-foreground mt-6">
        Full dynamic Panchang powered by flatlib coming soon. Data shown is illustrative.
      </p>
    </div>
  );
};
