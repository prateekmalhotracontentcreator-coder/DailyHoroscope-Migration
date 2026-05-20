import React, { useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { LoaderCircle, Sparkles, Stars } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const NAKSHATRA_DATA = {
  ashwini: { number: 1, lord: 'Ketu', deity: 'Ashwini Kumaras', symbol: 'Horse Head', qualities: ['Swift', 'Healing', 'Pioneering'], padaAkshar: ['Chu', 'Che', 'Cho', 'La'] },
  bharani: { number: 2, lord: 'Venus', deity: 'Yama', symbol: 'Yoni', qualities: ['Restraint', 'Creative', 'Transformative'], padaAkshar: ['Li', 'Lu', 'Le', 'Lo'] },
  krittika: { number: 3, lord: 'Sun', deity: 'Agni', symbol: 'Razor / Flame', qualities: ['Sharp', 'Purifying', 'Courageous'], padaAkshar: ['A', 'I', 'U', 'E'] },
  rohini: { number: 4, lord: 'Moon', deity: 'Brahma', symbol: 'Ox Cart', qualities: ['Creative', 'Fertile', 'Sensual'], padaAkshar: ['O', 'Va', 'Vi', 'Vu'] },
  mrigashira: { number: 5, lord: 'Mars', deity: 'Soma', symbol: 'Deer Head', qualities: ['Curious', 'Gentle', 'Seeking'], padaAkshar: ['Ve', 'Vo', 'Ka', 'Ki'] },
  ardra: { number: 6, lord: 'Rahu', deity: 'Rudra', symbol: 'Teardrop', qualities: ['Intense', 'Transforming', 'Cathartic'], padaAkshar: ['Ku', 'Gha', 'Ing', 'Jha'] },
  punarvasu: { number: 7, lord: 'Jupiter', deity: 'Aditi', symbol: 'Bow and Quiver', qualities: ['Generous', 'Returning', 'Nourishing'], padaAkshar: ['Ke', 'Ko', 'Ha', 'Hi'] },
  pushya: { number: 8, lord: 'Saturn', deity: 'Brihaspati', symbol: 'Flower / Circle', qualities: ['Protective', 'Spiritual', 'Nourishing'], padaAkshar: ['Hu', 'He', 'Ho', 'Da'] },
  ashlesha: { number: 9, lord: 'Mercury', deity: 'Nagas', symbol: 'Serpent', qualities: ['Penetrating', 'Mystical', 'Magnetic'], padaAkshar: ['Di', 'Du', 'De', 'Do'] },
  magha: { number: 10, lord: 'Ketu', deity: 'Pitrs', symbol: 'Throne', qualities: ['Regal', 'Ancestral', 'Authoritative'], padaAkshar: ['Ma', 'Mi', 'Mu', 'Me'] },
  purva_phalguni: { number: 11, lord: 'Venus', deity: 'Bhaga', symbol: 'Hammock', qualities: ['Pleasure', 'Creative', 'Romantic'], padaAkshar: ['Mo', 'Ta', 'Ti', 'Tu'] },
  uttara_phalguni: { number: 12, lord: 'Sun', deity: 'Aryaman', symbol: 'Bed Legs', qualities: ['Helpful', 'Responsible', 'Patron-like'], padaAkshar: ['Te', 'To', 'Pa', 'Pi'] },
  hasta: { number: 13, lord: 'Moon', deity: 'Savitar', symbol: 'Hand', qualities: ['Skilled', 'Dexterous', 'Resourceful'], padaAkshar: ['Pu', 'Sha', 'Na', 'Tha'] },
  chitra: { number: 14, lord: 'Mars', deity: 'Tvastar', symbol: 'Bright Jewel', qualities: ['Creative', 'Artistic', 'Perceptive'], padaAkshar: ['Pe', 'Po', 'Ra', 'Ri'] },
  swati: { number: 15, lord: 'Rahu', deity: 'Vayu', symbol: 'Coral / Sword', qualities: ['Independent', 'Flexible', 'Spreading'], padaAkshar: ['Ru', 'Re', 'Ro', 'Ta'] },
  vishakha: { number: 16, lord: 'Jupiter', deity: 'Indragni', symbol: 'Triumphal Arch', qualities: ['Goal-oriented', 'Determined', 'Competitive'], padaAkshar: ['Ti', 'Tu', 'Te', 'To'] },
  anuradha: { number: 17, lord: 'Saturn', deity: 'Mitra', symbol: 'Lotus', qualities: ['Devoted', 'Friendly', 'Disciplined'], padaAkshar: ['Na', 'Ni', 'Nu', 'Ne'] },
  jyeshtha: { number: 18, lord: 'Mercury', deity: 'Indra', symbol: 'Circular Amulet', qualities: ['Protective', 'Powerful', 'Senior'], padaAkshar: ['No', 'Ya', 'Yi', 'Yu'] },
  mula: { number: 19, lord: 'Ketu', deity: 'Niritti', symbol: 'Tied Roots', qualities: ['Investigative', 'Radical', 'Transforming'], padaAkshar: ['Ye', 'Yo', 'Bha', 'Bhi'] },
  purva_ashadha: { number: 20, lord: 'Venus', deity: 'Apas', symbol: 'Fan', qualities: ['Invincible', 'Purifying', 'Energising'], padaAkshar: ['Bhu', 'Dha', 'Pha', 'Da'] },
  uttara_ashadha: { number: 21, lord: 'Sun', deity: 'Vishvadevas', symbol: 'Elephant Tusk', qualities: ['Victorious', 'Responsible', 'Principled'], padaAkshar: ['Be', 'Bo', 'Ja', 'Ji'] },
  shravana: { number: 22, lord: 'Moon', deity: 'Vishnu', symbol: 'Ear', qualities: ['Learning', 'Listening', 'Connecting'], padaAkshar: ['Ju', 'Je', 'Jo', 'Gha'] },
  dhanishtha: { number: 23, lord: 'Mars', deity: 'Ashta Vasus', symbol: 'Drum', qualities: ['Wealthy', 'Musical', 'Courageous'], padaAkshar: ['Ga', 'Gi', 'Gu', 'Ge'] },
  shatabhisha: { number: 24, lord: 'Rahu', deity: 'Varuna', symbol: 'Empty Circle', qualities: ['Healing', 'Secretive', 'Mystical'], padaAkshar: ['Go', 'Sa', 'Si', 'Su'] },
  purva_bhadrapada: { number: 25, lord: 'Jupiter', deity: 'Aja Ekapad', symbol: 'Front Legs of Funeral Cot', qualities: ['Passionate', 'Fiery', 'Otherworldly'], padaAkshar: ['Se', 'So', 'Da', 'Di'] },
  uttara_bhadrapada: { number: 26, lord: 'Saturn', deity: 'Ahir Budhnya', symbol: 'Back Legs of Funeral Cot', qualities: ['Stable', 'Deep', 'Serpentine'], padaAkshar: ['Du', 'Tha', 'Jha', 'Da'] },
  revati: { number: 27, lord: 'Mercury', deity: 'Pushan', symbol: 'Fish / Drum', qualities: ['Nourishing', 'Protective', 'Completing'], padaAkshar: ['De', 'Do', 'Cha', 'Chi'] },
};

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: 'Nakshatra Calculator',
    applicationCategory: 'AstrologyApplication',
    operatingSystem: 'All',
    url: `${SITE}/nakshatra-calculator`,
    description: 'Find your birth Nakshatra and Pada with your date, time, and place of birth.',
    creator: {
      '@type': 'Organization',
      name: 'EverydayHoroscope',
    },
  };
}

function normalizeNakshatraKey(value) {
  return String(value || '')
    .trim()
    .toLowerCase()
    .replace(/[^a-z]+/g, '_')
    .replace(/^_+|_+$/g, '');
}

export function NakshatraCalculatorPage() {
  const [form, setForm] = useState({
    date_of_birth: '',
    time_of_birth: '',
    place_of_birth: '',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const nakshatraKey = normalizeNakshatraKey(result?.moon_nakshatra);
  const nakshatraData = nakshatraKey ? NAKSHATRA_DATA[nakshatraKey] : null;
  const padaIndex = Math.max((Number(result?.moon_nakshatra_pada) || 1) - 1, 0);

  const metaDescription = useMemo(
    () => 'Find your birth Nakshatra (lunar mansion) and Pada. Enter your date, time and place of birth for an accurate Vedic Nakshatra reading.',
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
        time_of_birth: form.time_of_birth,
        place_of_birth: form.place_of_birth,
        timezone: 'Asia/Kolkata',
      });
      setResult(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to calculate your Nakshatra right now.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="Nakshatra Calculator - Find Your Birth Star"
        description={metaDescription}
        url={`${SITE}/nakshatra-calculator`}
        schema={buildSchema()}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <Stars className="h-3.5 w-3.5" />
              Birth Star Finder
            </div>
            <div>
              <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                Nakshatra Calculator - Find Your Birth Star
              </h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                Discover your Moon Nakshatra, Pada, Dasha lord, and traditional naming syllables from your exact birth details.
              </p>
            </div>
          </div>
        </section>

        <div className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <div className="border-b border-gold/10 pb-4">
              <h2 className="text-xl font-semibold text-foreground">Enter your birth details</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Time and place are required here because Nakshatra and Pada depend on the Moon&apos;s exact degree.
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
                  required
                  value={form.time_of_birth}
                  onChange={(event) => setForm((current) => ({ ...current, time_of_birth: event.target.value }))}
                  className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-foreground">Place of Birth</span>
                <input
                  type="text"
                  required
                  value={form.place_of_birth}
                  onChange={(event) => setForm((current) => ({ ...current, place_of_birth: event.target.value }))}
                  placeholder="City, Country"
                  className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
                <p className="mt-2 text-xs text-muted-foreground">Public calculator timezone defaults to Asia/Kolkata.</p>
              </label>

              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : 'Calculate My Nakshatra'}
              </button>
            </form>
          </section>

          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <div className="border-b border-gold/10 pb-4">
              <h2 className="text-xl font-semibold text-foreground">Your result</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Nakshatra is the Moon&apos;s lunar mansion at birth, divided into 4 Padas.
              </p>
            </div>

            {loading && (
              <div className="flex min-h-80 flex-col items-center justify-center gap-3 text-center">
                <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
                <p className="text-sm text-muted-foreground">Calculating your birth star...</p>
              </div>
            )}

            {!loading && error && (
              <div className="mt-6 rounded-xl border border-red-500/20 bg-red-500/5 p-4 text-sm text-red-200">
                {error}
              </div>
            )}

            {!loading && !error && !result && (
              <div className="flex min-h-80 flex-col items-center justify-center text-center">
                <Sparkles className="h-10 w-10 text-gold/70" />
                <p className="mt-4 text-sm text-muted-foreground">
                  Submit your exact birth details to reveal your Nakshatra, Pada, and Dasha lord.
                </p>
              </div>
            )}

            {!loading && !error && result && nakshatraData && (
              <div className="mt-6 space-y-5">
                <div className="rounded-2xl border border-gold/20 bg-gradient-to-br from-gold/15 via-background to-background p-5">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Your Birth Nakshatra is</p>
                  <h3 className="mt-4 text-3xl font-playfair font-bold text-foreground">{result.moon_nakshatra}</h3>
                  <p className="mt-2 text-sm text-muted-foreground">
                    {nakshatraData.number}th Nakshatra · Pada {result.moon_nakshatra_pada}
                  </p>
                </div>

                <div className="rounded-xl border border-gold/20 bg-background/70 p-5">
                  <p className="text-sm text-muted-foreground">
                    Nakshatra Lord: <span className="font-semibold text-foreground">{nakshatraData.lord}</span> · Deity:{' '}
                    <span className="font-semibold text-foreground">{nakshatraData.deity}</span>
                  </p>
                  <p className="mt-2 text-sm text-muted-foreground">
                    Symbol: <span className="font-semibold text-foreground">{nakshatraData.symbol}</span> · Starting syllable:{' '}
                    <span className="font-semibold text-foreground">{nakshatraData.padaAkshar[padaIndex] || nakshatraData.padaAkshar[0]}</span>
                  </p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {nakshatraData.qualities.map((quality) => (
                      <span key={quality} className="rounded-full border border-gold/30 bg-gold/15 px-3 py-1 text-xs font-semibold text-gold">
                        {quality}
                      </span>
                    ))}
                  </div>
                  <p className="mt-4 text-sm leading-6 text-muted-foreground">
                    Your Vimshottari Dasha sequence starts with {nakshatraData.lord} Mahadasha, making this birth star central for timing, compatibility, and life rhythm interpretation.
                  </p>
                </div>

                <div className="rounded-xl border border-gold/20 bg-background/70 p-5">
                  <h3 className="text-base font-semibold text-foreground">Traditional naming guidance</h3>
                  <p className="mt-3 text-sm leading-6 text-muted-foreground">
                    Traditional Vedic names for this Nakshatra begin with: {nakshatraData.padaAkshar.join(', ')}.
                  </p>
                </div>
              </div>
            )}
          </section>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_1fr]">
          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">What is Nakshatra?</h2>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              The zodiac in Vedic astrology is divided into 27 lunar mansions called Nakshatras. Your birth Nakshatra comes from the Moon&apos;s exact position and is used for Dasha timing, naming, compatibility, and Muhurat work.
            </p>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              Each Nakshatra is further divided into 4 Padas, which refine expression and help determine traditional starting syllables for names.
            </p>
          </section>

          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">Go deeper with your full chart</h2>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              Your birth star is a key doorway into Dasha timing and karmic patterning. A full chart adds houses, planet strengths, yogas, and personalised life guidance.
            </p>
            <div className="mt-5 flex flex-wrap gap-3">
              <Link to="/birth-chart" className="inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90">
                Unlock Full Birth Chart and Dasha
              </Link>
              <Link to="/kundali-milan" className="inline-flex rounded-full border border-gold px-5 py-3 text-sm font-semibold text-gold transition hover:bg-gold/10">
                Check compatibility
              </Link>
            </div>
          </section>
        </div>

        <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">Related tools</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            <Link to="/rashi-calculator" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Find your Moon Sign (Rashi) ->
            </Link>
            <Link to="/kundali-milan" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Check Kundali Milan ->
            </Link>
            <Link to="/strategist" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Explore Dasha-based strategy ->
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
