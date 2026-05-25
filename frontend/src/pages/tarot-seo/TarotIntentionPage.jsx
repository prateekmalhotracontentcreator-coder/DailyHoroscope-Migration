import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, LoaderCircle, Sparkles } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/seo/tarot-seo`;
const SITE = 'https://www.everydayhoroscope.in';

function buildSchema(data) {
  if (!data) return null;

  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: data.meta_title,
        description: data.meta_description,
        url: `${SITE}/tarot/for/${data.slug}`,
        author: {
          '@type': 'Organization',
          name: 'Everyday Horoscope',
        },
        publisher: {
          '@type': 'Organization',
          name: 'Everyday Horoscope',
        },
      },
      {
        '@type': 'FAQPage',
        mainEntity: (data.faq || []).map((item) => ({
          '@type': 'Question',
          name: item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.answer,
          },
        })),
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'Home',
            item: SITE,
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: 'Tarot Spreads',
            item: `${SITE}/tarot/spreads`,
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: data.label,
            item: `${SITE}/tarot/for/${data.slug}`,
          },
        ],
      },
    ],
  };
}

export function TarotIntentionPage() {
  const { intentionSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchIntention() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/for/${intentionSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Tarot intention page not found.' : 'Unable to load this tarot intention guide right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchIntention();
    return () => {
      ignore = true;
    };
  }, [intentionSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);

  if (!loading && !data && error === 'Tarot intention page not found.') {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#120f0b_0%,#19130d_40%,#221913_100%)] text-stone-100">
        <SEO
          title="Tarot Intention Page Not Found"
          description="Browse the tarot spreads hub to explore published tarot intention guides."
          url={`${SITE}/tarot/spreads`}
          noindex
        />
        <main className="mx-auto flex min-h-[72vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Tarot Intentions</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-50">Guide not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-300">
            This problem-based tarot page is not part of the current published library. You can still explore the available guides from the tarot hub.
          </p>
          <Link
            to="/tarot/spreads"
            className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
          >
            View the tarot hub
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.16),transparent_26%),linear-gradient(180deg,#120f0b_0%,#19130d_40%,#221913_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Tarot Intention Guide'}
        description={data?.meta_description || 'Tarot reading guide by intention.'}
        url={data ? `${SITE}/tarot/for/${data.slug}` : `${SITE}/tarot/spreads`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/tarot/spreads" className="transition hover:text-gold">Tarot Spreads</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.label || 'Guide'}</span>
        </div>

        <Link
          to="/tarot/spreads"
          className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to tarot hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-gold/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading tarot guide...
          </div>
        ) : error && !data ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-8 shadow-[0_20px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                    <Sparkles className="h-3.5 w-3.5" />
                    Tarot for {data.label}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
                    Best Tarot Spreads for {data.label} - Top Layouts Explained
                  </h1>
                  <p className="mt-5 text-base leading-8 text-stone-300">{data.intro}</p>
                </div>
                <div className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5 py-4 text-sm text-stone-200">
                  <p className="text-xs uppercase tracking-[0.18em] text-gold">Top spreads</p>
                  <p className="mt-2 font-playfair text-2xl font-semibold text-stone-50">{data.top_spreads?.length || 0}</p>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Top tarot spreads</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">The strongest layouts for {data.label.toLowerCase()}</h2>
              <div className="mt-6 grid gap-5 lg:grid-cols-3">
                {(data.top_spreads || []).map((spread) => (
                  <article key={spread.slug} className="rounded-[1.5rem] border border-gold/15 bg-white/[0.04] p-5">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">{spread.chapter}</p>
                    <h3 className="mt-3 font-cinzel text-2xl font-semibold text-stone-50">{spread.title}</h3>
                    <p className="mt-3 text-sm leading-7 text-stone-300">{spread.purpose}</p>
                    <div className="mt-4 space-y-2">
                      {(spread.positions || []).slice(0, 3).map((position, index) => (
                        <p key={`${position}-${index}`} className="text-sm leading-7 text-stone-300">
                          {position}
                        </p>
                      ))}
                    </div>
                    <Link
                      to={`/tarot/spread/${spread.slug}`}
                      className="mt-5 inline-flex items-center text-sm font-semibold text-gold transition hover:text-gold/80"
                    >
                      Read full spread
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </article>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-2">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Best cards to see</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Supportive cards in a {data.label.toLowerCase()} reading</h2>
                <div className="mt-6 grid gap-4">
                  {(data.best_cards || []).map((card) => (
                    <Link
                      key={card.slug}
                      to={`/tarot/card/${card.slug}`}
                      className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4 transition hover:border-gold/40 hover:bg-white/[0.07]"
                    >
                      <p className="font-semibold text-stone-100">{card.name}</p>
                      <p className="mt-2 text-sm leading-7 text-stone-300">{card.meaning}</p>
                    </Link>
                  ))}
                </div>
              </article>

              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Cards that signal caution</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Challenging themes to read with extra honesty</h2>
                <div className="mt-6 grid gap-4">
                  {(data.caution_cards || []).map((card) => (
                    <Link
                      key={card.slug}
                      to={`/tarot/card/${card.slug}`}
                      className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4 transition hover:border-gold/40 hover:bg-white/[0.07]"
                    >
                      <p className="font-semibold text-stone-100">{card.name}</p>
                      <p className="mt-2 text-sm leading-7 text-stone-300">{card.meaning}</p>
                    </Link>
                  ))}
                </div>
              </article>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Sample walkthrough</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">One example reading path</h2>
                <div className="mt-6 space-y-4">
                  {(data.sample_walkthrough || []).map((step, index) => (
                    <div key={`${step}-${index}`} className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4 text-sm leading-7 text-stone-300">
                      {step}
                    </div>
                  ))}
                </div>
              </article>

              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Next step</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Use the live tarot tool when you are ready to draw.</h2>
                <p className="mt-5 text-sm leading-8 text-stone-300">
                  These SEO pages help you choose the right layout and notice the right card themes. Once you know what kind of reading you want, move into the interactive tarot tool to shuffle, draw, and reflect in real time.
                </p>
                <Link
                  to="/tarot"
                  className="mt-6 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
                >
                  Open the live tarot tool
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </article>
            </section>

            <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">FAQ</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Common questions about tarot for {data.label.toLowerCase()}</h2>
              <Accordion type="single" collapsible className="mt-6 space-y-3">
                {(data.faq || []).map((item, index) => (
                  <AccordionItem key={item.question} value={`faq-${index}`} className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5">
                    <AccordionTrigger className="text-left text-stone-100">{item.question}</AccordionTrigger>
                    <AccordionContent className="pb-5 text-sm leading-7 text-stone-300">{item.answer}</AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </section>
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}

export default TarotIntentionPage;
