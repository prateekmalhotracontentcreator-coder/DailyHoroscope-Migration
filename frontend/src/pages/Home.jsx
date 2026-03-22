import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/card';
import { DOBModal } from '../components/DOBPrompt';
import { Sparkles, Sun, Calendar, TrendingUp, Star, Heart, Crown, BookOpen, ChevronRight } from 'lucide-react';
import { Footer } from '../components/Footer';
import { useHoroscope, ZODIAC_MAP } from '../hooks/useHoroscope';

export const Home = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { primarySign, primarySignMeta, favouritesMeta, dobDone, saveDOB, dismissDOBPrompt } = useHoroscope();
  const [showDOBModal, setShowDOBModal] = useState(false);

  // Show DOB modal on Home if not yet done and user is logged in
  useEffect(() => {
    if (!dobDone && user) {
      const t = setTimeout(() => setShowDOBModal(true), 1000);
      return () => clearTimeout(t);
    }
  }, [dobDone, user]);

  const handleDOBSave = (dob, sign) => {
    saveDOB(dob);
    setShowDOBModal(false);
  };

  const features = [
    { id: 'daily',     title: 'Daily Horoscope',      description: 'Get your personalised daily cosmic guidance',      icon: Sun,      color: 'text-orange-500', bgColor: 'bg-orange-500/10', path: '/horoscope/daily' },
    { id: 'weekly',    title: 'Weekly Horoscope',     description: 'Plan your week with astrological insights',         icon: Calendar,  color: 'text-blue-500',   bgColor: 'bg-blue-500/10',   path: '/horoscope/weekly' },
    { id: 'monthly',   title: 'Monthly Horoscope',    description: 'Navigate the month ahead with confidence',         icon: TrendingUp,color: 'text-green-500',  bgColor: 'bg-green-500/10',  path: '/horoscope/monthly' },
    { id: 'birthchart',title: 'Birth Chart Analysis', description: 'Comprehensive Vedic astrology report',             icon: Star,      color: 'text-gold',       bgColor: 'bg-gold/10',       path: '/birth-chart',   premium: true },
    { id: 'kundali',   title: 'Kundali Milan',        description: 'Marriage compatibility analysis',                  icon: Heart,     color: 'text-pink-500',  bgColor: 'bg-pink-500/10',   path: '/kundali-milan', premium: true },
    { id: 'brihat',    title: 'Brihat Kundli Pro',    description: '40+ page comprehensive Vedic life report',         icon: Crown,     color: 'text-purple-500',bgColor: 'bg-purple-500/10', path: '/brihat-kundli', premium: true },
    { id: 'blog',      title: 'Cosmic Blog',          description: 'Astrology insights and zodiac guides',             icon: BookOpen,  color: 'text-purple-500',bgColor: 'bg-purple-500/10', path: '/blog' },
  ];

  const firstName = user?.name?.split(' ')[0] || 'there';

  return (
    <div className="min-h-screen">
      {/* DOB modal — shown once on Home for logged-in users */}
      {showDOBModal && (
        <DOBModal
          onSave={handleDOBSave}
          onDismiss={() => { dismissDOBPrompt(); setShowDOBModal(false); }}
        />
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">

        {/* ── Personalised banner ── */}
        {primarySignMeta ? (
          <div className="mb-10">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-xl border border-gold/30 bg-gradient-to-r from-gold/5 via-card to-gold/5">
              <div className="flex items-center gap-4">
                <div className="text-5xl leading-none">{primarySignMeta.symbol}</div>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-1">Welcome back, {firstName}</p>
                  <h2 className="text-2xl font-playfair font-semibold">Your sign: {primarySignMeta.name}</h2>
                  <p className="text-sm text-muted-foreground">{primarySignMeta.element} sign · Your cosmic guidance awaits</p>
                </div>
              </div>
              <div className="flex flex-col sm:items-end gap-2">
                <button
                  onClick={() => navigate('/horoscope/daily')}
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gold text-primary-foreground text-sm font-semibold hover:bg-gold/90 transition-colors"
                >
                  <Sun className="h-4 w-4" /> Today's Horoscope
                </button>
                <button
                  onClick={() => navigate('/horoscope/daily')}
                  className="inline-flex items-center gap-1.5 text-xs text-muted-foreground hover:text-gold transition-colors"
                >
                  Change sign <ChevronRight className="h-3 w-3" />
                </button>
              </div>
            </div>

            {/* Favourites quick-access */}
            {favouritesMeta.length > 1 && (
              <div className="mt-4">
                <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3 flex items-center gap-1.5">
                  <Star className="h-3.5 w-3.5 fill-gold" /> Favourite Signs
                </p>
                <div className="flex flex-wrap gap-2">
                  {favouritesMeta.map(sign => (
                    <button
                      key={sign.id}
                      onClick={() => navigate('/horoscope/daily')}
                      className={`flex items-center gap-2 px-3 py-2 rounded-full border text-sm font-medium transition-colors ${
                        sign.id === primarySign
                          ? 'border-gold bg-gold/10 text-gold'
                          : 'border-border hover:border-gold/40 hover:bg-gold/5'
                      }`}
                    >
                      <span>{sign.symbol}</span>
                      <span>{sign.name}</span>
                      {sign.id === primarySign && <span className="text-xs opacity-60">(yours)</span>}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        ) : (
          /* No sign saved — generic welcome + CTA */
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-playfair font-semibold mb-4">Your Daily Dose of Cosmic Guidance</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Discover what the stars have aligned for you. Get free daily horoscope predictions and explore premium astrology services.
            </p>
            <button
              onClick={() => setShowDOBModal(true)}
              className="mt-6 inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gold text-primary-foreground text-sm font-semibold hover:bg-gold/90 transition-colors"
            >
              <Sparkles className="h-4 w-4" /> Personalise my horoscope
            </button>
          </div>
        )}

        {/* ── Feature cards ── */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Card
                key={feature.id}
                data-testid={`feature-card-${feature.id}`}
                className="group relative p-8 border-2 border-border hover:border-gold transition-all duration-300 cursor-pointer hover:scale-105 hover:shadow-[0_8px_30px_-5px_rgba(197,160,89,0.3)]"
                onClick={() => navigate(feature.path)}
              >
                {feature.premium && (
                  <div className="absolute top-4 right-4">
                    <span className="inline-flex items-center space-x-1 bg-gold text-primary-foreground px-2 py-1 rounded-full text-xs font-semibold">
                      <Crown className="h-3 w-3" /><span>PREMIUM</span>
                    </span>
                  </div>
                )}
                <div className={`${feature.bgColor} rounded-sm p-4 w-fit mb-4`}>
                  <Icon className={`h-8 w-8 ${feature.color}`} />
                </div>
                <h3 className="text-2xl font-playfair font-semibold mb-2 group-hover:text-gold transition-colors">{feature.title}</h3>
                <p className="text-muted-foreground mb-4">{feature.description}</p>
                <div className="flex items-center text-gold text-sm font-semibold group-hover:translate-x-2 transition-transform">
                  Explore
                  <svg className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="mt-16 text-center">
          <Card className="p-8 bg-gradient-to-br from-card to-muted border-gold/30">
            <Sparkles className="h-12 w-12 text-gold mx-auto mb-4" />
            <h3 className="text-2xl font-playfair font-semibold mb-2">Your Astrological Journey Awaits</h3>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Whether you're seeking daily guidance or deep insights into your life path,
              our AI-powered astrology platform provides authentic, personalised readings
              based on Vedic astrological principles.
            </p>
          </Card>
        </div>
      </div>
      <Footer />
    </div>
  );
};
