import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, LoaderCircle, Sparkles } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/seo/zibu/symbols`;
const SITE = 'https://www.everydayhoroscope.in';

const CATEGORY_STYLES = {
  love: 'border-rose-400/25 bg-rose-500/10 text-rose-200',
  abundance: 'border-amber-400/25 bg-amber-500/10 text-amber-200',
  healing: 'border-emerald-400/25 bg-emerald-500/10 text-emerald-200',
  protection: 'border-sky-400/25 bg-sky-500/10 text-sky-200',
  spiritual: 'border-violet-400/25 bg-violet-500/10 text-violet-200',
  peace: 'border-teal-400/25 bg-teal-500/10 text-teal-200',
  manifestation: 'border-fuchsia-400/25 bg-fuchsia-500/10 text-fuchsia-200',
};

function polarPoint(cx, cy, radius, angleDeg) {
  const angle = (Math.PI / 180) * angleDeg;
  return {
    x: cx + radius * Math.cos(angle),
    y: cy + radius * Math.sin(angle),
  };
}

function buildPlaceholderPaths(symbolNumber) {
  const base = symbolNumber || 1;
  const a1 = (base * 29) % 360;
  const a2 = (base * 47 + 35) % 360;
  const a3 = (base * 61 + 80) % 360;

  const p1 = polarPoint(150, 150, 72, a1);
  const p2 = polarPoint(150, 150, 26, a2);
  const p3 = polarPoint(150, 150, 70, a3);

  const p4 = polarPoint(150, 150, 82, a2 + 120);
  const p5 = polarPoint(150, 150, 20, a3 + 70);
  const p6 = polarPoint(150, 150, 75, a1 + 150);

  const p7 = polarPoint(150, 150, 54, a3 + 24);
  const p8 = polarPoint(150, 150, 12, a1 + 210);
  const p9 = polarPoint(150, 150, 48, a2 + 190);

  return [
    `M ${p1.x} ${p1.y} Q ${p2.x} ${p2.y} ${p3.x} ${p3.y}`,
    `M ${p4.x} ${p4.y} C ${p5.x} ${p5.y}, ${p2.x} ${p2.y}, ${p6.x} ${p6.y}`,
    `M ${p7.x} ${p7.y} Q ${p8.x} ${p8.y} ${p9.x} ${p9.y}`,
  ];
}

function buildSchema(item) {
  if (!item) {
    return null;
  }

  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: item.meta_title,
        description: item.meta_description,
        url: `${SITE}/zibu/${item.slug}`,
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
        mainEntity: (item.faq || []).map((entry) => ({
          '@type': 'Question',
          name: entry.q,
          acceptedAnswer: {
            '@type': 'Answer',
            text: entry.a,
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
            name: 'Zibu Symbols',
            item: `${SITE}/zibu`,
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: item.display_name,
            item: `${SITE}/zibu/${item.slug}`,
          },
        ],
      },
    ],
  };
}

function ZibuPlaceholder({ symbolNumber, label }) {
  const paths = buildPlaceholderPaths(symbolNumber);
  const dots = [
    polarPoint(150, 150, 94, (symbolNumber * 31) % 360),
    polarPoint(150, 150, 92, (symbolNumber * 31 + 142) % 360),
  ];

  return (
    <div className="rounded-[1.75rem] border border-gold/20 bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.2),transparent_55%),rgba(255,255,255,0.04)] p-6">
      <svg viewBox="0 0 300 300" className="mx-auto h-72 w-full max-w-[18rem] text-gold">
        <circle cx="150" cy="150" r="112" fill="none" stroke="rgba(197,160,89,0.7)" strokeWidth="2.5" />
        <circle cx="150" cy="150" r="92" fill="none" stroke="rgba(197,160,89,0.16)" strokeWidth="1.5" />
        {paths.map((path) => (
          <path
            key={path}
            d={path}
            fill="none"
            stroke="currentColor"
            strokeWidth="7"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        ))}
        {dots.map((dot, index) => (
          <circle key={`${dot.x}-${dot.y}-${index}`} cx={dot.x} cy={dot.y} r="4.5" fill="currentColor" opacity="0.82" />
        ))}
      </svg>
      <p className="mt-4 text-center text-xs font-semibold uppercase tracking-[0.24em] text-gold">
        Artistic placeholder only
      </p>
      <p className="mt-3 text-center font-playfair text-lg italic text-stone-100">{label}</p>
      <p className="mt-2 text-center text-sm leading-6 text-stone-300">
        The original Zibu symbol drawing is not reproduced here. This abstract line-art placeholder is an original visual stand-in.
      </p>
    </div>
  );
}

export function ZibuSymbolPage() {
  const { symbolSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchSymbol() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/${symbolSlug}`);
        if (!ignore) {
          setData(response.data);
        }
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Zibu symbol not found.' : 'Unable to load this Zibu symbol right now.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchSymbol();
    return () => {
      ignore = true;
    };
  }, [symbolSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);

  if (!loading && !data && error === 'Zibu symbol not found.') {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#110f0a_0%,#19140e_38%,#221b14_100%)] text-stone-100">
        <SEO
          title="Zibu Symbol Not Found"
          description="Browse the Zibu symbol hub to explore all published symbol pages."
          url={`${SITE}/zibu`}
          noindex
        />
        <main className="mx-auto flex min-h-[72vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Zibu Symbols</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-50">Symbol not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-300">
            This symbol page is not part of the current Zibu library. You can still explore the full published catalog from the hub.
          </p>
          <Link
            to="/zibu"
            className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
          >
            View the Zibu hub
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.18),transparent_28%),linear-gradient(180deg,#110f0a_0%,#19140e_38%,#221b14_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Zibu Symbol'}
        description={data?.meta_description || 'Meaning and guidance for a Zibu symbol.'}
        url={data ? `${SITE}/zibu/${data.slug}` : `${SITE}/zibu`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/zibu" className="transition hover:text-gold">Zibu Symbols</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.intention || 'Symbol'}</span>
        </div>

        <Link
          to="/zibu"
          className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to all Zibu symbols
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-gold/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading Zibu symbol...
          </div>
        ) : error && !data ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">
            {error}
          </div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-8 shadow-[0_20px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${CATEGORY_STYLES[data.category] || 'border-gold/20 bg-gold/10 text-gold'}`}>
                    {data.category_label}
                  </span>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
                    Zibu Symbol for {data.intention} - Meaning and How to Use It
                  </h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">
                    {data.tagline}
                  </p>
                </div>
                <div className="rounded-[1.5rem] border border-gold/20 bg-gold/10 px-5 py-4 text-sm shadow-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Symbol number</p>
                  <p className="mt-2 font-cinzel text-4xl text-stone-50">{data.symbol_number}</p>
                </div>
              </div>
            </section>

            <div className="mt-8 grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
              <section>
                <ZibuPlaceholder symbolNumber={data.symbol_number} label={data.intention} />
              </section>

              <section className="space-y-6">
                <article className="rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6">
                  <div className="flex items-center gap-2 text-gold">
                    <Sparkles className="h-4 w-4" />
                    <p className="text-xs font-semibold uppercase tracking-[0.22em]">Meaning</p>
                  </div>
                  <p className="mt-4 text-sm leading-8 text-stone-300">{data.meaning}</p>
                </article>

                <article className="rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6">
                  <h2 className="font-playfair text-2xl font-semibold text-stone-50">Best for</h2>
                  <div className="mt-4 flex flex-wrap gap-3">
                    {(data.best_for || []).map((item) => (
                      <span key={item} className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm text-stone-100">
                        {item}
                      </span>
                    ))}
                  </div>
                </article>
              </section>
            </div>

            <div className="mt-8 grid gap-8 lg:grid-cols-[1.05fr_0.95fr]">
              <section className="rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6">
                <h2 className="font-playfair text-2xl font-semibold text-stone-50">When to use this symbol</h2>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.when_to_use}</p>

                <h2 className="mt-8 font-playfair text-2xl font-semibold text-stone-50">How to use it step by step</h2>
                <ol className="mt-4 grid gap-4">
                  {(data.how_to_use || []).map((step, index) => (
                    <li key={step} className="flex gap-4 rounded-2xl border border-gold/15 bg-gold/[0.05] p-4">
                      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gold text-sm font-semibold text-stone-950">
                        {index + 1}
                      </span>
                      <span className="text-sm leading-7 text-stone-300">{step}</span>
                    </li>
                  ))}
                </ol>
              </section>

              <section className="space-y-6">
                <article className="rounded-[1.75rem] border border-gold/20 bg-[linear-gradient(160deg,rgba(197,160,89,0.16),rgba(255,255,255,0.04))] p-6">
                  <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Affirmation</p>
                  <blockquote className="mt-4 border-l-2 border-gold pl-4 font-playfair text-2xl italic leading-9 text-stone-50">
                    {data.affirmation}
                  </blockquote>
                </article>

                <article className="rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6">
                  <h2 className="font-playfair text-2xl font-semibold text-stone-50">Chakra and element</h2>
                  <div className="mt-4 flex flex-wrap gap-3">
                    <span className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm text-stone-100">
                      {data.chakra}
                    </span>
                    <span className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm text-stone-100">
                      {data.element}
                    </span>
                  </div>
                </article>
              </section>
            </div>

            <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                  <h2 className="font-playfair text-2xl font-semibold text-stone-50">Complementary symbols</h2>
                  <p className="mt-2 text-sm leading-7 text-stone-300">
                    Explore nearby intentions from the same energetic family.
                  </p>
                </div>
                <Link to="/zibu" className="text-sm font-semibold text-gold transition hover:text-gold/80">
                  View full hub
                </Link>
              </div>

              <div className="mt-5 grid gap-4 md:grid-cols-3">
                {(data.complementary_symbols || []).map((item) => (
                  <Link
                    key={item.slug}
                    to={`/zibu/${item.slug}`}
                    className="rounded-2xl border border-gold/20 bg-gold/[0.05] p-4 transition hover:border-gold/40 hover:bg-gold/[0.08]"
                  >
                    <p className="font-cinzel text-xl font-semibold text-stone-50">{item.intention}</p>
                    <p className="mt-2 text-xs font-semibold uppercase tracking-[0.16em] text-gold">{item.category_label}</p>
                    <p className="mt-3 text-sm leading-7 text-stone-300">{item.tagline}</p>
                  </Link>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/[0.05] p-6">
              <h2 className="font-playfair text-2xl font-semibold text-stone-50">Frequently asked questions</h2>
              <Accordion type="single" collapsible className="mt-4">
                {(data.faq || []).map((entry) => (
                  <AccordionItem key={entry.q} value={entry.q} className="border-gold/15">
                    <AccordionTrigger className="text-left text-base font-semibold text-stone-50">
                      {entry.q}
                    </AccordionTrigger>
                    <AccordionContent className="text-sm leading-7 text-stone-300">
                      {entry.a}
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </section>

            <section className="mt-8 rounded-[2rem] border border-gold/20 bg-[linear-gradient(160deg,rgba(197,160,89,0.18),rgba(255,255,255,0.05))] p-8 text-center">
              <h2 className="font-playfair text-2xl font-semibold text-stone-50">Explore your full Vedic chart</h2>
              <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-stone-300">
                Symbol work can sharpen intention. A full birth chart adds timing, planetary context, and practical guidance about what is unfolding in your life right now.
              </p>
              <Link
                to="/birth-chart"
                className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
              >
                Explore your full Vedic chart
              </Link>
            </section>
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}

export default ZibuSymbolPage;
