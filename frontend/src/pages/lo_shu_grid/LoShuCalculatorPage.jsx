import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Loader2, Sparkles } from 'lucide-react';
import { GRID_CELL_DETAILS } from './loShuContent';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import LoShuGridBoard from '../../components/lo-shu/LoShuGridBoard';
import { buildBreadcrumbSchema, buildFaqSchema, CALCULATOR_FAQ_ITEMS, SITE } from './loShuContent';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

const INITIAL_FORM = {
  full_name: '',
  dob: '',
  gender: 'male',
};

function buildSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        name: 'Lo Shu Grid Calculator - Your Personal Numerology Birth Chart',
        url: `${SITE}/lo-shu-grid/calculator`,
        description: 'Calculate your Lo Shu Grid using your birth date and name. See missing numbers, active arrows, Rajayoga patterns, and numerology insights.',
      },
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Lo Shu Grid', url: `${SITE}/lo-shu-grid` },
        { name: 'Calculator', url: `${SITE}/lo-shu-grid/calculator` },
      ]),
      buildFaqSchema(CALCULATOR_FAQ_ITEMS),
    ],
  };
}

function toSectionId(type, value) {
  return `${type}-${value}`;
}

export default function LoShuCalculatorPage() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API}/lo-shu/calculate`, form);
      setResult(response.data);
      requestAnimationFrame(() => {
        document.getElementById('results-panel')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    } catch (requestError) {
      setError(requestError.response?.data?.detail || 'Could not calculate your Lo Shu Grid right now.');
    } finally {
      setLoading(false);
    }
  };

  const handleCellClick = (number, present) => {
    if (!result) return;
    let targetId = 'number-summary';
    if (!present) {
      targetId = toSectionId('missing-number', number);
    } else {
      const activeArrow = (result.active_arrows || []).find((arrow) => arrow.numbers.includes(number));
      if (activeArrow) {
        targetId = toSectionId('active-arrow', activeArrow.slug);
      }
    }
    document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.16),transparent_28%),linear-gradient(180deg,hsl(var(--background))_0%,rgba(197,160,89,0.03)_100%)] text-foreground">
      <SEO
        title="Lo Shu Grid Calculator - Your Personal Numerology Birth Chart"
        description="Calculate your Lo Shu Grid birth chart with your full name and date of birth. Discover missing numbers, active arrows, and Rajayoga patterns."
        url={`${SITE}/lo-shu-grid/calculator`}
        schema={buildSchema()}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="grid gap-8 lg:grid-cols-[0.94fr_1.06fr] lg:items-start">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
              <Sparkles className="h-3.5 w-3.5" />
              Personal Chart
            </div>
            <h1 className="mt-6 font-playfair text-4xl font-semibold leading-tight sm:text-5xl">
              Lo Shu Grid Calculator - Your Personal Numerology Birth Chart
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-8 text-muted-foreground">
              Enter your full name, date of birth, and gender to generate your Lo Shu Grid, detect active arrows, and highlight the missing numbers that need more conscious balance.
            </p>
            <div className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">What you will get</p>
              <ul className="mt-4 space-y-3 text-sm text-muted-foreground">
                {[
                  'A visual 3x3 Lo Shu chart with present and missing cells.',
                  'Basic, Destiny, Kua, and Name numbers in one strip.',
                  'Active arrows, missing arrows, and Rajayoga detection.',
                  'Missing-number guidance with direct links to full detail pages.',
                ].map((item) => (
                  <li key={item} className="flex gap-3">
                    <CheckCircle2 className="mt-0.5 h-4 w-4 flex-shrink-0 text-gold" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="rounded-[2rem] border border-gold/20 bg-card/80 p-8 shadow-sm backdrop-blur">
            <div className="grid gap-6">
              <label className="grid gap-2">
                <span className="text-sm font-semibold text-foreground">Full name</span>
                <input
                  name="full_name"
                  value={form.full_name}
                  onChange={handleChange}
                  placeholder="Enter your full name"
                  className="rounded-2xl border border-gold/15 bg-background/70 px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold/40"
                  required
                />
              </label>

              <label className="grid gap-2">
                <span className="text-sm font-semibold text-foreground">Date of birth</span>
                <input
                  type="date"
                  name="dob"
                  value={form.dob}
                  onChange={handleChange}
                  className="rounded-2xl border border-gold/15 bg-background/70 px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold/40"
                  required
                />
              </label>

              <label className="grid gap-2">
                <span className="text-sm font-semibold text-foreground">Gender</span>
                <select
                  name="gender"
                  value={form.gender}
                  onChange={handleChange}
                  className="rounded-2xl border border-gold/15 bg-background/70 px-4 py-3 text-sm text-foreground outline-none transition focus:border-gold/40"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
              </label>

              <button
                type="submit"
                disabled={loading}
                className="inline-flex items-center justify-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-primary-foreground transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-70"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                Generate My Grid
              </button>

              {error ? (
                <p className="rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                  {error}
                </p>
              ) : null}
            </div>
          </form>
        </section>

        {result ? (
          <section id="results-panel" className="mt-12 space-y-8">
            {result.rajayoga_level !== 'none' ? (
              <div className="rounded-[1.75rem] border border-emerald-400/20 bg-emerald-500/10 p-6 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-emerald-300">Rajayoga Present</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-foreground">
                  {result.rajayoga_level === 'dual' ? 'Both Rajayoga diagonals are active.' : 'One Rajayoga diagonal is active.'}
                </h2>
                <p className="mt-3 text-sm leading-7 text-muted-foreground">
                  {result.rajayoga_level === 'dual'
                    ? 'Your grid carries both highlighted diagonals from the decoded Lo Shu source, suggesting unusually strong determination and emotional composure when your effort stays consistent.'
                    : 'Your grid includes one of the highlighted Rajayoga diagonals, suggesting a stronger success pattern in the area represented by that line.'}
                </p>
              </div>
            ) : null}

            <div className="grid gap-8 lg:grid-cols-[1.25fr_0.75fr]">
              <div className="rounded-[2rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Your visual grid</h2>
                <p className="mt-3 text-sm leading-7 text-muted-foreground">
                  Tap any cell to jump toward the most relevant interpretation section below.
                </p>
                <LoShuGridBoard
                  counts={result.number_counts}
                  interactive
                  onCellClick={handleCellClick}
                  className="mt-6"
                />
              </div>

              <div id="number-summary" className="rounded-[2rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Calculated numbers</h2>
                <div className="mt-6 grid gap-3">
                  {[
                    ['Basic Number', result.basic_number],
                    ['Destiny Number', result.destiny_number],
                    ['Kua Number', result.kua_number],
                    ['Name Number', result.name_number],
                  ].map(([label, value]) => {
                    const cell = GRID_CELL_DETAILS[value] || {};
                    return (
                      <div key={label} className="rounded-[1.5rem] border border-gold/15 bg-gold/[0.04] p-4">
                        <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{label}</p>
                        <div className="mt-2 flex items-baseline gap-3">
                          <p className="font-playfair text-4xl font-semibold text-foreground">{value}</p>
                          {cell.label && (
                            <p className="text-sm font-semibold text-foreground">{cell.label}</p>
                          )}
                        </div>
                        {cell.note && (
                          <p className="mt-1 text-xs leading-5 text-muted-foreground">{cell.note}</p>
                        )}
                      </div>
                    );
                  })}
                </div>

                <div className="mt-6 flex flex-wrap gap-2">
                  <span className="rounded-full border border-gold/20 bg-gold/10 px-3 py-1.5 text-xs font-semibold text-gold">
                    Present: {result.present_numbers.join(', ') || 'None'}
                  </span>
                  <span className="rounded-full border border-border bg-background/70 px-3 py-1.5 text-xs font-semibold text-muted-foreground">
                    Missing: {result.missing_numbers.join(', ') || 'None'}
                  </span>
                </div>
              </div>
            </div>

            <div className="rounded-[2rem] border border-gold/30 bg-gradient-to-br from-gold/10 via-card/80 to-card/75 p-8 shadow-md">
              <div className="flex flex-wrap items-center gap-3">
                <h2 className="font-playfair text-4xl font-semibold">Active Arrows</h2>
                {(result.active_arrows || []).length > 0 && (
                  <span className="rounded-full border border-gold/30 bg-gold/15 px-4 py-1.5 text-sm font-semibold text-gold">
                    {result.active_arrows.length} active
                  </span>
                )}
              </div>
              <p className="mt-3 max-w-3xl text-sm leading-7 text-muted-foreground">
                Arrows are complete lines across your grid. Each one concentrates three numbers into a single amplified theme and often shapes the strongest patterns in how you think, feel, and act.
              </p>
              <div className="mt-6 grid gap-5">
                {(result.active_arrows || []).length > 0 ? result.active_arrows.map((arrow) => (
                  <article
                    key={arrow.slug}
                    id={toSectionId('active-arrow', arrow.slug)}
                    className="rounded-[1.75rem] border border-gold/25 bg-gold/[0.06] p-6 shadow-sm"
                  >
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-gold/20 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-gold">
                        {arrow.theme}
                      </span>
                      {arrow.rajayoga ? (
                        <span className="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-300">
                          Rajayoga
                        </span>
                      ) : null}
                    </div>
                    <div className="mt-4 flex flex-wrap items-baseline gap-4">
                      <h3 className="font-playfair text-3xl font-semibold">{arrow.name}</h3>
                      <p className="text-base font-semibold text-gold">{arrow.numbers.join(' · ')}</p>
                    </div>
                    <p className="mt-4 max-w-4xl text-base leading-8 text-muted-foreground">{arrow.effect_summary}</p>
                    <Link
                      to={`/lo-shu-grid/arrow/${arrow.slug}`}
                      className="mt-5 inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/10 px-5 py-2.5 text-sm font-semibold text-gold transition hover:bg-gold/20"
                    >
                      Full arrow detail
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </article>
                )) : (
                  <p className="text-sm text-muted-foreground">
                    No full arrows are active in this chart. Missing numbers may be carrying the stronger story here.
                  </p>
                )}
              </div>
            </div>

            <div className="rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
              <h2 className="font-playfair text-3xl font-semibold">Missing numbers</h2>
              <div className="mt-6 grid gap-4 md:grid-cols-2">
                {(result.missing_number_details || []).map((item) => (
                  <article
                    key={item.number}
                    id={toSectionId('missing-number', item.number)}
                    className="rounded-[1.5rem] border border-gold/15 bg-background/60 p-5"
                  >
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="rounded-full border border-gold/20 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-gold">
                        Missing {item.number}
                      </span>
                      <span className="rounded-full border border-border bg-card/60 px-3 py-1 text-xs font-semibold text-muted-foreground">
                        {item.ruling_planet} · {item.ruling_day}
                      </span>
                    </div>
                    <h3 className="mt-4 font-playfair text-2xl font-semibold">Number {item.number}</h3>
                    <p className="mt-4 text-sm leading-7 text-muted-foreground">{item.effect_summary}</p>
                    <p className="mt-4 text-sm text-foreground">
                      Remedy highlight: <span className="text-muted-foreground">{item.remedies?.[0]}</span>
                    </p>
                    <Link
                      to={`/lo-shu-grid/missing-${item.number}`}
                      className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:opacity-80"
                    >
                      Learn more
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </article>
                ))}
              </div>
            </div>

            {(result.missing_arrows || []).length > 0 ? (
              <div className="rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
                <h2 className="font-playfair text-3xl font-semibold">Missing arrows</h2>
                <div className="mt-6 grid gap-4 md:grid-cols-2">
                  {result.missing_arrows.map((arrow) => (
                    <article key={arrow.slug} className="rounded-[1.5rem] border border-gold/15 bg-background/60 p-5">
                      <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{arrow.theme}</p>
                      <h3 className="mt-3 font-playfair text-2xl font-semibold">{arrow.name}</h3>
                      <p className="mt-2 text-sm font-medium text-gold">{arrow.numbers.join(' - ')}</p>
                      <p className="mt-4 text-sm leading-7 text-muted-foreground">{arrow.effect_summary}</p>
                    </article>
                  ))}
                </div>
              </div>
            ) : null}
          </section>
        ) : null}

        <section className="mt-12 rounded-[2rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
          <h2 className="font-playfair text-3xl font-semibold">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-5">
            {CALCULATOR_FAQ_ITEMS.map((item, index) => (
              <AccordionItem key={item.question} value={`faq-${index}`} className="border-gold/10">
                <AccordionTrigger className="text-left font-semibold text-foreground hover:no-underline">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-7 text-muted-foreground">
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
