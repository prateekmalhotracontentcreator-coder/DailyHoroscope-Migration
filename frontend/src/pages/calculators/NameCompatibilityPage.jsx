import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import { Copy, HeartHandshake, LoaderCircle, RotateCcw, Sparkles } from 'lucide-react';
import { toast } from 'sonner';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;
const SITE = 'https://www.everydayhoroscope.in';

const BAND_STYLES = {
  high: {
    label: 'High Compatibility',
    className: 'border-emerald-400/30 bg-emerald-500/15 text-emerald-300',
  },
  good: {
    label: 'Good Compatibility',
    className: 'border-sky-400/30 bg-sky-500/15 text-sky-300',
  },
  moderate: {
    label: 'Moderate Compatibility',
    className: 'border-amber-400/30 bg-amber-500/15 text-amber-300',
  },
  challenging: {
    label: 'Challenging Compatibility',
    className: 'border-red-400/30 bg-red-500/15 text-red-300',
  },
};

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebApplication',
        name: 'Name Compatibility Calculator',
        applicationCategory: 'AstrologyApplication',
        operatingSystem: 'All',
        url: `${SITE}/compatibility/name`,
        description: 'Find out how compatible two names are using Chaldean numerology.',
        creator: {
          '@type': 'Organization',
          name: 'EverydayHoroscope',
        },
      },
      {
        '@type': 'FAQPage',
        mainEntity: [
          {
            '@type': 'Question',
            name: 'How is name compatibility calculated?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'This calculator uses Chaldean numerology to reduce each name into a core number and then compares the pair using a fixed compatibility matrix.',
            },
          },
          {
            '@type': 'Question',
            name: 'Is name compatibility accurate?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'It is best used as a symbolic guidance tool. A high score suggests smoother energetic resonance, while mixed scores show where more conscious effort may be needed.',
            },
          },
          {
            '@type': 'Question',
            name: 'What does a high compatibility score mean?',
            acceptedAnswer: {
              '@type': 'Answer',
              text: 'A high score suggests the two name vibrations support each other naturally, often making attraction, communication, and emotional rhythm feel easier.',
            },
          },
        ],
      },
    ],
  };
}

function normalizeName(value) {
  return value.replace(/\s+/g, ' ').trim();
}

export function NameCompatibilityPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [form, setForm] = useState({
    name1: searchParams.get('n1') || '',
    name2: searchParams.get('n2') || '',
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const shareUrl = useMemo(() => {
    const params = new URLSearchParams();
    if (result?.name1) params.set('n1', result.name1);
    if (result?.name2) params.set('n2', result.name2);
    const query = params.toString();
    return `${SITE}/compatibility/name${query ? `?${query}` : ''}`;
  }, [result?.name1, result?.name2]);

  useEffect(() => {
    const q1 = normalizeName(searchParams.get('n1') || '');
    const q2 = normalizeName(searchParams.get('n2') || '');
    if (!q1 || !q2) return;

    setForm((current) => {
      if (current.name1 === q1 && current.name2 === q2) return current;
      return { name1: q1, name2: q2 };
    });
  }, [searchParams]);

  useEffect(() => {
    const q1 = normalizeName(searchParams.get('n1') || '');
    const q2 = normalizeName(searchParams.get('n2') || '');
    if (!q1 || !q2) return;
    if (result?.name1 === q1 && result?.name2 === q2) return;

    void runCalculation(q1, q2, false);
  }, [result?.name1, result?.name2, searchParams]);

  async function runCalculation(rawName1, rawName2, syncParams = true) {
    const name1 = normalizeName(rawName1);
    const name2 = normalizeName(rawName2);

    if (!name1 || !name2) {
      setError('Both names are required.');
      setResult(null);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API}/numerology/name-compatibility`, { name1, name2 });
      setResult(response.data);
      if (syncParams) {
        setSearchParams({ n1: response.data.name1, n2: response.data.name2 });
      }
    } catch (err) {
      setResult(null);
      setError(err?.response?.data?.detail || 'Unable to calculate name compatibility right now.');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();
    await runCalculation(form.name1, form.name2, true);
  }

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(shareUrl);
      toast.success('Result link copied');
    } catch {
      toast.error('Could not copy the result link');
    }
  }

  function handleReset() {
    setForm({ name1: '', name2: '' });
    setResult(null);
    setError('');
    setSearchParams({});
  }

  const bandMeta = result?.band ? BAND_STYLES[result.band] : null;

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title="Name Compatibility Calculator - Chaldean Numerology"
        description="Find out how compatible two names are using Chaldean numerology. Enter any two names to get your compatibility score, number analysis, and relationship insight."
        url={`${SITE}/compatibility/name`}
        schema={buildSchema()}
      />

      <main className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="max-w-3xl space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
              <HeartHandshake className="h-3.5 w-3.5" />
              Chaldean Numerology
            </div>
            <div>
              <h1 className="text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                Name Compatibility Calculator
              </h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                Discover your numerological connection through the Chaldean name vibration system. Enter any two names to reveal compatibility score, harmony band, and relationship insight.
              </p>
            </div>
          </div>
        </section>

        <div className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <div className="border-b border-gold/10 pb-4">
              <h2 className="text-xl font-semibold text-foreground">Enter two names</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                This fast calculator uses Chaldean name numbers only, with no LLM and no birth data required.
              </p>
            </div>

            <form className="mt-6 space-y-5" onSubmit={handleSubmit}>
              <label className="block">
                <span className="text-sm font-medium text-foreground">Name 1</span>
                <input
                  type="text"
                  value={form.name1}
                  onChange={(event) => setForm((current) => ({ ...current, name1: event.target.value }))}
                  placeholder="Your name"
                  className="mt-2 w-full rounded-lg border border-gold/30 bg-gold/[0.02] px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
              </label>

              <label className="block">
                <span className="text-sm font-medium text-foreground">Name 2</span>
                <input
                  type="text"
                  value={form.name2}
                  onChange={(event) => setForm((current) => ({ ...current, name2: event.target.value }))}
                  placeholder="Their name"
                  className="mt-2 w-full rounded-lg border border-gold/30 bg-gold/[0.02] px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold"
                />
              </label>

              <div className="flex flex-wrap gap-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex items-center justify-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? <LoaderCircle className="h-4 w-4 animate-spin" /> : 'Calculate Compatibility'}
                </button>

                <button
                  type="button"
                  onClick={handleReset}
                  className="inline-flex items-center gap-2 rounded-full border border-gold px-5 py-3 text-sm font-semibold text-gold transition hover:bg-gold/10"
                >
                  <RotateCcw className="h-4 w-4" />
                  Try different names
                </button>
              </div>
            </form>
          </section>

          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <div className="border-b border-gold/10 pb-4">
              <h2 className="text-xl font-semibold text-foreground">Your compatibility result</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Shareable result links are generated automatically from the two names.
              </p>
            </div>

            {loading && (
              <div className="flex min-h-80 flex-col items-center justify-center gap-3 text-center">
                <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
                <p className="text-sm text-muted-foreground">Calculating your Chaldean compatibility...</p>
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
                  Enter two names to reveal the compatibility score, harmony band, and relationship reading.
                </p>
              </div>
            )}

            {!loading && !error && result && (
              <div className="mt-6 space-y-5">
                <div className="rounded-2xl border border-gold/20 bg-gradient-to-br from-gold/15 to-gold/5 p-5 text-center">
                  <p className="text-sm text-muted-foreground">{result.name1} = {result.number1} · {result.name2} = {result.number2}</p>
                  <p className="mt-4 text-5xl font-cinzel text-gold">{result.score}%</p>
                  <p className="mt-2 text-sm font-semibold text-foreground">Compatible</p>
                  {bandMeta && (
                    <div className={`mt-4 inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${bandMeta.className}`}>
                      {bandMeta.label}
                    </div>
                  )}
                </div>

                <div className="rounded-xl border border-gold/20 bg-background/70 p-5">
                  <p className="text-sm leading-7 text-muted-foreground">{result.summary}</p>
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    type="button"
                    onClick={handleCopy}
                    className="inline-flex items-center gap-2 rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10"
                  >
                    <Copy className="h-4 w-4" />
                    Share this result
                  </button>
                  <p className="self-center text-xs text-muted-foreground">{shareUrl}</p>
                </div>
              </div>
            )}
          </section>
        </div>

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_1fr]">
          <section className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">What is Chaldean numerology?</h2>
            <p className="mt-3 text-sm leading-7 text-muted-foreground">
              Chaldean numerology is one of the oldest name-vibration systems, assigning values to letters based on sound resonance rather than alphabetical order.
            </p>
            <p className="mt-3 text-sm leading-7 text-muted-foreground">
              In compatibility work, each name is reduced to a core vibration and then compared through a harmony matrix that estimates ease, tension, and energetic fit between two people.
            </p>
          </section>

          <section className="rounded-xl border border-gold/20 bg-gold/[0.05] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">Go deeper with a full numerology report</h2>
            <p className="mt-3 text-sm leading-7 text-muted-foreground">
              A full relationship numerology reading adds Life Path compatibility, Soul Urge resonance, communication patterns, and timing support beyond just name vibration.
            </p>
            <Link to="/numerology" className="mt-5 inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90">
              Unlock Relationship Report
            </Link>
          </section>
        </div>

        <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-4">
            <AccordionItem value="faq-1" className="border-gold/10">
              <AccordionTrigger className="text-left font-semibold text-foreground hover:no-underline">
                How is name compatibility calculated?
              </AccordionTrigger>
              <AccordionContent className="text-sm leading-7 text-muted-foreground">
                This calculator reduces each name to a Chaldean core number and then compares the pair against a fixed harmony matrix to estimate the relationship tone.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="faq-2" className="border-gold/10">
              <AccordionTrigger className="text-left font-semibold text-foreground hover:no-underline">
                Is name compatibility accurate?
              </AccordionTrigger>
              <AccordionContent className="text-sm leading-7 text-muted-foreground">
                It is best used as symbolic guidance. A strong score suggests easier energetic fit, while mixed scores highlight where patience and communication matter more.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="faq-3" className="border-gold/10">
              <AccordionTrigger className="text-left font-semibold text-foreground hover:no-underline">
                What does a high compatibility score mean?
              </AccordionTrigger>
              <AccordionContent className="text-sm leading-7 text-muted-foreground">
                A high score suggests the two name vibrations support each other naturally, often making attraction, responsiveness, and communication flow more smoothly.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </section>

        <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-foreground">Related tools</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            <Link to="/rashi-calculator" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Rashi Calculator ->
            </Link>
            <Link to="/nakshatra-calculator" className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
              Nakshatra Calculator ->
            </Link>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
