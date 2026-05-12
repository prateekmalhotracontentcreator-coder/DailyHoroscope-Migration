import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { HoroscopeCard } from '../components/HoroscopeCard';
import { HoroscopeShareCard, ShareButtons } from '../components/ShareCard';
import { Card } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { ArrowLeft, ArrowRight, Star } from 'lucide-react';
import { ZODIAC_SIGNS_FULL, ZODIAC_MAP } from '../hooks/useHoroscope';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Vedic ruling planet + sign description for SEO-rich metadata
const SIGN_META = {
  aries:       { ruler: 'Mars',    quality: 'Cardinal', desc: 'Aries, the first sign of the Vedic zodiac, is ruled by Mars. Bold, pioneering, and energetic, Aries natives are natural leaders driven by courage and ambition.' },
  taurus:      { ruler: 'Venus',   quality: 'Fixed',    desc: 'Taurus is ruled by Venus, the planet of beauty and wealth. Grounded, patient, and sensual, Taurus natives seek stability, comfort, and lasting security.' },
  gemini:      { ruler: 'Mercury', quality: 'Mutable',  desc: 'Gemini is ruled by Mercury, the planet of intellect. Quick-witted, curious, and communicative, Gemini natives thrive on ideas, conversation, and versatility.' },
  cancer:      { ruler: 'Moon',    quality: 'Cardinal', desc: 'Cancer is ruled by the Moon, governing emotion and intuition. Nurturing, empathetic, and deeply connected to home and family, Cancer natives are guided by feeling.' },
  leo:         { ruler: 'Sun',     quality: 'Fixed',    desc: 'Leo is ruled by the Sun, the centre of our solar system. Confident, creative, and magnetic, Leo natives are natural performers who radiate warmth and authority.' },
  virgo:       { ruler: 'Mercury', quality: 'Mutable',  desc: 'Virgo is ruled by Mercury, the planet of analysis. Practical, discerning, and detail-oriented, Virgo natives excel at service, health, and methodical problem-solving.' },
  libra:       { ruler: 'Venus',   quality: 'Cardinal', desc: 'Libra is ruled by Venus, the planet of harmony. Diplomatic, gracious, and justice-seeking, Libra natives strive for balance in all relationships and decisions.' },
  scorpio:     { ruler: 'Mars',    quality: 'Fixed',    desc: 'Scorpio is governed by Mars and Ketu in Vedic astrology. Intense, transformative, and deeply perceptive, Scorpio natives pursue truth beneath the surface.' },
  sagittarius: { ruler: 'Jupiter', quality: 'Mutable',  desc: 'Sagittarius is ruled by Jupiter, the planet of wisdom and expansion. Philosophical, adventurous, and optimistic, Sagittarius natives seek meaning through exploration.' },
  capricorn:   { ruler: 'Saturn',  quality: 'Cardinal', desc: 'Capricorn is ruled by Saturn, the planet of discipline. Ambitious, patient, and pragmatic, Capricorn natives build lasting success through persistence and structure.' },
  aquarius:    { ruler: 'Saturn',  quality: 'Fixed',    desc: 'Aquarius is governed by Saturn and Rahu in Vedic astrology. Innovative, humanitarian, and independent, Aquarius natives are visionaries who champion progress.' },
  pisces:      { ruler: 'Jupiter', quality: 'Mutable',  desc: 'Pisces is ruled by Jupiter. Compassionate, intuitive, and spiritually attuned, Pisces natives move through the world with empathy, creativity, and deep faith.' },
};

const ELEMENT_STYLES = {
  Fire:  { color: 'text-amber-500',  bg: 'bg-amber-500/10',  border: 'border-amber-500/30'  },
  Earth: { color: 'text-green-500',  bg: 'bg-green-500/10',  border: 'border-green-500/30'  },
  Air:   { color: 'text-blue-400',   bg: 'bg-blue-400/10',   border: 'border-blue-400/30'   },
  Water: { color: 'text-cyan-500',   bg: 'bg-cyan-500/10',   border: 'border-cyan-500/30'   },
};

export const DailyHoroscopeSign = () => {
  const { sign } = useParams();
  const navigate = useNavigate();
  const shareCardRef = useRef(null);

  const [horoscope, setHoroscope] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const signData = ZODIAC_MAP[sign?.toLowerCase()];
  const meta = SIGN_META[sign?.toLowerCase()];

  // Redirect unknown sign slugs to the main daily horoscope page
  useEffect(() => {
    if (sign && !signData) navigate('/horoscope/daily', { replace: true });
  }, [sign, signData, navigate]);

  useEffect(() => {
    if (!signData) return;
    setLoading(true);
    setHoroscope(null);
    axios.get(`${API}/horoscope/${signData.id}/daily`)
      .then(r => setHoroscope(r.data))
      .catch(() => setError('Unable to load today\'s horoscope. Please try again.'))
      .finally(() => setLoading(false));
  }, [signData]);

  if (!signData || !meta) return null;

  const styles = ELEMENT_STYLES[signData.element] || ELEMENT_STYLES.Fire;
  const today = new Date().toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  const pageUrl = `https://www.everydayhoroscope.in/horoscope/daily/${signData.id}`;
  const currentIndex = ZODIAC_SIGNS_FULL.findIndex(s => s.id === signData.id);
  const prevSign = ZODIAC_SIGNS_FULL[(currentIndex + 11) % 12];
  const nextSign = ZODIAC_SIGNS_FULL[(currentIndex + 1) % 12];

  const schema = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        '@id': `${pageUrl}#webpage`,
        'name': `${signData.name} Daily Horoscope Today — Free Vedic Predictions`,
        'description': `Read today's free ${signData.name} daily horoscope. Vedic astrology predictions for love, career, health, and finances — rooted in 5,000 years of ancient wisdom.`,
        'url': pageUrl,
        'isPartOf': { '@id': 'https://www.everydayhoroscope.in/#website' },
        'publisher': { '@id': 'https://www.everydayhoroscope.in/#organization' },
        'about': {
          '@type': 'Thing',
          'name': `${signData.name} (${signData.dates})`,
          'description': meta.desc,
        },
        'breadcrumb': {
          '@type': 'BreadcrumbList',
          'itemListElement': [
            { '@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://www.everydayhoroscope.in' },
            { '@type': 'ListItem', 'position': 2, 'name': 'Daily Horoscope', 'item': 'https://www.everydayhoroscope.in/horoscope/daily' },
            { '@type': 'ListItem', 'position': 3, 'name': `${signData.name} Horoscope`, 'item': pageUrl },
          ],
        },
      },
    ],
  };

  return (
    <div className="min-h-screen pb-24 lg:pb-0">
      <SEO
        title={`${signData.name} Daily Horoscope Today — Free Vedic Predictions`}
        description={`Read today's free ${signData.name} daily horoscope. Vedic astrology predictions for love, career, health, and finances. ${signData.name} (${signData.dates}) — ruled by ${meta.ruler}.`}
        url={pageUrl}
        schema={schema}
      />

      <div className="py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">

          {/* Back + prev/next */}
          <div className="flex items-center justify-between mb-6">
            <Button onClick={() => navigate('/horoscope/daily')} variant="ghost" size="sm">
              <ArrowLeft className="h-4 w-4 mr-2" /> All Signs
            </Button>
            <div className="flex items-center gap-2">
              <Link
                to={`/horoscope/daily/${prevSign.id}`}
                className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground border border-border hover:border-gold/40 px-3 py-1.5 rounded-sm transition-all"
              >
                <ArrowLeft className="h-3 w-3" /> {prevSign.symbol} {prevSign.name}
              </Link>
              <Link
                to={`/horoscope/daily/${nextSign.id}`}
                className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground border border-border hover:border-gold/40 px-3 py-1.5 rounded-sm transition-all"
              >
                {nextSign.name} {nextSign.symbol} <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
          </div>

          {/* Sign hero */}
          <div className={`rounded-sm border ${styles.border} ${styles.bg} p-6 mb-6 flex flex-col sm:flex-row items-center sm:items-start gap-5`}>
            <div className={`text-7xl leading-none flex-shrink-0 ${styles.color}`}>{signData.symbol}</div>
            <div className="text-center sm:text-left">
              <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2 mb-2">
                <span className={`text-xs font-bold uppercase tracking-widest px-2 py-0.5 rounded-full ${styles.bg} ${styles.color} border ${styles.border}`}>
                  {signData.element}
                </span>
                <span className="text-xs text-muted-foreground border border-border px-2 py-0.5 rounded-full">
                  Ruled by {meta.ruler}
                </span>
                <span className="text-xs text-muted-foreground border border-border px-2 py-0.5 rounded-full">
                  {meta.quality}
                </span>
              </div>
              <h1 className="font-cinzel font-bold text-2xl sm:text-3xl mb-1">
                {signData.name} Daily Horoscope
              </h1>
              <p className="text-sm text-muted-foreground">{signData.dates} &nbsp;·&nbsp; {today}</p>
              <p className="text-sm text-muted-foreground mt-2 leading-relaxed max-w-lg">{meta.desc}</p>
            </div>
          </div>

          {/* Horoscope content */}
          {error ? (
            <Card className="p-6 text-center text-muted-foreground">{error}</Card>
          ) : (
            <HoroscopeCard
              title={`Today's ${signData.name} Horoscope`}
              content={horoscope?.content}
              isLoading={loading}
              type="daily"
              signName={signData.name}
              signSymbol={signData.symbol}
            />
          )}

          {/* Share */}
          {!loading && horoscope?.content && (
            <Card className="border border-gold/20 p-5 mt-6">
              <ShareButtons
                pageUrl={pageUrl}
                shareText={`${signData.name} Daily Horoscope — ${today} ${signData.symbol}`}
                cardRef={shareCardRef}
                filename={`horoscope-${signData.id}-daily`}
                fbPageCaption={`${signData.symbol} ${signData.name} Daily Horoscope — ${today}\n\n${horoscope?.content?.overview?.slice(0, 200)}...\n\n🔮 everydayhoroscope.in\n#${signData.name}Horoscope #VedicAstrology #EverydayHoroscope`}
              />
            </Card>
          )}

          <HoroscopeShareCard
            cardRef={shareCardRef}
            signName={signData.name}
            signSymbol={signData.symbol}
            signDates={signData.dates}
            signElement={signData.element}
            horoscopeType="daily"
            content={horoscope?.content}
          />

          {/* All 12 signs grid */}
          <div className="mt-10">
            <h2 className="font-playfair text-lg font-semibold mb-4 text-muted-foreground uppercase tracking-widest text-sm">
              All Zodiac Signs
            </h2>
            <div className="grid grid-cols-4 sm:grid-cols-6 gap-2">
              {ZODIAC_SIGNS_FULL.map(s => {
                const st = ELEMENT_STYLES[s.element];
                const isCurrent = s.id === signData.id;
                return (
                  <Link
                    key={s.id}
                    to={`/horoscope/daily/${s.id}`}
                    className={`flex flex-col items-center gap-1 p-3 rounded-sm border transition-all hover:-translate-y-0.5 ${
                      isCurrent
                        ? `border-gold bg-gold/10 shadow-[0_0_15px_-5px_rgba(197,160,89,0.4)]`
                        : `border-border bg-card hover:border-gold/40`
                    }`}
                  >
                    <span className={`text-2xl leading-none ${isCurrent ? 'text-gold' : st.color}`}>{s.symbol}</span>
                    <span className="text-[10px] font-semibold">{s.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* SEO CTA */}
          <div className="mt-10 rounded-sm border border-gold/20 bg-gold/[0.04] p-6 text-center">
            <Star className="h-6 w-6 text-gold mx-auto mb-3" />
            <h2 className="font-cinzel font-bold text-lg mb-2">Get Your Personalised Vedic Report</h2>
            <p className="text-sm text-muted-foreground mb-4 max-w-sm mx-auto">
              Your daily horoscope is just the beginning. Unlock your full Birth Chart, Kundali, and 43-day destiny roadmap.
            </p>
            <Button onClick={() => navigate('/register')} className="bg-gold hover:bg-gold/90 text-primary-foreground px-8">
              Start Free — No Card Required
            </Button>
          </div>

        </div>
      </div>
    </div>
  );
};
