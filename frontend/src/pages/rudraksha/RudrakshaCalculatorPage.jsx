import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { LoaderCircle, Sparkles } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import SharedBirthCityPicker from '../../components/SharedBirthCityPicker';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import {
  API,
  CALCULATOR_FAQ,
  SITE,
  buildBreadcrumbSchema,
  buildFaqSchema,
} from './rudrakshaUtils';

function buildCalculatorSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebApplication',
        name: 'Rudraksha Calculator',
        applicationCategory: 'AstrologyApplication',
        operatingSystem: 'All',
        url: `${SITE}/rudraksha/calculator`,
        description: 'Enter your birth details and get a personalised Rudraksha recommendation based on your Vedic birth chart.',
      },
      buildFaqSchema(CALCULATOR_FAQ),
      buildBreadcrumbSchema([
        { name: 'Home', item: SITE },
        { name: 'Rudraksha', item: `${SITE}/rudraksha` },
        { name: 'Calculator', item: `${SITE}/rudraksha/calculator` },
      ]),
    ],
  };
}

function RecommendationCard({ item, variant = 'primary' }) {
  const instructions = item.wearing_instructions || {};
  const isPrimary = variant === 'primary';
  return (
    <article className={`rounded-3xl border shadow-sm ${isPrimary ? 'border-gold/25 bg-[linear-gradient(135deg,rgba(197,160,89,0.18),rgba(255,255,255,0.94))] p-6' : 'border-gold/18 bg-white/80 p-5'}`}>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{isPrimary ? 'Primary recommendation' : 'Secondary recommendation'}</p>
          <h3 className="mt-3 font-cinzel text-4xl leading-none text-stone-900">{item.mukhi}</h3>
          <p className="mt-2 font-playfair text-xl font-semibold text-stone-900">{item.name}</p>
        </div>
        <Link to={`/rudraksha/${item.slug}`} className="rounded-full border border-gold/25 bg-white/80 px-3 py-1.5 text-xs font-semibold uppercase tracking-wide text-stone-700 transition hover:border-gold/40">
          Learn More
        </Link>
      </div>

      <p className="mt-4 text-sm leading-7 text-stone-700">{item.reason}</p>

      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        <div className="rounded-2xl border border-gold/12 bg-white/80 p-3">
          <p className="text-[11px] uppercase tracking-[0.2em] text-stone-500">Day</p>
          <p className="mt-2 text-sm font-semibold text-stone-900">{instructions.day}</p>
        </div>
        <div className="rounded-2xl border border-gold/12 bg-white/80 p-3">
          <p className="text-[11px] uppercase tracking-[0.2em] text-stone-500">Metal</p>
          <p className="mt-2 text-sm font-semibold text-stone-900">{instructions.metal}</p>
        </div>
        <div className="rounded-2xl border border-gold/12 bg-white/80 p-3">
          <p className="text-[11px] uppercase tracking-[0.2em] text-stone-500">Mantra</p>
          <p className="mt-2 text-sm font-semibold text-stone-900">{instructions.mantra}</p>
        </div>
      </div>
    </article>
  );
}

export function RudrakshaCalculatorPage() {
  const [form, setForm] = useState({
    date: '',
    time: '',
    city_slug: '',
    place: 'New Delhi',
    unknownTime: false,
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mukhis, setMukhis] = useState([]);

  useEffect(() => {
    let ignore = false;

    async function fetchMukhis() {
      try {
        const response = await axios.get(`${API}/mukhis`);
        if (!ignore) setMukhis(response.data || []);
      } catch {
        if (!ignore) setMukhis([]);
      }
    }

    fetchMukhis();
    return () => {
      ignore = true;
    };
  }, []);

  const mukhiMap = useMemo(
    () => Object.fromEntries(mukhis.map((item) => [item.mukhi, item])),
    [mukhis],
  );

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post(`${API}/calculator`, {
        date: form.date,
        time: form.unknownTime ? '12:00' : (form.time || '12:00'),
        place: form.place,
      });
      setResult(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Unable to calculate your Rudraksha right now.');
    } finally {
      setLoading(false);
    }
  }

  const universalMukhi = result?.universal?.mukhi ? mukhiMap[result.universal.mukhi] : null;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(197,160,89,0.18),_transparent_34%),linear-gradient(180deg,#fbf6ea_0%,#fffaf1_100%)] text-stone-900 flex flex-col">
      <SEO
        title="Rudraksha Calculator - Find Your Ideal Bead from Your Birth Chart"
        description="Enter your birth details and get a personalised Rudraksha recommendation based on your Vedic birth chart. Find the mukhi that strengthens your chart's weakest point."
        url={`${SITE}/rudraksha/calculator`}
        schema={buildCalculatorSchema()}
      />

      <main className="flex-1 px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <section className="rounded-[2rem] border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.16),rgba(255,255,255,0.95)_55%,rgba(252,248,240,0.95))] p-8 shadow-sm sm:p-10">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-white/75 px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
                <Sparkles className="h-3.5 w-3.5" />
                Birth Chart Matcher
              </div>
              <h1 className="mt-5 font-cinzel text-4xl leading-tight sm:text-5xl">
                Rudraksha Calculator - Find Your Ideal Bead from Your Birth Chart
              </h1>
              <p className="mt-4 max-w-2xl font-playfair text-lg italic leading-8 text-stone-700">
                This calculator uses your Vedic birth chart to look at Lagna, Moon sign, Mahadasha, and planetary pressure before suggesting a starting Rudraksha. It is designed as spiritual guidance, not as a replacement for personal judgement or professional advice.
              </p>
            </div>
          </section>

          <div className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
            <section className="rounded-3xl border border-gold/20 bg-white/80 p-6 shadow-sm">
              <div className="border-b border-gold/10 pb-4">
                <h2 className="font-playfair text-2xl font-semibold">Enter your birth details</h2>
                <p className="mt-2 text-sm leading-6 text-stone-600">
                  Place and time sharpen the chart. If you do not know your birth time, the calculator uses noon as a neutral public fallback.
                </p>
              </div>

              <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
                <label className="block">
                  <span className="text-sm font-medium text-stone-900">Date of birth</span>
                  <input
                    type="date"
                    required
                    value={form.date}
                    onChange={(event) => setForm((current) => ({ ...current, date: event.target.value }))}
                    className="mt-2 w-full rounded-xl border border-gold/25 bg-stone-50/70 px-4 py-3 text-sm outline-none transition focus:border-gold"
                  />
                </label>

                <label className="block">
                  <span className="text-sm font-medium text-stone-900">Time of birth</span>
                  <input
                    type="time"
                    value={form.unknownTime ? '12:00' : form.time}
                    onChange={(event) => setForm((current) => ({ ...current, time: event.target.value }))}
                    disabled={form.unknownTime}
                    className="mt-2 w-full rounded-xl border border-gold/25 bg-stone-50/70 px-4 py-3 text-sm outline-none transition focus:border-gold disabled:cursor-not-allowed disabled:opacity-70"
                  />
                </label>

                <label className="flex items-start gap-3 rounded-2xl border border-gold/15 bg-gold/[0.04] px-4 py-3 text-sm text-stone-700">
                  <input
                    type="checkbox"
                    checked={form.unknownTime}
                    onChange={(event) =>
                      setForm((current) => ({
                        ...current,
                        unknownTime: event.target.checked,
                        time: event.target.checked ? '' : current.time,
                      }))
                    }
                    className="mt-1 h-4 w-4 rounded border-gold/40"
                  />
                  <span>I don&apos;t know my birth time. Use 12:00 PM as a broad default.</span>
                </label>

                <div>
                  <SharedBirthCityPicker
                    inputId="rudraksha-birth-location"
                    label="Place of birth"
                    value={form.city_slug}
                    onChange={(city) =>
                      setForm((current) => ({
                        ...current,
                        city_slug: city.slug,
                        place: city.city_name,
                      }))
                    }
                    helpText="Choose from the supported location catalogue for a cleaner chart lookup."
                    labelStyle={{ display: 'block', fontSize: 14, fontWeight: 500, color: '#1c1917' }}
                    inputStyle={{
                      width: '100%',
                      borderRadius: 12,
                      border: '1px solid rgba(197,160,89,0.35)',
                      background: 'rgba(245,245,244,0.75)',
                      padding: '12px 16px',
                      fontSize: 14,
                      color: '#1c1917',
                    }}
                    selectStyle={{
                      width: '100%',
                      borderRadius: 12,
                      border: '1px solid rgba(197,160,89,0.35)',
                      background: 'rgba(245,245,244,0.75)',
                      padding: '12px 16px',
                      fontSize: 14,
                      color: '#1c1917',
                    }}
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading || !form.date || !form.place}
                  className="inline-flex items-center justify-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : 'Calculate My Rudraksha'}
                </button>
              </form>
            </section>

            <section className="rounded-3xl border border-gold/20 bg-white/80 p-6 shadow-sm">
              <div className="border-b border-gold/10 pb-4">
                <h2 className="font-playfair text-2xl font-semibold">Your recommendation</h2>
                <p className="mt-2 text-sm leading-6 text-stone-600">
                  The calculator ranks a primary bead, possible secondary supports, and keeps 5 Mukhi as a universal base.
                </p>
              </div>

              {loading && (
                <div className="flex min-h-[28rem] flex-col items-center justify-center gap-3">
                  <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
                  <p className="text-sm text-stone-600">Reading your chart signals...</p>
                </div>
              )}

              {!loading && error && (
                <div className="mt-6 rounded-2xl border border-red-400/30 bg-red-50 p-4 text-sm text-red-700">
                  {error}
                </div>
              )}

              {!loading && !error && !result && (
                <div className="flex min-h-[28rem] flex-col items-center justify-center text-center">
                  <Sparkles className="h-10 w-10 text-gold/70" />
                  <p className="mt-4 max-w-sm text-sm leading-7 text-stone-600">
                    Enter your birth details to generate a chart-based Rudraksha starting point, with day, mantra, and follow-up links for each bead.
                  </p>
                </div>
              )}

              {!loading && !error && result && (
                <div className="mt-6 space-y-5">
                  {result.chart_signals && (
                    <div className="grid gap-3 sm:grid-cols-2">
                      {[
                        ['Lagna', result.chart_signals.lagna],
                        ['Moon sign', result.chart_signals.moon_sign],
                        ['Current Mahadasha', result.chart_signals.current_mahadasha || 'Not available'],
                        ['Atmakaraka', result.chart_signals.atmakaraka || 'Not available'],
                      ].map(([label, value]) => (
                        <div key={label} className="rounded-2xl border border-gold/12 bg-stone-50/80 p-4">
                          <p className="text-[11px] uppercase tracking-[0.2em] text-stone-500">{label}</p>
                          <p className="mt-2 text-sm font-semibold text-stone-900">{value}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  <RecommendationCard item={result.primary} />

                  {result.secondary?.length > 0 && (
                    <div className="space-y-4">
                      {result.secondary.map((item) => (
                        <RecommendationCard key={`${item.mukhi}-${item.reason}`} item={item} variant="secondary" />
                      ))}
                    </div>
                  )}

                  <div className="rounded-2xl border border-gold/18 bg-stone-50/90 p-5">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Universal base</p>
                    <div className="mt-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                      <div>
                        <p className="font-playfair text-xl font-semibold text-stone-900">
                          {universalMukhi?.name || '5 Mukhi Rudraksha'}
                        </p>
                        <p className="mt-2 text-sm leading-7 text-stone-600">{result.universal?.note}</p>
                      </div>
                      <Link to={`/rudraksha/${result.universal?.slug || '5-mukhi'}`} className="text-sm font-semibold text-gold transition hover:underline">
                        Learn more about 5 Mukhi
                      </Link>
                    </div>
                  </div>

                  <div className="rounded-2xl border border-gold/12 bg-gold/[0.05] p-5">
                    <p className="text-sm leading-7 text-stone-700">
                      {result.disclaimer || 'This recommendation is based on Vedic astrology principles and is for spiritual guidance only.'}
                    </p>
                    <div className="mt-4 flex flex-wrap gap-3">
                      <Link to="/birth-chart" className="inline-flex rounded-full bg-stone-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-stone-800">
                        Get a deeper birth chart reading
                      </Link>
                      <Link to="/rudraksha" className="inline-flex rounded-full border border-gold/25 bg-white/80 px-4 py-2 text-sm font-semibold text-stone-800 transition hover:border-gold/40">
                        Explore all 21 mukhis
                      </Link>
                    </div>
                  </div>
                </div>
              )}
            </section>
          </div>

          <section className="mt-8 rounded-3xl border border-gold/20 bg-white/80 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">Frequently asked questions</h2>
            <Accordion type="single" collapsible className="mt-4">
              {CALCULATOR_FAQ.map((item) => (
                <AccordionItem key={item.question} value={item.question}>
                  <AccordionTrigger className="text-left text-base font-semibold text-stone-900">
                    {item.question}
                  </AccordionTrigger>
                  <AccordionContent className="text-sm leading-7 text-stone-600">
                    {item.answer}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default RudrakshaCalculatorPage;
