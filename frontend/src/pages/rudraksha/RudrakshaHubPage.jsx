import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowRight, LoaderCircle, Sparkles, Stars } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import {
  ACTIVATION_STEPS,
  API,
  HUB_FAQ,
  SITE,
  buildBreadcrumbSchema,
  buildFaqSchema,
} from './rudrakshaUtils';

function buildHubSchema() {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildFaqSchema(HUB_FAQ),
      buildBreadcrumbSchema([
        { name: 'Home', item: SITE },
        { name: 'Rudraksha', item: `${SITE}/rudraksha` },
      ]),
    ],
  };
}

export function RudrakshaHubPage() {
  const [mukhis, setMukhis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchMukhis() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/mukhis`);
        if (!ignore) {
          setMukhis(response.data || []);
        }
      } catch {
        if (!ignore) setError('Unable to load the Rudraksha guide right now.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchMukhis();
    return () => {
      ignore = true;
    };
  }, []);

  const spotlight = useMemo(() => mukhis.slice(0, 3), [mukhis]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.18),_transparent_38%),linear-gradient(180deg,#fbf7ef_0%,#f7f1e5_36%,#fffaf1_100%)] text-stone-900 flex flex-col">
      <SEO
        title="Rudraksha - All 21 Mukhis, Benefits & Calculator"
        description="Explore all 21 Rudraksha mukhis - ruling planets, benefits, and wearing instructions. Use our Vedic calculator to find which Rudraksha suits your birth chart."
        url={`${SITE}/rudraksha`}
        schema={buildHubSchema()}
      />

      <main className="flex-1 px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <section className="overflow-hidden rounded-[2rem] border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.18),rgba(255,248,232,0.9)_55%,rgba(255,255,255,0.95))] p-8 shadow-sm sm:p-10">
            <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
              <div>
                <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-white/70 px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
                  <Sparkles className="h-3.5 w-3.5" />
                  Sacred Bead Hub
                </div>
                <h1 className="mt-5 max-w-3xl font-cinzel text-4xl font-semibold leading-tight sm:text-5xl">
                  Rudraksha - Sacred Beads for Healing, Protection &amp; Vedic Guidance
                </h1>
                <p className="mt-5 max-w-2xl font-playfair text-lg italic leading-8 text-stone-700">
                  Rudraksha beads are traditionally worn as spiritual companions: some for steadiness, some for courage, some for protection, and some for deeper inner work. Each mukhi carries its own symbolic current, and this guide gathers all 21 in one place so you can explore them calmly before choosing what fits your path.
                </p>
                <div className="mt-7 flex flex-wrap gap-3">
                  <Link to="/rudraksha/calculator" className="inline-flex items-center gap-2 rounded-full bg-gold px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90">
                    Find Your Rudraksha
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                  <a href="#mukhi-grid" className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-white/70 px-5 py-3 text-sm font-semibold text-stone-800 transition hover:bg-white">
                    Browse all 21 mukhis
                  </a>
                </div>
              </div>

              <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
                {spotlight.map((item) => (
                  <div key={item.mukhi} className="rounded-2xl border border-gold/20 bg-white/70 p-5 shadow-sm backdrop-blur">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{item.ruling_planet}</p>
                    <p className="mt-3 font-cinzel text-3xl text-stone-900">{item.mukhi}</p>
                    <p className="text-sm font-semibold text-stone-800">{item.name}</p>
                    <p className="mt-3 text-sm leading-6 text-stone-600">{item.overview}</p>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section id="mukhi-grid" className="mt-10">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Explore The Beads</p>
                <h2 className="mt-2 font-playfair text-3xl font-semibold">All 21 Rudraksha mukhis</h2>
              </div>
              <p className="max-w-xl text-sm leading-6 text-stone-600">
                Each card shows the ruling planet, a short benefit summary, and a path to the full page with mantra, cautions, and wearing guidance.
              </p>
            </div>

            {loading && (
              <div className="flex min-h-72 items-center justify-center">
                <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
              </div>
            )}

            {!loading && error && (
              <div className="mt-6 rounded-2xl border border-red-400/30 bg-red-50 p-5 text-sm text-red-700">
                {error}
              </div>
            )}

            {!loading && !error && (
              <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                {mukhis.map((item) => (
                  <article key={item.mukhi} className="group rounded-2xl border border-gold/20 bg-white/75 p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-gold/35 hover:shadow-md">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{item.ruling_planet}</p>
                        <h3 className="mt-3 font-cinzel text-4xl leading-none text-stone-900">{item.mukhi}</h3>
                      </div>
                      <span className="rounded-full border border-gold/25 bg-gold/[0.08] px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide text-stone-700">
                        {item.rarity}
                      </span>
                    </div>
                    <p className="mt-4 font-playfair text-lg font-semibold text-stone-800">{item.name}</p>
                    <p className="mt-3 text-sm leading-6 text-stone-600">{item.overview}</p>
                    <div className="mt-5 flex flex-wrap gap-2">
                      {item.benefits.slice(0, 3).map((benefit) => (
                        <span key={benefit} className="rounded-full border border-stone-200 bg-stone-50 px-3 py-1 text-xs font-medium text-stone-600">
                          {benefit}
                        </span>
                      ))}
                    </div>
                    <Link to={`/rudraksha/${item.slug}`} className="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-gold transition group-hover:gap-3">
                      Learn More
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </article>
                ))}
              </div>
            )}
          </section>

          <section className="mt-10 rounded-[1.75rem] border border-gold/25 bg-[linear-gradient(135deg,rgba(197,160,89,0.22),rgba(255,250,241,0.95))] p-7 shadow-sm">
            <div className="grid gap-6 lg:grid-cols-[1fr_0.9fr] lg:items-center">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Chart-Based Suggestion</p>
                <h2 className="mt-2 font-playfair text-3xl font-semibold">Find Your Rudraksha</h2>
                <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-700">
                  Enter your birth details and the calculator will look at Lagna, Moon sign, Mahadasha, and chart pressure points before suggesting a practical starting bead.
                </p>
              </div>
              <div className="rounded-2xl border border-gold/20 bg-white/80 p-5 shadow-sm">
                <p className="text-sm leading-6 text-stone-600">
                  Good for first-time seekers who want a birth-chart-based direction instead of choosing only by curiosity or popularity.
                </p>
                <Link to="/rudraksha/calculator" className="mt-5 inline-flex items-center gap-2 rounded-full bg-stone-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800">
                  Open Rudraksha Calculator
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>
          </section>

          <section className="mt-10 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
            <div className="rounded-2xl border border-gold/20 bg-white/75 p-6 shadow-sm">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                <Stars className="h-3.5 w-3.5" />
                How To Wear
              </div>
              <h2 className="mt-4 font-playfair text-2xl font-semibold">A simple 4-step wearing flow</h2>
              <div className="mt-6 space-y-4">
                {ACTIVATION_STEPS.map((step, index) => (
                  <div key={step.title} className="rounded-2xl border border-gold/15 bg-stone-50/80 p-4">
                    <p className="font-cinzel text-sm text-gold">{String(index + 1).padStart(2, '0')}</p>
                    <h3 className="mt-2 font-playfair text-lg font-semibold text-stone-900">{step.title}</h3>
                    <p className="mt-2 text-sm leading-6 text-stone-600">{step.body}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-2xl border border-gold/20 bg-white/75 p-6 shadow-sm">
              <h2 className="font-playfair text-2xl font-semibold">Frequently asked questions</h2>
              <Accordion type="single" collapsible className="mt-4">
                {HUB_FAQ.map((item) => (
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
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default RudrakshaHubPage;
