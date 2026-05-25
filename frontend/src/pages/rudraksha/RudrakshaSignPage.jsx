import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowRight, LoaderCircle, Stars } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import {
  API,
  SITE,
  buildBreadcrumbSchema,
  buildFaqSchema,
  buildTopicArticleSchema,
  canonicalTitle,
  normalizeFaqItems,
} from './rudrakshaUtils';

function buildPageSchema(data, canonicalUrl) {
  const faqItems = normalizeFaqItems(data.faq);

  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildTopicArticleSchema({
        headline: data.title,
        description: data.meta_description,
        url: canonicalUrl,
      }),
      buildFaqSchema(faqItems),
      buildBreadcrumbSchema([
        { name: 'Home', item: SITE },
        { name: 'Rudraksha', item: `${SITE}/rudraksha` },
        { name: `Rudraksha for ${data.sign}`, item: canonicalUrl },
      ]),
    ],
  };
}

function MukhiCard({ label, bead, body }) {
  return (
    <div className="rounded-2xl border border-gold/20 bg-white/80 p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{label}</p>
      <h3 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">{bead.name}</h3>
      <p className="mt-3 text-sm leading-7 text-stone-600">{body || bead.fit_reason}</p>
      <Link to={`/rudraksha/${bead.slug}`} className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:gap-3">
        Open bead guide
        <ArrowRight className="h-4 w-4" />
      </Link>
    </div>
  );
}

export function RudrakshaSignPage() {
  const { sign } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchSignPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/sign/${sign}`);
        if (!ignore) {
          setData(response.data || null);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this Rudraksha sign guide right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (sign) {
      fetchSignPage();
    } else {
      setLoading(false);
    }

    return () => {
      ignore = true;
    };
  }, [sign]);

  const canonicalUrl = data ? `${SITE}/rudraksha/for/sign/${data.slug}` : `${SITE}/rudraksha/for/sign/${sign || ''}`;
  const faqItems = useMemo(() => normalizeFaqItems(data?.faq), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(197,160,89,0.16),_transparent_34%),linear-gradient(180deg,#fbf6eb_0%,#fffaf1_100%)] text-stone-900 flex flex-col">
      <SEO
        title={canonicalTitle(data?.meta_title || 'Best Rudraksha for Your Sign')}
        description={data?.meta_description || 'Explore sign-based Rudraksha guidance by ruling planet and temperament.'}
        url={canonicalUrl}
        canonical={canonicalUrl}
        schema={data ? buildPageSchema(data, canonicalUrl) : null}
        noindex={!data && !loading}
      />

      <main className="flex-1 px-4 py-10 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="mb-6 flex items-center gap-2 text-sm text-stone-500">
            <Link to="/" className="transition hover:text-gold">Home</Link>
            <span>/</span>
            <Link to="/rudraksha" className="transition hover:text-gold">Rudraksha</Link>
            <span>/</span>
            <span className="text-stone-800">{data ? data.sign : 'Sign guide'}</span>
          </div>

          {loading ? (
            <div className="flex min-h-[50vh] items-center justify-center">
              <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
            </div>
          ) : error || !data ? (
            <div className="rounded-3xl border border-gold/20 bg-white/80 p-8 text-center shadow-sm">
              <h1 className="font-cinzel text-4xl text-stone-900">Sign guide not found</h1>
              <p className="mt-4 text-sm leading-7 text-stone-600">{error || 'This page is currently unavailable.'}</p>
              <Link to="/rudraksha" className="mt-6 inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90">
                Back to Rudraksha hub
              </Link>
            </div>
          ) : (
            <>
              <section className="rounded-[2rem] border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.16),rgba(255,255,255,0.94)_55%,rgba(252,248,240,0.95))] p-8 shadow-sm sm:p-10">
                <div className="grid gap-8 lg:grid-cols-[1.12fr_0.88fr] lg:items-start">
                  <div>
                    <div className="inline-flex items-center gap-2 rounded-full border border-gold/25 bg-white/70 px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-gold">
                      <Stars className="h-3.5 w-3.5" />
                      Sign Resonance Guide
                    </div>
                    <h1 className="mt-5 font-cinzel text-4xl leading-tight sm:text-5xl">{data.title}</h1>
                    <p className="mt-4 max-w-2xl font-playfair text-lg italic leading-8 text-stone-700">{data.intro}</p>
                    <div className="mt-6 flex flex-wrap gap-3">
                      <span className="rounded-full border border-gold/25 bg-white/80 px-4 py-2 text-sm font-semibold text-stone-800">
                        Ruling planet: {data.ruling_planet}
                      </span>
                      <span className="rounded-full border border-gold/25 bg-white/80 px-4 py-2 text-sm font-semibold text-stone-800">
                        Primary bead: {data.primary_mukhi.name}
                      </span>
                    </div>
                  </div>

                  <div className="rounded-3xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Sign Snapshot</p>
                    <div className="mt-4 space-y-4 text-sm leading-7 text-stone-700">
                      <p><span className="font-semibold text-stone-900">Nature:</span> {data.nature}</p>
                      <p><span className="font-semibold text-stone-900">Best day:</span> {data.wearing_guidance?.best_day}</p>
                      <p><span className="font-semibold text-stone-900">Preferred metal:</span> {data.wearing_guidance?.best_metal}</p>
                      <p><span className="font-semibold text-stone-900">Activation mantra:</span> {data.wearing_guidance?.activation_mantra}</p>
                    </div>
                  </div>
                </div>
              </section>

              <div className="mt-8 grid gap-8 lg:grid-cols-[1.02fr_0.98fr]">
                <section className="space-y-8">
                  <div className="grid gap-4">
                    <MukhiCard label="Primary Match" bead={data.primary_mukhi} />
                    <MukhiCard
                      label="Secondary Support"
                      bead={data.secondary_mukhi}
                      body={`${data.secondary_mukhi.fit_reason} This is often used when ${data.sign} energy needs extra balance around ${data.typical_challenges.slice(0, 2).join(' and ')}.`}
                    />
                  </div>

                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <h2 className="font-playfair text-2xl font-semibold">{data.sign} shadow patterns</h2>
                    <div className="mt-4 flex flex-wrap gap-3">
                      {data.typical_challenges?.map((item) => (
                        <span key={item} className="rounded-full border border-gold/20 bg-gold/[0.06] px-4 py-2 text-sm font-medium text-stone-700">
                          {item}
                        </span>
                      ))}
                    </div>
                  </div>
                </section>

                <section className="space-y-8">
                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <h2 className="font-playfair text-2xl font-semibold">Beads to approach carefully</h2>
                    <div className="mt-4 space-y-4">
                      {data.avoid_mukhis?.map((item) => (
                        <div key={item.slug} className="rounded-2xl border border-amber-200 bg-amber-50/70 p-4">
                          <p className="font-semibold text-stone-900">{item.name}</p>
                          <p className="mt-2 text-sm leading-6 text-stone-700">{item.fit_reason}</p>
                          <Link to={`/rudraksha/${item.slug}`} className="mt-3 inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:gap-3">
                            Open bead guide
                            <ArrowRight className="h-4 w-4" />
                          </Link>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="rounded-2xl border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.14),rgba(255,255,255,0.95))] p-6 shadow-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Chart-Based Next Step</p>
                    <h2 className="mt-2 font-playfair text-2xl font-semibold">Want more than sign-level guidance?</h2>
                    <p className="mt-3 text-sm leading-7 text-stone-700">
                      Sign pages are a helpful shortcut, but your Lagna, Moon sign, Mahadasha, and weak planets can shift the best choice. Use the calculator when you want the recommendation filtered through your actual chart.
                    </p>
                    <Link to="/rudraksha/calculator" className="mt-5 inline-flex items-center gap-2 rounded-full bg-stone-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800">
                      Open Rudraksha calculator
                      <ArrowRight className="h-4 w-4" />
                    </Link>
                  </div>
                </section>
              </div>

              <section className="mt-8 rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold">Frequently asked questions</h2>
                <Accordion type="single" collapsible className="mt-4">
                  {faqItems.map((item) => (
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
            </>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default RudrakshaSignPage;
