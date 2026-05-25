import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowRight, LoaderCircle } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import {
  ACTIVATION_STEPS,
  API,
  SITE,
  buildArticleSchema,
  buildBreadcrumbSchema,
  buildFaqSchema,
  canonicalTitle,
} from './rudrakshaUtils';

function buildPageSchema(mukhi) {
  const faqItems = (mukhi.faq || []).map((item) => ({
    question: item.q,
    answer: item.a,
  }));

  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema(mukhi),
      buildFaqSchema(faqItems),
      buildBreadcrumbSchema([
        { name: 'Home', item: SITE },
        { name: 'Rudraksha', item: `${SITE}/rudraksha` },
        { name: mukhi.name, item: `${SITE}/rudraksha/${mukhi.slug}` },
      ]),
    ],
  };
}

function badgeLabel(value) {
  return String(value || '').replace(/\s+\/\s+/g, ' / ');
}

export function RudrakshaMukhiPage() {
  const { mukhi: mukhiSlug } = useParams();
  const [mukhi, setMukhi] = useState(null);
  const [mukhis, setMukhis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const mukhiNumber = useMemo(() => {
    const match = String(mukhiSlug || '').match(/^(\d+)-mukhi$/);
    return match ? Number(match[1]) : null;
  }, [mukhiSlug]);

  useEffect(() => {
    let ignore = false;

    async function fetchPageData() {
      if (!mukhiNumber) {
        setError('This Rudraksha page could not be found.');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError('');
        const [detailResponse, listResponse] = await Promise.all([
          axios.get(`${API}/mukhi/${mukhiNumber}`),
          axios.get(`${API}/mukhis`),
        ]);
        if (!ignore) {
          setMukhi(detailResponse.data || null);
          setMukhis(listResponse.data || []);
        }
      } catch {
        if (!ignore) setError('Unable to load this Rudraksha guide right now.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPageData();
    return () => {
      ignore = true;
    };
  }, [mukhiNumber]);

  const related = useMemo(() => {
    if (!mukhi) return [];
    const relatedNumbers = new Set(mukhi.related_mukhis || []);
    const byPlanet = mukhis.filter((item) => item.ruling_planet === mukhi.ruling_planet && item.mukhi !== mukhi.mukhi);
    const manual = mukhis.filter((item) => relatedNumbers.has(item.mukhi));
    const merged = [...manual, ...byPlanet]
      .filter((item, index, array) => array.findIndex((entry) => entry.mukhi === item.mukhi) === index)
      .slice(0, 3);
    return merged;
  }, [mukhi, mukhis]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#faf5ea_0%,#fffaf2_100%)] flex items-center justify-center">
        <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
      </div>
    );
  }

  if (error || !mukhi) {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#faf5ea_0%,#fffaf2_100%)] flex flex-col">
        <main className="flex-1 px-4 py-16 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-3xl rounded-3xl border border-gold/20 bg-white/80 p-8 text-center shadow-sm">
            <h1 className="font-cinzel text-4xl text-stone-900">Rudraksha page not found</h1>
            <p className="mt-4 text-sm leading-7 text-stone-600">{error || 'This page is currently unavailable.'}</p>
            <Link to="/rudraksha" className="mt-6 inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90">
              Back to Rudraksha hub
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  const instructions = mukhi.wearing_instructions || {};
  const faqItems = mukhi.faq || [];

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_right,_rgba(197,160,89,0.18),_transparent_34%),linear-gradient(180deg,#fbf6ea_0%,#fffaf1_100%)] text-stone-900 flex flex-col">
      <SEO
        title={canonicalTitle(mukhi.meta_title)}
        description={mukhi.meta_description}
        url={`${SITE}/rudraksha/${mukhi.slug}`}
        schema={buildPageSchema(mukhi)}
      />

      <main className="flex-1 px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-6 flex items-center gap-2 text-sm text-stone-500">
            <Link to="/" className="transition hover:text-gold">Home</Link>
            <span>/</span>
            <Link to="/rudraksha" className="transition hover:text-gold">Rudraksha</Link>
            <span>/</span>
            <span className="text-stone-800">{mukhi.name}</span>
          </div>

          <section className="rounded-[2rem] border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.16),rgba(255,255,255,0.94)_55%,rgba(252,248,240,0.95))] p-8 shadow-sm sm:p-10">
            <div className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr] lg:items-start">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Mukhi Detail Guide</p>
                <h1 className="mt-4 font-cinzel text-4xl leading-tight sm:text-5xl">
                  {mukhi.mukhi} Mukhi Rudraksha - Benefits, Who Should Wear &amp; Mantra
                </h1>
                <p className="mt-4 max-w-2xl font-playfair text-lg italic leading-8 text-stone-700">
                  {mukhi.overview}
                </p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <span className="rounded-full border border-gold/25 bg-white/80 px-4 py-2 text-sm font-semibold text-stone-800">
                    Ruling Planet: {badgeLabel(mukhi.ruling_planet)}
                  </span>
                  <span className="rounded-full border border-gold/25 bg-white/80 px-4 py-2 text-sm font-semibold text-stone-800">
                    Ruling Deity: {mukhi.ruling_deity}
                  </span>
                </div>
              </div>

              <div className="rounded-3xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Rarity &amp; Price Band</p>
                <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-1">
                  <div className="rounded-2xl border border-gold/15 bg-stone-50/90 p-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Rarity</p>
                    <p className="mt-2 font-playfair text-xl font-semibold text-stone-900">{mukhi.rarity}</p>
                  </div>
                  <div className="rounded-2xl border border-gold/15 bg-stone-50/90 p-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-stone-500">Price Band</p>
                    <p className="mt-2 font-playfair text-xl font-semibold text-stone-900">{mukhi.price_range}</p>
                  </div>
                </div>
                <p className="mt-4 text-sm leading-6 text-stone-600">
                  Rare beads are often approached with more care and are usually selected for a specific purpose instead of casual experimentation.
                </p>
              </div>
            </div>
          </section>

          <div className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
            <section className="space-y-8">
              <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Benefits</h2>
                <ul className="mt-4 space-y-3">
                  {mukhi.benefits.map((benefit) => (
                    <li key={benefit} className="rounded-xl border border-gold/12 bg-stone-50/80 px-4 py-3 text-sm leading-6 text-stone-700">
                      {benefit}
                    </li>
                  ))}
                </ul>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Best for</h2>
                <div className="mt-4 flex flex-wrap gap-3">
                  {mukhi.best_for.map((item) => (
                    <span key={item} className="rounded-full border border-gold/20 bg-gold/[0.06] px-4 py-2 text-sm font-medium text-stone-700">
                      {item}
                    </span>
                  ))}
                </div>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Cautions</h2>
                <ul className="mt-4 space-y-3">
                  {mukhi.cautions.map((item) => (
                    <li key={item} className="rounded-xl border border-amber-200 bg-amber-50/70 px-4 py-3 text-sm leading-6 text-stone-700">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="space-y-8">
              <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Wearing instructions</h2>
                <div className="mt-5 overflow-hidden rounded-2xl border border-gold/15">
                  <div className="grid grid-cols-[0.9fr_1.1fr] border-b border-gold/10 bg-gold/[0.06] px-4 py-3 text-sm font-semibold text-stone-800">
                    <span>Guidance</span>
                    <span>Details</span>
                  </div>
                  {[
                    ['Day', instructions.day],
                    ['Metal', instructions.metal],
                    ['Mantra', instructions.mantra],
                    ['How to wear', instructions.how_to_wear],
                  ].map(([label, value]) => (
                    <div key={label} className="grid grid-cols-[0.9fr_1.1fr] border-b border-gold/10 px-4 py-3 text-sm text-stone-700 last:border-b-0">
                      <span className="font-medium text-stone-800">{label}</span>
                      <span>{value}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Activation guide</h2>
                <div className="mt-5 space-y-3">
                  {ACTIVATION_STEPS.map((step, index) => (
                    <div key={step.title} className="rounded-2xl border border-gold/12 bg-stone-50/80 p-4">
                      <p className="font-cinzel text-sm text-gold">{String(index + 1).padStart(2, '0')}</p>
                      <h3 className="mt-2 font-semibold text-stone-900">{step.title}</h3>
                      <p className="mt-2 text-sm leading-6 text-stone-600">{step.body}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </div>

          <section className="mt-8 rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">Frequently asked questions</h2>
            <Accordion type="single" collapsible className="mt-4">
              {faqItems.map((item) => (
                <AccordionItem key={item.q} value={item.q}>
                  <AccordionTrigger className="text-left text-base font-semibold text-stone-900">
                    {item.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-sm leading-7 text-stone-600">
                    {item.a}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </section>

          {related.length > 0 && (
            <section className="mt-8 rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Related Paths</p>
                  <h2 className="mt-2 font-playfair text-2xl font-semibold">Related mukhis</h2>
                </div>
                <Link to="/rudraksha/calculator" className="text-sm font-semibold text-gold transition hover:underline">
                  Find your ideal Rudraksha
                </Link>
              </div>
              <div className="mt-5 grid gap-4 md:grid-cols-3">
                {related.map((item) => (
                  <article key={item.mukhi} className="rounded-2xl border border-gold/15 bg-stone-50/80 p-5">
                    <p className="font-cinzel text-3xl text-stone-900">{item.mukhi}</p>
                    <p className="mt-2 font-semibold text-stone-900">{item.name}</p>
                    <p className="mt-3 text-sm leading-6 text-stone-600">{item.overview}</p>
                    <Link to={`/rudraksha/${item.slug}`} className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-gold">
                      Learn More
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </article>
                ))}
              </div>
            </section>
          )}

          <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.18),rgba(255,248,238,0.95))] p-7 shadow-sm">
            <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Calculator CTA</p>
                <h2 className="mt-2 font-playfair text-3xl font-semibold">Find your ideal Rudraksha</h2>
                <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-700">
                  If you want a chart-based suggestion instead of choosing only by description, use the calculator to map your birth details to a practical starting bead.
                </p>
              </div>
              <Link to="/rudraksha/calculator" className="inline-flex items-center justify-center gap-2 rounded-full bg-stone-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800">
                Open calculator
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </section>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default RudrakshaMukhiPage;
