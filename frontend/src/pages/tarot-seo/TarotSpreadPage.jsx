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
        '@type': 'HowTo',
        name: data.meta_title,
        description: data.meta_description,
        step: (data.schema_howto_steps || []).map((step, index) => ({
          '@type': 'HowToStep',
          position: index + 1,
          name: step.name,
          text: step.text,
        })),
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
            name: data.title,
            item: `${SITE}/tarot/spread/${data.slug}`,
          },
        ],
      },
    ],
  };
}

export function TarotSpreadPage() {
  const { spreadSlug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchSpread() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/spread/${spreadSlug}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Tarot spread not found.' : 'Unable to load this tarot spread right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchSpread();
    return () => {
      ignore = true;
    };
  }, [spreadSlug]);

  const schema = useMemo(() => buildSchema(data), [data]);

  if (!loading && !data && error === 'Tarot spread not found.') {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#120f0b_0%,#19130d_40%,#221913_100%)] text-stone-100">
        <SEO
          title="Tarot Spread Not Found"
          description="Browse the tarot spreads hub to explore published tarot spread pages."
          url={`${SITE}/tarot/spreads`}
          noindex
        />
        <main className="mx-auto flex min-h-[72vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Tarot Spreads</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-50">Spread not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-300">
            This tarot spread page is not part of the current published library. You can still explore the available layouts from the spreads hub.
          </p>
          <Link
            to="/tarot/spreads"
            className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
          >
            View the tarot spreads hub
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.16),transparent_26%),linear-gradient(180deg,#120f0b_0%,#19130d_40%,#221913_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || 'Tarot Spread'}
        description={data?.meta_description || 'Tarot spread guide.'}
        url={data ? `${SITE}/tarot/spread/${data.slug}` : `${SITE}/tarot/spreads`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/tarot/spreads" className="transition hover:text-gold">Tarot Spreads</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.title || 'Spread'}</span>
        </div>

        <Link
          to="/tarot/spreads"
          className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-gold"
        >
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to tarot spreads
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-gold/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
            Loading tarot spread...
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
                  <div className="inline-flex items-center gap-2 rounded-full border border-gold/30 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                    <Sparkles className="h-3.5 w-3.5" />
                    {data.chapter}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">
                    {data.title} Tarot Spread - How to Do It and What It Reveals
                  </h1>
                  <p className="mt-5 text-base leading-8 text-stone-300">{data.purpose}</p>
                </div>
                <div className="grid gap-3 text-sm text-stone-200 sm:grid-cols-2 lg:grid-cols-1">
                  <div className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5 py-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-gold">Card count</p>
                    <p className="mt-2 font-playfair text-2xl font-semibold text-stone-50">{data.card_count}</p>
                  </div>
                  <div className="rounded-2xl border border-gold/15 bg-white/[0.04] px-5 py-4">
                    <p className="text-xs uppercase tracking-[0.18em] text-gold">Best used for</p>
                    <p className="mt-2 leading-6 text-stone-200">{data.chapter}</p>
                  </div>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Spread diagram</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Card positions and layout meaning</h2>
                <div className="mt-6 grid gap-4">
                  {(data.diagram || []).map((item, index) => (
                    <div key={`${item}-${index}`} className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Position {index + 1}</p>
                      <p className="mt-2 text-sm leading-7 text-stone-300">{item}</p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">How to perform</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">A grounded way to read this layout</h2>
                <ol className="mt-6 grid gap-4">
                  {(data.how_to || []).map((step, index) => (
                    <li key={`${step}-${index}`} className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Step {index + 1}</p>
                      <p className="mt-2 text-sm leading-7 text-stone-300">{step}</p>
                    </li>
                  ))}
                </ol>
              </article>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Sample reading</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Example cards in each position</h2>
                <div className="mt-6 grid gap-4">
                  {(data.sample_reading || []).map((item, index) => (
                    <div key={`${item.position}-${index}`} className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">{item.card}</p>
                      <p className="mt-2 text-sm font-medium text-stone-100">{item.position}</p>
                      <p className="mt-2 text-sm leading-7 text-stone-300">{item.interpretation}</p>
                    </div>
                  ))}
                </div>
              </article>

              <article className="rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">When to use it</p>
                <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Best situations and questions for this spread</h2>
                <div className="mt-6 grid gap-4">
                  {(data.when_to_use || []).map((item, index) => (
                    <div key={`${item}-${index}`} className="rounded-[1.25rem] border border-gold/15 bg-white/[0.04] p-4 text-sm leading-7 text-stone-300">
                      {item}
                    </div>
                  ))}
                </div>
                <Link
                  to="/tarot"
                  className="mt-6 inline-flex items-center rounded-full bg-gold px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
                >
                  Draw cards in the tarot tool
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </article>
            </section>

            <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/[0.05] p-7 backdrop-blur">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">FAQ</p>
              <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Common questions about the {data.title} spread</h2>
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

export default TarotSpreadPage;
