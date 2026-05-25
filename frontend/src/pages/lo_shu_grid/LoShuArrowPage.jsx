import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowRight, Loader2 } from 'lucide-react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { buildBreadcrumbSchema, buildFaqSchema, SITE } from './loShuContent';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

function buildSchema(data) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: data.title,
        description: data.meta_description,
        url: `${SITE}/lo-shu-grid/arrow/${data.slug}`,
        author: { '@type': 'Organization', name: 'Everyday Horoscope' },
        publisher: { '@type': 'Organization', name: 'Everyday Horoscope' },
      },
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Lo Shu Grid', url: `${SITE}/lo-shu-grid` },
        { name: data.name, url: `${SITE}/lo-shu-grid/arrow/${data.slug}` },
      ]),
      buildFaqSchema((data.faq || []).map((item) => ({ question: item.question || item.q, answer: item.answer || item.a }))),
    ],
  };
}

export default function LoShuArrowPage() {
  const { slug = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    let active = true;

    async function loadPage() {
      setLoading(true);
      setNotFound(false);

      try {
        const response = await axios.get(`${API}/lo-shu/arrow/${slug}`);
        if (active) {
          setData(response.data);
        }
      } catch {
        if (active) {
          setNotFound(true);
          setData(null);
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    loadPage();
    return () => {
      active = false;
    };
  }, [slug]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <SEO title="Loading Arrow Page" description="Loading Lo Shu arrow detail page." noindex />
        <main className="mx-auto flex min-h-[70vh] max-w-4xl items-center justify-center px-4">
          <Loader2 className="h-8 w-8 animate-spin text-gold" />
        </main>
        <Footer />
      </div>
    );
  }

  if (notFound || !data) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <SEO title="Arrow Page Not Found" description="The requested Lo Shu arrow page could not be found." noindex />
        <main className="mx-auto flex min-h-[70vh] max-w-4xl flex-col items-center justify-center px-4 text-center">
          <h1 className="font-playfair text-4xl font-semibold">Arrow page not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-muted-foreground">
            This Lo Shu arrow detail page is not available. You can return to the hub or calculate your chart directly.
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Link to="/lo-shu-grid" className="rounded-full border border-gold/20 bg-card px-5 py-3 text-sm font-semibold text-foreground">
              Back to hub
            </Link>
            <Link to="/lo-shu-grid/calculator" className="rounded-full bg-gold px-5 py-3 text-sm font-semibold text-primary-foreground">
              Open calculator
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  const faqItems = (data.faq || []).map((item) => ({ question: item.question || item.q, answer: item.answer || item.a }));

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.16),transparent_28%),linear-gradient(180deg,hsl(var(--background))_0%,rgba(197,160,89,0.03)_100%)] text-foreground">
      <SEO
        title={data.meta_title || data.title}
        description={data.meta_description}
        url={`${SITE}/lo-shu-grid/arrow/${data.slug}`}
        schema={buildSchema(data)}
      />

      <main className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <nav className="text-sm text-muted-foreground">
          <Link to="/lo-shu-grid" className="transition hover:text-gold">Lo Shu Grid</Link>
          <span className="mx-2">/</span>
          <span>{data.name}</span>
        </nav>

        <section className="mt-5 rounded-[2rem] border border-gold/20 bg-card/80 p-8 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">{data.theme}</p>
              <h1 className="mt-4 font-playfair text-4xl font-semibold leading-tight sm:text-5xl">
                {data.name}
              </h1>
              <p className="mt-4 max-w-3xl text-base leading-8 text-muted-foreground">{data.effect_present}</p>
            </div>
            <div className="rounded-[1.5rem] border border-gold/20 bg-gold/[0.04] px-5 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Numbers</p>
              <p className="mt-3 text-lg font-semibold text-foreground">{data.numbers.join(' - ')}</p>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
          <article className="rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">When this arrow is present</h2>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">{data.effect_present}</p>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">When this arrow is missing</h2>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">{data.effect_missing}</p>
          </article>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="font-playfair text-2xl font-semibold">Real-life traits</h2>
            {data.rajayoga ? (
              <span className="rounded-full border border-emerald-400/20 bg-emerald-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-emerald-300">
                Rajayoga
              </span>
            ) : null}
          </div>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {(data.real_life_traits || []).map((item) => (
              <div key={item} className="rounded-2xl border border-gold/15 bg-gold/[0.04] px-4 py-3 text-sm text-muted-foreground">
                {item}
              </div>
            ))}
          </div>
          <div className="mt-6 rounded-2xl border border-gold/15 bg-background/60 p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Shadow side</p>
            <p className="mt-3 text-sm leading-7 text-muted-foreground">{data.shadow_trait}</p>
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-8 text-center shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Want to see whether this arrow is active in your own chart?</h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-muted-foreground">
            Use the calculator to build your grid and check whether this arrow appears naturally in your birth pattern.
          </p>
          <Link
            to="/lo-shu-grid/calculator"
            className="mt-6 inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-sm font-semibold text-primary-foreground transition hover:opacity-90"
          >
            Open calculator
            <ArrowRight className="h-4 w-4" />
          </Link>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-4">
            {faqItems.map((item, index) => (
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
