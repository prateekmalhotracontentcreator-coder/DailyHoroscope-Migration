import React, { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { ArrowLeft, Sparkles } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { HoroscopeCard } from '../../components/HoroscopeCard';
import { Button } from '../../components/ui/button';
import { Card } from '../../components/ui/card';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const SIGNS = {
  aries:       { name: 'Aries',       dates: 'Mar 21 - Apr 19', element: 'Fire',  glyph: '\u2648' },
  taurus:      { name: 'Taurus',      dates: 'Apr 20 - May 20', element: 'Earth', glyph: '\u2649' },
  gemini:      { name: 'Gemini',      dates: 'May 21 - Jun 20', element: 'Air',   glyph: '\u264a' },
  cancer:      { name: 'Cancer',      dates: 'Jun 21 - Jul 22', element: 'Water', glyph: '\u264b' },
  leo:         { name: 'Leo',         dates: 'Jul 23 - Aug 22', element: 'Fire',  glyph: '\u264c' },
  virgo:       { name: 'Virgo',       dates: 'Aug 23 - Sep 22', element: 'Earth', glyph: '\u264d' },
  libra:       { name: 'Libra',       dates: 'Sep 23 - Oct 22', element: 'Air',   glyph: '\u264e' },
  scorpio:     { name: 'Scorpio',     dates: 'Oct 23 - Nov 21', element: 'Water', glyph: '\u264f' },
  sagittarius: { name: 'Sagittarius', dates: 'Nov 22 - Dec 21', element: 'Fire',  glyph: '\u2650' },
  capricorn:   { name: 'Capricorn',   dates: 'Dec 22 - Jan 19', element: 'Earth', glyph: '\u2651' },
  aquarius:    { name: 'Aquarius',    dates: 'Jan 20 - Feb 18', element: 'Air',   glyph: '\u2652' },
  pisces:      { name: 'Pisces',      dates: 'Feb 19 - Mar 20', element: 'Water', glyph: '\u2653' },
};

const ELEMENT_COLORS = {
  Fire: 'from-orange-500/20 to-red-500/10',
  Earth: 'from-green-600/20 to-emerald-500/10',
  Air: 'from-sky-400/20 to-blue-400/10',
  Water: 'from-blue-600/20 to-indigo-500/10',
};

const PERIOD_META = {
  tomorrow: {
    label: 'Tomorrow',
    heading: 'Tomorrow Horoscope',
    apiType: 'tomorrow',
    title: (sign) => `${sign} Horoscope Tomorrow - Vedic Prediction`,
    description: (sign) => `Get your ${sign} horoscope for tomorrow. Vedic astrology prediction for love, career, health and lucky elements.`,
    pageHeading: (sign) => `${sign} Horoscope Tomorrow`,
    dateLabel: (date) => `For ${date}`,
    ctaLabel: 'View Full Tomorrow Horoscope',
    overviewLabel: 'Tomorrow Forecast',
    ctaHref: '/horoscope/daily',
  },
  weekly: {
    label: 'Weekly',
    heading: 'Weekly Horoscope',
    apiType: 'weekly',
    title: (sign) => `${sign} Weekly Horoscope - This Week's Vedic Forecast`,
    description: (sign) => `${sign} weekly horoscope - your 7-day Vedic forecast for love, career, and wellness. Updated every week.`,
    pageHeading: (sign) => `${sign} Weekly Horoscope`,
    dateLabel: (date) => `Week of ${date}`,
    ctaLabel: 'View Full Weekly Horoscope',
    overviewLabel: 'This Week Forecast',
    ctaHref: '/horoscope/weekly',
  },
  monthly: {
    label: 'Monthly',
    heading: 'Monthly Horoscope',
    apiType: 'monthly',
    title: (sign, monthYear) => `${sign} Monthly Horoscope - ${monthYear} Vedic Forecast`,
    description: (sign, monthYear) => `${sign} horoscope for ${monthYear} - full monthly Vedic forecast covering love, career, health, and auspicious dates.`,
    pageHeading: (sign) => `${sign} Monthly Horoscope`,
    dateLabel: (date) => date,
    ctaLabel: 'View Full Monthly Horoscope',
    overviewLabel: 'This Month Forecast',
    ctaHref: '/horoscope/monthly',
  },
};

function formatPredictionDate(predictionDate, period) {
  if (!predictionDate) return '';
  const parsed = new Date(`${predictionDate}T12:00:00`);
  if (period === 'monthly') {
    return parsed.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' });
  }
  return parsed.toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

function buildArticleSchema(signName, periodLabel, canonicalUrl, predictionDate) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: `${signName} ${periodLabel} Horoscope`,
    datePublished: predictionDate,
    dateModified: predictionDate,
    mainEntityOfPage: canonicalUrl,
    author: { '@type': 'Organization', name: 'EverydayHoroscope' },
    publisher: { '@type': 'Organization', name: 'EverydayHoroscope', url: SITE },
  };
}

export function HoroscopeSignPage({ period }) {
  const { sign } = useParams();
  const navigate = useNavigate();
  const [horoscope, setHoroscope] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const signKey = sign?.toLowerCase();
  const signMeta = signKey ? SIGNS[signKey] : null;
  const periodMeta = PERIOD_META[period];

  useEffect(() => {
    if (sign && !signMeta) {
      navigate('/horoscope/daily', { replace: true });
    }
  }, [navigate, sign, signMeta]);

  useEffect(() => {
    let ignore = false;

    async function fetchHoroscope() {
      if (!signMeta || !periodMeta) return;
      try {
        setLoading(true);
        setError('');
        setHoroscope(null);
        const response = await axios.post(`${API}/horoscope/generate`, {
          sign: signKey,
          type: periodMeta.apiType,
        });
        if (!ignore) setHoroscope(response.data);
      } catch {
        if (!ignore) setError('Unable to load this horoscope right now. Please try again shortly.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchHoroscope();
    return () => {
      ignore = true;
    };
  }, [periodMeta, signKey, signMeta]);

  const monthYear = useMemo(() => {
    const reference = period === 'monthly' && horoscope?.prediction_date
      ? new Date(`${horoscope.prediction_date}T12:00:00`)
      : new Date();
    return reference.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' });
  }, [horoscope?.prediction_date, period]);

  const canonicalUrl = signMeta ? `${SITE}/horoscope/${signKey}/${period}` : `${SITE}/horoscope/daily`;
  const predictionLabel = horoscope?.prediction_date ? formatPredictionDate(horoscope.prediction_date, period) : monthYear;
  const title = signMeta ? periodMeta.title(signMeta.name, monthYear) : 'Horoscope';
  const description = signMeta ? periodMeta.description(signMeta.name, monthYear) : 'Vedic horoscope.';
  const schema = signMeta
    ? buildArticleSchema(signMeta.name, periodMeta.label, canonicalUrl, horoscope?.prediction_date || new Date().toISOString().slice(0, 10))
    : null;

  if (!signMeta || !periodMeta) return null;

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO title={title} description={description} url={canonicalUrl} schema={schema} />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <Button onClick={() => navigate('/horoscope/daily')} variant="ghost" className="mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" /> Back to Horoscope Home
        </Button>

        <section className={`rounded-3xl border border-gold/20 bg-gradient-to-br ${ELEMENT_COLORS[signMeta.element]} p-8 shadow-sm`}>
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="flex items-start gap-5">
              <div className="flex h-24 w-24 items-center justify-center rounded-full border border-gold/20 bg-background/70 text-6xl shadow-sm">
                {signMeta.glyph}
              </div>
              <div>
                <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/15 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                  <Sparkles className="h-3.5 w-3.5" />
                  {periodMeta.label}
                </div>
                <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                  {periodMeta.pageHeading(signMeta.name)}
                </h1>
                <p className="mt-2 text-sm text-muted-foreground">
                  {signMeta.dates} · {signMeta.element} sign
                </p>
                <p className="mt-2 text-sm text-muted-foreground">
                  {periodMeta.dateLabel(predictionLabel)}
                </p>
              </div>
            </div>

            <div className="flex flex-wrap gap-2">
              {Object.entries(PERIOD_META).map(([periodKey, item]) => (
                <Link
                  key={periodKey}
                  to={`/horoscope/${signKey}/${periodKey}`}
                  className={`rounded-full border px-4 py-2 text-sm font-semibold transition ${
                    periodKey === period
                      ? 'border-gold/40 bg-gold/15 text-gold'
                      : 'border-border bg-background/70 text-muted-foreground hover:border-gold/30 hover:text-gold'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </section>

        <div className="mt-8">
          {error ? (
            <Card className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
              <p className="text-sm text-muted-foreground">{error}</p>
            </Card>
          ) : (
            <HoroscopeCard
              title={periodMeta.heading}
              content={horoscope?.content}
              isLoading={loading}
              type={period}
              signName={signMeta.name}
              signSymbol={signMeta.glyph}
              dateLabel={periodMeta.dateLabel(predictionLabel)}
            />
          )}
        </div>

        <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">Want a reading that's personalised to your exact birth chart?</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-muted-foreground">
            General sign horoscopes are a strong starting point, but your birth chart reveals the timing, strengths, and karmic patterns unique to you.
          </p>
          <Link
            to="/birth-chart"
            className="mt-5 inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90"
          >
            Unlock Your Birth Chart
          </Link>
        </section>

        <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">Browse all zodiac signs for {periodMeta.label.toLowerCase()}</h2>
          <div className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            {Object.entries(SIGNS).map(([slug, item]) => (
              <Link
                key={slug}
                to={`/horoscope/${slug}/${period}`}
                className={`flex items-center gap-3 rounded-full border px-4 py-3 text-sm transition ${
                  slug === signKey
                    ? 'border-gold/40 bg-gold/20 text-foreground'
                    : 'border-border bg-background/70 text-muted-foreground hover:border-gold/30 hover:text-foreground'
                }`}
              >
                <span className="text-xl">{item.glyph}</span>
                <span className="font-medium">{item.name}</span>
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-8 text-center">
          <p className="text-sm text-muted-foreground">
            Explore your full {periodMeta.label.toLowerCase()} horoscope across all areas of life.
          </p>
          <Link
            to={periodMeta.ctaHref}
            className="mt-4 inline-flex rounded-full border border-gold px-5 py-3 text-sm font-semibold text-gold transition hover:bg-gold/10"
          >
            {periodMeta.ctaLabel}
          </Link>
        </section>
      </main>

      <Footer />
    </div>
  );
}
