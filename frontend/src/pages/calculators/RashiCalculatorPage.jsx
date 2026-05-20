import React, { useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { LoaderCircle, MoonStar, Sparkles } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const RASHI_DATA = {
  aries: {
    hindi: 'Mesha',
    lord: 'Mars',
    element: 'Fire',
    quality: 'Cardinal',
    glyph: '\u2648',
    traits: ['Energetic', 'Courageous', 'Impulsive', 'Leadership'],
    interpretation: 'Aries Moon natives feel first and act fast. Your emotional world needs movement, challenge, and the freedom to back your instincts.',
  },
  taurus: {
    hindi: 'Vrishabha',
    lord: 'Venus',
    element: 'Earth',
    quality: 'Fixed',
    glyph: '\u2649',
    traits: ['Patient', 'Reliable', 'Artistic', 'Stubborn'],
    interpretation: 'Taurus Moon gives emotional steadiness and a deep need for comfort. You process life through loyalty, beauty, and tangible security.',
  },
  gemini: {
    hindi: 'Mithuna',
    lord: 'Mercury',
    element: 'Air',
    quality: 'Mutable',
    glyph: '\u264A',
    traits: ['Curious', 'Adaptable', 'Communicative', 'Restless'],
    interpretation: 'Gemini Moon makes the mind active and emotionally alert. You soothe yourself through conversation, information, and fresh perspective.',
  },
  cancer: {
    hindi: 'Karka',
    lord: 'Moon',
    element: 'Water',
    quality: 'Cardinal',
    glyph: '\u264B',
    traits: ['Intuitive', 'Nurturing', 'Emotional', 'Protective'],
    interpretation: 'Cancer Moon is deeply feeling, instinctive, and protective. Home, family, and emotional safety shape how you respond to the world.',
  },
  leo: {
    hindi: 'Simha',
    lord: 'Sun',
    element: 'Fire',
    quality: 'Fixed',
    glyph: '\u264C',
    traits: ['Creative', 'Generous', 'Charismatic', 'Proud'],
    interpretation: 'Leo Moon seeks warmth, recognition, and heartfelt expression. You thrive when your inner life is honoured and your generosity has room to shine.',
  },
  virgo: {
    hindi: 'Kanya',
    lord: 'Mercury',
    element: 'Earth',
    quality: 'Mutable',
    glyph: '\u264D',
    traits: ['Analytical', 'Perfectionist', 'Practical', 'Helpful'],
    interpretation: 'Virgo Moon notices details and wants order in emotional life. You feel stronger when you can improve, organise, and be of real use.',
  },
  libra: {
    hindi: 'Tula',
    lord: 'Venus',
    element: 'Air',
    quality: 'Cardinal',
    glyph: '\u264E',
    traits: ['Diplomatic', 'Charming', 'Indecisive', 'Fair'],
    interpretation: 'Libra Moon values harmony, balance, and emotional grace. Relationships often become the mirror through which you understand your feelings.',
  },
  scorpio: {
    hindi: 'Vrishchika',
    lord: 'Mars',
    element: 'Water',
    quality: 'Fixed',
    glyph: '\u264F',
    traits: ['Intense', 'Passionate', 'Secretive', 'Transformative'],
    interpretation: 'Scorpio Moon feels everything at depth and rarely loves halfway. Your emotional growth comes through trust, resilience, and transformation.',
  },
  sagittarius: {
    hindi: 'Dhanu',
    lord: 'Jupiter',
    element: 'Fire',
    quality: 'Mutable',
    glyph: '\u2650',
    traits: ['Optimistic', 'Adventurous', 'Philosophical', 'Restless'],
    interpretation: 'Sagittarius Moon needs meaning, hope, and room to expand. Your emotions settle when life feels purposeful and future-facing.',
  },
  capricorn: {
    hindi: 'Makara',
    lord: 'Saturn',
    element: 'Earth',
    quality: 'Cardinal',
    glyph: '\u2651',
    traits: ['Disciplined', 'Ambitious', 'Patient', 'Reserved'],
    interpretation: 'Capricorn Moon carries emotional maturity and a strong sense of duty. You often process feelings through responsibility, structure, and long-term thinking.',
  },
  aquarius: {
    hindi: 'Kumbha',
    lord: 'Saturn',
    element: 'Air',
    quality: 'Fixed',
    glyph: '\u2652',
    traits: ['Innovative', 'Independent', 'Humanitarian', 'Detached'],
    interpretation: 'Aquarius Moon blends emotional intelligence with objectivity. You need independence, original ideas, and a sense that your path matters to something larger.',
  },
  pisces: {
    hindi: 'Meena',
    lord: 'Jupiter',
    element: 'Water',
    quality: 'Mutable',
    glyph: '\u2653',
    traits: ['Intuitive', 'Creative', 'Compassionate', 'Escapist'],
    interpretation: 'Pisces Moon is imaginative, porous, and spiritually sensitive. You absorb atmospheres quickly and feel best with beauty, compassion, and healthy boundaries.',
  },
};

const ELEMENT_TONE = {
  Fire: 'from-orange-500/20 to-red-500/10',
  Earth: 'from-emerald-500/20 to-lime-500/10',
  Air: 'from-sky-500/20 to-cyan-500/10',
  Water: 'from-blue-600/20 to-indigo-500/10',
};

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: 'Rashi Calculator',
    applicationCategory: 'AstrologyApplication',
    operatingSystem: 'All',
    url: `${SITE}/rashi-calculator`,
    description: 'Find your Rashi (Vedic Moon sign) instantly with your date of birth, time, and place details.',
    creator: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
  };
}

function normalizeSignKey(value) {
  return String(value || '').trim().toLowerCase();
}

export function RashiCalculatorPage() {
  const [form, setForm] = useState({
    date_of_birth: '',
    time_of_birth: '',
    place_of_birth: 'New Delhi',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const signKey = normalizeSignKey(result?.moon_sign);
  const signData = signKey ? RASHI_DATA[signKey] : null;

  const metaDescription = useMemo(
    () => 'Find your Rashi (Vedic Moon sign) instantly. Enter your date of birth to get your Moon sign, ruling planet, traits and personalised insights.',
    [],
  );

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API}/calculate-birth-chart`, {
        date_of_birth: form.date_of_birth,
        time_of_birth: form.time_of_birth || undefined,
        place_of_birth: form.place_of_birth || 'New Delhi',
        timezone: 'Asia/Kolkata',
      });
      setResult(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to calculate your Rashi right now.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="Rashi Calculator - Find Your Vedic Moon Sign"
        description={metaDescription}
        url={`${SITE}/rashi-calculator`}
        schema={buildSchema()}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <MoonStar className="h-3.5 w-3.5" />
              Free Vedic Calculator
            </div>
            <div>
              <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                Rashi Calculator - Find Your Vedic Moon Sign
              </h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                Enter your birth details to discover your Rashi, the Moon sign used in Vedic astrology for emotional nature, instinct, and inner temperament.
              </p>
            </div>
          </div>
        </section>

        <div className="mt-8 grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <div className="border-b border-gold/10 pb-4">
              <h2 className="text-xl font-semibold text-foreground">Enter your birth details</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Date is required. Time and place improve accuracy, especially near sign transitions.
              </p>
            </div>

            <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
              <label className="block">
                <span className="text-sm font-medium text-foreground">Date of Birth</span>
                <input
                  type="date"
                  required
                  value={form.date_of_birth}
                  onChange={(event) => setForm((current) => ({ ...current, date_of_birth: event.target.value }))}
                  className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-foreground">Time of Birth</span>
                <input
                  type="time"
                  value={form.time_of_birth}
                  onChange={(event) => setForm((current) => ({ ...current, time_of_birth: event.target.value }))}
                  className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
                <p className="mt-2 text-xs text-muted-foreground">Optional, but helpful for a finer Moon degree reading.</p>
              </label>

              <label className="block">
                <span className="text-sm font-medium text-foreground">Place of Birth</span>
                <input
                  type="text"
                  value={form.place_of_birth}
                  onChange={(event) => setForm((current) => ({ ...current, place_of_birth: event.target.value }))}
                  placeholder="New Delhi"
                  className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
                <p className="mt-2 text-xs text-muted-foreground">Default timezone for this public calculator is Asia/Kolkata.</p>
              </label>

              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : 'Calculate My Rashi'}
              </button>
            </form>
          </section>

          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <div className="border-b border-gold/10 pb-4">
              <h2 className="text-xl font-semibold text-foreground">Your result</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Your Rashi comes from the Moon&apos;s sign at the moment of birth.
              </p>
            </div>

            {loading && (
              <div className="flex min-h-72 flex-col items-center justify-center gap-3 text-center">
                <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
                <p className="text-sm text-muted-foreground">Calculating your Moon sign...</p>
              </div>
            )}

            {!loading && error && (
              <div className="mt-6 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-200">
                {error}
              </div>
            )}

            {!loading && !error && !result && (
              <div className="flex min-h-72 flex-col items-center justify-center text-center">
                <MoonStar className="h-10 w-10 text-gold/70" />
                <p className="mt-4 text-sm text-muted-foreground">
                  Submit your birth details to reveal your Vedic Moon sign and key personality traits.
                </p>
              </div>
            )}

            {!loading && !error && result && signData && (
              <div className="mt-6 space-y-5">
                <div className={`rounded-2xl border border-gold/20 bg-gradient-to-br ${ELEMENT_TONE[signData.element]} p-5`}>
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Your Rashi (Moon Sign) is</p>
                  <div className="mt-4 flex items-center gap-4">
                    <div className="flex h-20 w-20 items-center justify-center rounded-full border border-gold/20 bg-background/75 text-5xl text-gold shadow-sm">
                      {signData.glyph}
                    </div>
                    <div>
                      <h3 className="text-3xl font-playfair font-bold text-foreground">{result.moon_sign}</h3>
                      <p className="mt-1 text-sm text-muted-foreground">{signData.hindi}</p>
                      {typeof result.moon_degree === 'number' && (
                        <p className="mt-2 text-sm text-muted-foreground">Moon degree: {result.moon_degree.toFixed(2)}°</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="rounded-xl border border-gold/20 bg-background/70 p-5">
                  <p className="text-sm text-muted-foreground">
                    Lord: <span className="font-semibold text-foreground">{signData.lord}</span> · Element:{' '}
                    <span className="font-semibold text-foreground">{signData.element}</span> · Quality:{' '}
                    <span className="font-semibold text-foreground">{signData.quality}</span>
                  </p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {signData.traits.map((trait) => (
                      <span key={trait} className="rounded-full border border-gold/30 bg-gold/15 px-3 py-1 text-xs font-semibold text-gold">
                        {trait}
                      </span>
                    ))}
                  </div>
                  <p className="mt-4 text-sm leading-6 text-muted-foreground">{signData.interpretation}</p>
                </div>
              </div>
            )}
          </section>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_1fr]">
          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">What is Rashi?</h2>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              In Vedic astrology, Rashi means your Moon sign, not your Sun sign. It reflects emotional patterning, instinctive reactions, and the inner lens through which you experience relationships, comfort, and security.
            </p>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              Western astrology focuses on the Sun sign by birth date, while Vedic astrology gives special weight to the Moon because it moves faster and captures the lived texture of the mind.
            </p>
          </section>

          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">Discover your full Vedic profile</h2>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              Your Rashi is only one layer. A full birth chart shows planets, houses, dashas, and karmic timing unique to your exact birth details.
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link to="/birth-chart" className="inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90">
                Unlock Full Birth Chart
              </Link>
              <Link to="/strategist" className="inline-flex rounded-full border border-gold px-5 py-3 text-sm font-semibold text-gold transition hover:bg-gold/10">
                Explore The Strategist
              </Link>
            </div>
          </section>
        </div>

        <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">Related tools</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Link to="/nakshatra-calculator" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Find your Nakshatra ->
            </Link>
            <Link to="/kundali-milan" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Check compatibility ->
            </Link>
            <Link to="/birth-chart" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Unlock your full Kundali ->
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
