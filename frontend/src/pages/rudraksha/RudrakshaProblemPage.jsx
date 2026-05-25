import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowRight, LoaderCircle, ShieldAlert } from 'lucide-react';
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
        { name: data.problem, item: canonicalUrl },
      ]),
    ],
  };
}

function MukhiCard({ bead, label }) {
  return (
    <article className="rounded-2xl border border-gold/20 bg-white/80 p-5 shadow-sm">
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{label}</p>
      <h3 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">{bead.name}</h3>
      <p className="mt-3 text-sm leading-7 text-stone-600">{bead.fit_reason}</p>
      <Link to={`/rudraksha/${bead.slug}`} className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:gap-3">
        Open bead guide
        <ArrowRight className="h-4 w-4" />
      </Link>
    </article>
  );
}

export function RudrakshaProblemPage() {
  const { problem } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchProblemPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/problem/${problem}`);
        if (!ignore) {
          setData(response.data || null);
        }
      } catch (err) {
        if (!ignore) {
          setError(err?.response?.data?.detail || 'Unable to load this Rudraksha problem guide right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (problem) {
      fetchProblemPage();
    } else {
      setLoading(false);
    }

    return () => {
      ignore = true;
    };
  }, [problem]);

  const canonicalUrl = data ? `${SITE}/rudraksha/for/problem/${data.slug}` : `${SITE}/rudraksha/for/problem/${problem || ''}`;
  const faqItems = useMemo(() => normalizeFaqItems(data?.faq), [data]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(197,160,89,0.18),_transparent_32%),linear-gradient(180deg,#fbf7ed_0%,#fffaf2_100%)] text-stone-900 flex flex-col">
      <SEO
        title={canonicalTitle(data?.meta_title || 'Rudraksha for a Specific Problem')}
        description={data?.meta_description || 'Explore traditional Rudraksha guidance for a specific life challenge.'}
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
            <span className="text-stone-800">{data ? data.problem : 'Problem guide'}</span>
          </div>

          {loading ? (
            <div className="flex min-h-[50vh] items-center justify-center">
              <LoaderCircle className="h-8 w-8 animate-spin text-gold" />
            </div>
          ) : error || !data ? (
            <div className="rounded-3xl border border-gold/20 bg-white/80 p-8 text-center shadow-sm">
              <h1 className="font-cinzel text-4xl text-stone-900">Problem guide not found</h1>
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
                      <ShieldAlert className="h-3.5 w-3.5" />
                      Problem-Area Guide
                    </div>
                    <h1 className="mt-5 font-cinzel text-4xl leading-tight sm:text-5xl">{data.title}</h1>
                    <p className="mt-4 max-w-2xl font-playfair text-lg italic leading-8 text-stone-700">{data.intro}</p>
                  </div>

                  <div className="rounded-3xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Wearing Snapshot</p>
                    <div className="mt-4 space-y-4 text-sm leading-7 text-stone-700">
                      <p><span className="font-semibold text-stone-900">Thread:</span> {data.wearing_method?.thread}</p>
                      <p><span className="font-semibold text-stone-900">Metal:</span> {data.wearing_method?.metal}</p>
                      <p><span className="font-semibold text-stone-900">Mantra:</span> {data.wearing_method?.mantra}</p>
                      <p><span className="font-semibold text-stone-900">Activation:</span> {data.wearing_method?.activation_ritual}</p>
                    </div>
                  </div>
                </div>
              </section>

              <div className="mt-8 grid gap-8 lg:grid-cols-[1.02fr_0.98fr]">
                <section className="space-y-8">
                  <MukhiCard bead={data.primary_mukhi} label="Primary Bead" />

                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <h2 className="font-playfair text-2xl font-semibold">Supporting beads</h2>
                    <div className="mt-4 grid gap-4 sm:grid-cols-2">
                      {data.supporting_mukhis?.map((item) => (
                        <MukhiCard key={item.slug} bead={item} label="Support" />
                      ))}
                    </div>
                  </div>
                </section>

                <section className="space-y-8">
                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <h2 className="font-playfair text-2xl font-semibold">Combination suggestion</h2>
                    <p className="mt-4 text-sm leading-7 text-stone-700">{data.combination_suggestion}</p>
                  </div>

                  <div className="rounded-2xl border border-gold/20 bg-white/80 p-6 shadow-sm">
                    <h2 className="font-playfair text-2xl font-semibold">Lifestyle support around the bead</h2>
                    <ul className="mt-4 space-y-3">
                      {data.lifestyle_tips?.map((item) => (
                        <li key={item} className="rounded-xl border border-gold/12 bg-stone-50/80 px-4 py-3 text-sm leading-6 text-stone-700">
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="rounded-2xl border border-gold/20 bg-[linear-gradient(135deg,rgba(197,160,89,0.14),rgba(255,255,255,0.95))] p-6 shadow-sm">
                    <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Chart-Based Next Step</p>
                    <h2 className="mt-2 font-playfair text-2xl font-semibold">Want a chart-specific remedy angle?</h2>
                    <p className="mt-3 text-sm leading-7 text-stone-700">
                      Problem pages give a thematic public answer. The calculator adds Mahadasha, Lagna, and planetary weakness so the recommendation can reflect your chart rather than only the problem headline.
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

export default RudrakshaProblemPage;
