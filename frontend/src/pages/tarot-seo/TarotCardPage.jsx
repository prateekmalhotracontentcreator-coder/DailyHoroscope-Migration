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

function titleCase(value) {
  return String(value || '')
    .split('-')
    .map((item) => item.charAt(0).toUpperCase() + item.slice(1))
    .join(' ');
}

function buildSchema(data) {
  if (!data) return null;

  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: data.meta_title,
        description: data.meta_description,
        url: `${SITE}/tarot/card/${data.slug}`,
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
            name: data.name,
            item: `${SITE}/tarot/card/${data.slug}`,
          },
        ],
      },
    ],
  };
}

export function TarotCardPage() {
  const { cardSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchCard() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/card/${cardSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Tarot card not found.' : 'Unable to load this tarot card right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchCard();
    return () => {
      ignore = true;
    };
  }, [cardSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);
  const suitLabel = data?.suit ? titleCase(data.suit) : 'Major Arcana';

  if (!loading && !data && error === 'Tarot card not found.') {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#120f0b_0%,#19130d_40%,#221913_100%)] text-stone-100">
        <SEO
          title="Tarot Card Not Found"
          description="Browse the tarot spreads hub to explore published tarot card meaning pages."
          url={`${SITE}/tarot/spreads`}
          noindex
        />
        <main className="mx-auto flex min-h-[72vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Tarot Cards</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-50">Card not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-300">
            This tarot card meaning page is not part of the current published library. You can still explore the available tarot guides from the hub.
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
        title={data?.meta_title || 'Tarot Card Meaning'}
        description={data?.meta_description || 'Tarot card meaning guide.'}
        url={data ? `${SITE}/tarot/card/${data.slug}` : `${SITE}/tarot/spreads`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/tarot/spreads" className="transition hover:text-gold">Tarot Spreads</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.name || 'Card'}</span>
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
            Loading tarot card...
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
                    {suitLabel}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
                    {data.name} Tarot Card - Meaning, Reversed and How to Read It
                  </h1>
                </div>
                <div className="grid gap-3 text-sm text-stone-200 sm:grid-cols-2 lg:grid-cols-1">
                  <div className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5 py-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-gold">Arcana</p>
                    <p className="mt-2 font-playfair text-2xl font-semibold text-stone-50">{titleCase(data.arcana)}</p>
                  </div>
                  <div className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5 py-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-gold">Imaging key</p>
                    <p className="mt-2 leading-6 text-stone-200">{data.imagery}</p>
                  </div>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-2">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Upright meaning</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">What this card says when it lands openly</h2>
                <p className="mt-5 text-sm leading-8 text-stone-300">{data.upright}</p>
              </article>

              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Reversed meaning</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">What changes when the energy turns inward or sideways</h2>
                <p className="mt-5 text-sm leading-8 text-stone-300">{data.reversed}</p>
              </article>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-3">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Love readings</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.love}</p>
              </article>
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Career readings</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.career}</p>
              </article>
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Health readings</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.health}</p>
              </article>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Symbols and imagery</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Why the visual language matters</h2>
                <p className="mt-5 text-sm leading-8 text-stone-300">{data.imagery}</p>
              </article>

              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Best spreads for this card</p>
                <div className="mt-5 grid gap-3">
                  {(data.best_spreads || []).map((spread) => (
                    <Link
                      key={spread.slug}
                      to={`/tarot/spread/${spread.slug}`}
                      className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4 transition hover:border-gold/40 hover:bg-white/[0.07]"
                    >
                      <p className="font-semibold text-stone-100">{spread.title}</p>
                      <p className="mt-2 text-sm text-gold">View spread guide</p>
                    </Link>
                  ))}
                </div>
                <Link
                  to="/tarot"
                  className="mt-6 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
                >
                  Use the live tarot tool
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </article>
            </section>

            <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">FAQ</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Common questions about {data.name}</h2>
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

export default TarotCardPage;
