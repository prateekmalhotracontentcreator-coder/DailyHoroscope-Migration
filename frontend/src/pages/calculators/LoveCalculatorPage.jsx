import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import { Copy, Heart, LoaderCircle, RotateCcw, Sparkles } from 'lucide-react';
import { toast } from 'sonner';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/numerology`;
const SITE = 'https://www.everydayhoroscope.in';
const CIRCLE = 2 * Math.PI * 54;

const BAND_STYLES = {
  cosmic: 'border-gold/40 bg-gold/[0.08] text-gold',
  high: 'border-pink-400/30 bg-pink-500/15 text-pink-300',
  good: 'border-emerald-400/30 bg-emerald-500/15 text-emerald-300',
  moderate: 'border-sky-400/30 bg-sky-500/15 text-sky-300',
  challenging: 'border-amber-400/30 bg-amber-500/15 text-amber-300',
  low: 'border-red-400/30 bg-red-500/15 text-red-300',
};

const FAQ_ITEMS = [
  {
    question: 'Is the love calculator accurate?',
    answer: 'It is best used as a symbolic compatibility snapshot. A strong score suggests smoother resonance, while a mixed score highlights where patience, communication, and awareness matter more.',
  },
  {
    question: "What's the difference between name and birth date mode?",
    answer: 'Name mode compares Chaldean name vibrations, while birth date mode compares Life Path numbers derived from date of birth. Together they reveal different layers of relationship chemistry.',
  },
  {
    question: 'What does a high compatibility score mean?',
    answer: 'A high score usually points to stronger emotional rhythm, easier communication, and better energetic flow between two people. It does not replace maturity or real-life effort, but it suggests a naturally supportive pattern.',
  },
  {
    question: 'How is this different from Kundali matching?',
    answer: 'This calculator uses numerology only for a quick public reading. Kundali matching goes much deeper through birth-chart factors such as Moon sign, Nakshatra, houses, and dasha timing.',
  },
];

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebApplication',
        applicationCategory: 'AstrologyApplication',
        name: 'Love Calculator',
        description: 'Vedic numerology love compatibility calculator',
        operatingSystem: 'All',
        url: `${SITE}/love-calculator`,
      },
      {
        '@type': 'FAQPage',
        mainEntity: FAQ_ITEMS.map((item) => ({
          '@type': 'Question',
          name: item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.answer,
          },
        })),
      },
    ],
  };
}

function normalizeName(value) {
  return value.replace(/\s+/g, ' ').trim();
}

function buildShareUrl(mode, result) {
  const params = new URLSearchParams();
  if (mode === 'name' && result?.name1 && result?.name2) {
    params.set('m', 'name');
    params.set('n1', result.name1);
    params.set('n2', result.name2);
  }
  if (mode === 'birthdate' && result?.dob1 && result?.dob2) {
    params.set('m', 'dob');
    params.set('d1', result.dob1);
    params.set('d2', result.dob2);
  }
  const query = params.toString();
  return `${SITE}/love-calculator${query ? `?${query}` : ''}`;
}

export function LoveCalculatorPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialMode = searchParams.get('m') === 'dob' ? 'birthdate' : 'name';
  const [mode, setMode] = useState(initialMode);
  const [form, setForm] = useState({
    name1: searchParams.get('n1') || '',
    name2: searchParams.get('n2') || '',
    dob1: searchParams.get('d1') || '',
    dob2: searchParams.get('d2') || '',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const queryMode = searchParams.get('m') === 'dob' ? 'birthdate' : 'name';
    setMode(queryMode);
    setForm({
      name1: searchParams.get('n1') || '',
      name2: searchParams.get('n2') || '',
      dob1: searchParams.get('d1') || '',
      dob2: searchParams.get('d2') || '',
    });
  }, [searchParams]);

  useEffect(() => {
    const queryMode = searchParams.get('m') === 'dob' ? 'birthdate' : searchParams.get('m') === 'name' ? 'name' : '';
    if (!queryMode) return;
    if (queryMode === 'name') {
      const n1 = normalizeName(searchParams.get('n1') || '');
      const n2 = normalizeName(searchParams.get('n2') || '');
      if (!n1 || !n2) return;
      void runCalculation('name', { name1: n1, name2: n2 }, false);
      return;
    }
    const d1 = (searchParams.get('d1') || '').trim();
    const d2 = (searchParams.get('d2') || '').trim();
    if (!d1 || !d2) return;
    void runCalculation('birthdate', { dob1: d1, dob2: d2 }, false);
  }, [searchParams]);

  async function runCalculation(nextMode, values, syncParams = true) {
    setLoading(true);
    setError('');

    const payload = nextMode === 'name'
      ? { mode: 'name', name1: normalizeName(values.name1 || ''), name2: normalizeName(values.name2 || '') }
      : { mode: 'birthdate', dob1: (values.dob1 || '').trim(), dob2: (values.dob2 || '').trim() };

    try {
      const response = await axios.post(`${API}/love-calculator`, payload);
      setResult(response.data);
      if (syncParams) {
        if (nextMode === 'name') {
          setSearchParams({ m: 'name', n1: response.data.name1, n2: response.data.name2 });
        } else {
          setSearchParams({ m: 'dob', d1: response.data.dob1, d2: response.data.dob2 });
        }
      }
    } catch (err) {
      setResult(null);
      setError(err?.response?.data?.detail || 'Unable to calculate compatibility right now.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    await runCalculation(mode, form, true);
  }

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(buildShareUrl(mode, result));
      toast.success('Compatibility link copied');
    } catch {
      toast.error('Could not copy the result link');
    }
  }

  function handleReset() {
    setForm({ name1: '', name2: '', dob1: '', dob2: '' });
    setResult(null);
    setError('');
    setSearchParams({});
  }

  function changeMode(nextMode) {
    setMode(nextMode);
    setResult(null);
    setError('');
  }

  const dynamicTitle = useMemo(() => {
    if (!result) return 'Love Calculator - Check Your Compatibility';
    if (result.mode === 'name' && result.name1 && result.name2) {
      return `${result.name1} + ${result.name2} = ${result.score}% Compatible 💕`;
    }
    if (result.mode === 'birthdate' && result.dob1 && result.dob2) {
      return `${result.score}% Love Match - Birth Date Compatibility`;
    }
    return 'Love Calculator - Check Your Compatibility';
  }, [result]);

  const ringOffset = useMemo(() => CIRCLE - (CIRCLE * (result?.score || 0)) / 100, [result?.score]);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={dynamicTitle}
        description="Find your love compatibility score instantly. Enter two names or birth dates to calculate your cosmic connection - powered by Vedic numerology."
        url={result ? buildShareUrl(mode, result) : `${SITE}/love-calculator`}
        schema={buildSchema()}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <Sparkles className="h-3.5 w-3.5" />
              Vedic Numerology
            </div>
            <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
              Love Calculator
            </h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
              Discover your cosmic compatibility through Vedic numerology. Check connection by name or by birth date, then share the result with a single link.
            </p>
          </div>
        </section>

        <div className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
          <section className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
            <div className="flex gap-3 rounded-full border border-gold/20 bg-gold/[0.04] p-2">
              {[
                ['name', 'By Name'],
                ['birthdate', 'By Birth Date'],
              ].map(([value, label]) => (
                <button
                  key={value}
                  type="button"
                  onClick={() => changeMode(value)}
                  className={`flex-1 rounded-full px-4 py-2 text-sm font-semibold transition ${
                    mode === value
                      ? 'bg-gold text-primary-foreground'
                      : 'border border-gold/30 text-gold'
                  }`}
                >
                  {label}
                </button>
              ))}
            </div>

            <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
              {mode === 'name' ? (
                <>
                  <label className="block">
                    <span className="text-sm font-medium text-foreground">Your name</span>
                    <input
                      type="text"
                      value={form.name1}
                      onChange={(event) => setForm((current) => ({ ...current, name1: event.target.value }))}
                      className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                      placeholder="Priya"
                    />
                  </label>
                  <div className="flex justify-center text-2xl text-gold">
                    <Heart className="h-6 w-6 fill-current" />
                  </div>
                  <label className="block">
                    <span className="text-sm font-medium text-foreground">Their name</span>
                    <input
                      type="text"
                      value={form.name2}
                      onChange={(event) => setForm((current) => ({ ...current, name2: event.target.value }))}
                      className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                      placeholder="Arjun"
                    />
                  </label>
                </>
              ) : (
                <>
                  <label className="block">
                    <span className="text-sm font-medium text-foreground">Your date of birth</span>
                    <input
                      type="date"
                      value={form.dob1}
                      onChange={(event) => setForm((current) => ({ ...current, dob1: event.target.value }))}
                      className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                    />
                  </label>
                  <div className="flex justify-center text-2xl text-gold">
                    <Heart className="h-6 w-6 fill-current" />
                  </div>
                  <label className="block">
                    <span className="text-sm font-medium text-foreground">Their date of birth</span>
                    <input
                      type="date"
                      value={form.dob2}
                      onChange={(event) => setForm((current) => ({ ...current, dob2: event.target.value }))}
                      className="mt-2 w-full rounded-xl border border-gold/30 bg-background px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                    />
                  </label>
                </>
              )}

              <button
                type="submit"
                disabled={loading}
                className="inline-flex w-full items-center justify-center rounded-xl bg-gold px-5 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {loading ? <LoaderCircle className="mr-2 h-4 w-4 animate-spin" /> : null}
                Calculate Love Score
              </button>

              {error ? (
                <div className="rounded-xl border border-red-400/20 bg-red-500/10 p-4 text-sm text-red-200">
                  {error}
                </div>
              ) : null}
            </form>
          </section>

          <section className={`rounded-2xl border p-6 shadow-sm ${result ? BAND_STYLES[result.band] : 'border-gold/20 bg-background/80 text-foreground'}`}>
            {!result ? (
              <div className="flex h-full min-h-[360px] items-center justify-center text-center text-sm text-muted-foreground">
                Enter two names or two birth dates to reveal your compatibility score.
              </div>
            ) : (
              <div className="space-y-6">
                <div className="flex flex-col items-center text-center">
                  <div className="relative h-40 w-40">
                    <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
                      <circle cx="60" cy="60" r="54" fill="none" stroke="rgba(197,160,89,0.18)" strokeWidth="10" />
                      <circle
                        cx="60"
                        cy="60"
                        r="54"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="10"
                        strokeLinecap="round"
                        strokeDasharray={CIRCLE}
                        strokeDashoffset={ringOffset}
                        style={{ transition: 'stroke-dashoffset 900ms ease' }}
                      />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                      <p className="text-5xl font-semibold text-gold">{result.score}%</p>
                    </div>
                  </div>
                  <p className="mt-4 text-2xl font-playfair italic text-foreground">{result.label}</p>
                  <p className="mt-3 max-w-xl text-sm leading-6 text-muted-foreground">{result.description}</p>
                </div>

                <div className="grid gap-4 sm:grid-cols-3">
                  {[
                    ['Mind', result.elements.mind],
                    ['Heart', result.elements.heart],
                    ['Energy', result.elements.energy],
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-xl border border-gold/15 bg-background/80 p-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="font-medium text-foreground">{label} compatibility</span>
                        <span className="text-gold">{value}%</span>
                      </div>
                      <div className="mt-3 h-2 rounded-full bg-muted">
                        <div className="h-2 rounded-full bg-gold transition-all duration-700" style={{ width: `${value}%` }} />
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    type="button"
                    onClick={handleCopy}
                    className="inline-flex items-center justify-center rounded-lg bg-gold px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90"
                  >
                    <Copy className="mr-2 h-4 w-4" />
                    Share your score
                  </button>
                  <button
                    type="button"
                    onClick={handleReset}
                    className="inline-flex items-center justify-center rounded-lg border border-gold/30 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/[0.06]"
                  >
                    <RotateCcw className="mr-2 h-4 w-4" />
                    Calculate again
                  </button>
                </div>
              </div>
            )}
          </section>
        </div>

        <section className="mt-10 rounded-2xl border border-gold/20 bg-gold/[0.05] p-6 shadow-sm">
          <h2 className="text-2xl font-playfair font-bold text-foreground">Want the full picture?</h2>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            {[
              {
                title: 'Relationship Numerology Report',
                body: 'Explore the deeper number patterns behind emotional flow, attraction, and long-term harmony.',
                href: '/numerology',
              },
              {
                title: 'Kundali Milan',
                body: 'Compare full birth charts through traditional Vedic compatibility matching.',
                href: '/kundali-milan',
              },
              {
                title: 'Love Weather Report',
                body: 'See the current planetary climate shaping your romantic life and timing windows.',
                href: '/love-weather-report',
              },
            ].map((item) => (
              <Link key={item.title} to={item.href} className="rounded-xl border border-gold/20 bg-background/80 p-5 shadow-sm transition hover:border-gold/40 hover:bg-gold/[0.04]">
                <h3 className="text-lg font-semibold text-foreground">{item.title}</h3>
                <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.body}</p>
                <p className="mt-4 text-sm font-semibold text-gold">Explore</p>
              </Link>
            ))}
          </div>
          <p className="mt-5 text-sm text-muted-foreground">
            Premium members get unlimited love readings and deeper compatibility reports across numerology and Vedic astrology.
          </p>
        </section>

        <section className="mt-10 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">How it works</h2>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            Vedic numerology assigns each name or birth date a cosmic number. The compatibility between two numbers reveals relationship dynamics across mind, heart, and energy.
          </p>
        </section>

        <section className="mt-10 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
          <h2 className="text-2xl font-playfair font-bold text-foreground">Love Calculator FAQ</h2>
          <Accordion type="single" collapsible className="mt-4">
            {FAQ_ITEMS.map((item, index) => (
              <AccordionItem key={item.question} value={`faq-${index}`}>
                <AccordionTrigger className="text-left text-sm font-medium text-foreground">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-6 text-muted-foreground">
                  {item.answer}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>
      </main>

      <Footer />
    </div>
  );
}
