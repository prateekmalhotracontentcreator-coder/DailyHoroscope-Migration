import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowRight, LoaderCircle, Sparkles } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/seo/tarot-seo`;
const SITE = 'https://www.everydayhoroscope.in';

const FAQ_ITEMS = [
  {
    question: 'What can I find in the tarot spreads hub?',
    answer: 'This hub gathers source-backed tarot spread explainers, all 78 card meanings, and targeted pages for love, career, money, healing, and other common reading intentions.',
  },
  {
    question: 'Are these pages the same as the live tarot reading tool?',
    answer: 'No. These pages explain layouts, symbolism, and interpretation. The separate /tarot tool is where you actually draw cards and reflect on a live reading.',
  },
  {
    question: 'How do I choose the right tarot spread?',
    answer: 'Choose based on the depth of the question. A one-card draw is good for a daily theme, while multi-card spreads help with timelines, relationships, crossroads, and complex emotional patterns.',
  },
  {
    question: 'Do I need to learn every card before trying a spread?',
    answer: 'No. A simple spread with clear positions is often the fastest way to build confidence because the layout itself tells you what each card is trying to answer.',
  },
];

function buildSchema(data) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'CollectionPage',
        name: data?.meta_title || 'Tarot Spreads Hub',
        description: data?.meta_description || 'Browse tarot spreads, card meanings, and intention guides.',
        url: `${SITE}/tarot/spreads`,
        mainEntity: {
          '@type': 'ItemList',
          itemListElement: (data?.featured_spreads || []).map((spread, index) => ({
            '@type': 'ListItem',
            position: index + 1,
            name: spread.title,
            url: `${SITE}/tarot/spread/${spread.slug}`,
          })),
        },
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
        ],
      },
    ],
  };
}

export function TarotSeoHubPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchHub() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/hub`);
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load the tarot spreads hub right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchHub();
    return () => {
      ignore = true;
    };
  }, []);

  const schema = useMemo(() => buildSchema(data), [data]);
  const majorCards = (data?.cards || []).filter((card) => card.arcana === 'major');
  const minorCards = (data?.cards || []).filter((card) => card.arcana === 'minor');

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.18),transparent_28%),linear-gradient(180deg,#120f0b_0%,#19130d_40%,#221913_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Tarot Spreads Hub'}
        description={data?.meta_description || 'Browse tarot spreads, meanings, and intention guides.'}
        url={`${SITE}/tarot/spreads`}
        schema={schema}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="relative overflow-hidden rounded-[2rem] border border-gold/20 bg-white/[0.05] p-8 shadow-[0_20px_80px_rgba(0,0,0,0.28)] backdrop-blur md:p-10">
          <div className="absolute inset-y-0 right-0 hidden w-1/3 bg-[radial-gradient(circle_at_center,rgba(197,160,89,0.16),transparent_65%)] lg:block" />
          <div className="relative max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
              <Sparkles className="h-3.5 w-3.5" />
              Tarot SEO Library
            </div>
            <h1 className="mt-5 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
              Tarot Spreads, Card Meanings, and Intention Guides
            </h1>
            <p className="mt-5 max-w-2xl text-base leading-8 text-stone-300">
              Explore nearly two hundred tarot learning pages built around practical spread layouts, the full 78-card deck, and focused reading themes like love, career, money, healing, and self-discovery.
            </p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm text-stone-300">
              <span className="rounded-full border border-gold/20 bg-white/[0.04] px-4 py-2">100 spreads</span>
              <span className="rounded-full border border-gold/20 bg-white/[0.04] px-4 py-2">78 card pages</span>
              <span className="rounded-full border border-gold/20 bg-white/[0.04] px-4 py-2">20 intention guides</span>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">How to use this hub</p>
            <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-50">Start with the question, then choose the right tarot doorway.</h2>
            <div className="mt-6 grid gap-4 text-sm leading-7 text-stone-300">
              <p>If you want structure, begin with a spread page and follow the position meanings exactly as laid out.</p>
              <p>If one card keeps showing up in your readings, use the card directory to understand its upright, reversed, and life-area meanings in more detail.</p>
              <p>If your question is highly specific, the intention guides help you pick spreads and recognise supportive or cautionary cards before you shuffle.</p>
            </div>
            <Link
              to="/tarot"
              className="mt-6 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
            >
              Open the live tarot tool
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </article>

          <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Directory snapshot</p>
            <div className="mt-4 space-y-4 text-sm text-stone-300">
              <div className="rounded-2xl border border-gold/15 bg-white/[0.03] p-4">
                <p className="font-semibold text-stone-100">Spread library</p>
                <p className="mt-2 leading-7">One-card pulls, relationship spreads, decision layouts, year-ahead structures, and themed spreads mined from the source tarot textbook.</p>
              </div>
              <div className="rounded-2xl border border-gold/15 bg-white/[0.03] p-4">
                <p className="font-semibold text-stone-100">Card meanings</p>
                <p className="mt-2 leading-7">Major Arcana turning points plus Minor Arcana suit dynamics, with upright, reversed, love, career, and wellbeing angles.</p>
              </div>
              <div className="rounded-2xl border border-gold/15 bg-white/[0.03] p-4">
                <p className="font-semibold text-stone-100">Problem-based reading guides</p>
                <p className="mt-2 leading-7">Fast-start pages for love, money, anxiety, breakups, legal matters, family, travel, manifestation, and spiritual questions.</p>
              </div>
            </div>
          </article>
        </section>

        <section className="mt-8">
          <div className="mb-4 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Featured spreads</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">A strong place to begin if you want guided structure.</h2>
            </div>
            {data?.spreads?.length ? (
              <p className="text-sm text-stone-400">{data.spreads.length} spread pages</p>
            ) : null}
          </div>

          {loading ? (
            <div className="flex items-center justify-center rounded-[2rem] border border-gold/20 bg-white/[0.05] p-10 text-stone-300">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
              Loading tarot spread library...
            </div>
          ) : error ? (
            <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {(data?.featured_spreads || []).map((spread) => (
                <Link
                  key={spread.slug}
                  to={`/tarot/spread/${spread.slug}`}
                  className="group rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6 transition-all hover:-translate-y-1 hover:border-gold/40 hover:bg-white/[0.08]"
                >
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{spread.chapter}</p>
                  <h3 className="mt-3 font-cinzel text-2xl font-semibold leading-tight text-stone-50">{spread.title}</h3>
                  <p className="mt-4 text-sm leading-7 text-stone-300">{spread.purpose}</p>
                  <div className="mt-5 flex items-center justify-between text-sm">
                    <span className="rounded-full border border-gold/20 bg-white/[0.04] px-3 py-1 text-stone-200">{spread.card_count} cards</span>
                    <span className="font-semibold text-gold transition group-hover:text-gold/80">Read spread</span>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </section>

        <section className="mt-10 grid gap-6 lg:grid-cols-2">
          <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Card directory</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">All 78 tarot card pages</h2>
              </div>
              <p className="text-sm text-stone-400">{data?.cards?.length || 0} cards</p>
            </div>

            <div className="mt-6 grid gap-6 md:grid-cols-2">
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.18em] text-stone-200">Major Arcana</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {majorCards.map((card) => (
                    <Link
                      key={card.slug}
                      to={`/tarot/card/${card.slug}`}
                      className="rounded-full border border-gold/20 bg-white/[0.04] px-3 py-2 text-xs font-medium text-stone-200 transition hover:border-gold/40 hover:text-gold"
                    >
                      {card.name}
                    </Link>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.18em] text-stone-200">Minor Arcana</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {minorCards.slice(0, 24).map((card) => (
                    <Link
                      key={card.slug}
                      to={`/tarot/card/${card.slug}`}
                      className="rounded-full border border-gold/20 bg-white/[0.04] px-3 py-2 text-xs font-medium text-stone-200 transition hover:border-gold/40 hover:text-gold"
                    >
                      {card.name}
                    </Link>
                  ))}
                </div>
                <p className="mt-4 text-sm leading-7 text-stone-400">
                  The full Minor Arcana directory is accessible through the individual card URLs and sitemap.
                </p>
              </div>
            </div>
          </article>

          <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Intention guides</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Tarot pages by problem or life area</h2>
              </div>
              <p className="text-sm text-stone-400">{data?.intentions?.length || 0} guides</p>
            </div>
            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              {(data?.intentions || []).map((item) => (
                <Link
                  key={item.slug}
                  to={`/tarot/for/${item.slug}`}
                  className="rounded-[1.25rem] border border-gold/20 bg-white/[0.04] px-4 py-4 text-sm font-medium text-stone-200 transition hover:border-gold/40 hover:bg-white/[0.07] hover:text-gold"
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </article>
        </section>

        <section className="mt-10 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">FAQ</p>
          <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Common questions about this tarot SEO library</h2>
          <Accordion type="single" collapsible className="mt-6 space-y-3">
            {FAQ_ITEMS.map((item, index) => (
              <AccordionItem key={item.question} value={`faq-${index}`} className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5">
                <AccordionTrigger className="text-left text-stone-100">{item.question}</AccordionTrigger>
                <AccordionContent className="pb-5 text-sm leading-7 text-stone-300">
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

export default TarotSeoHubPage;
