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
        url: `${SITE}/lo-shu-grid/personal-year/${data.number}`,
        author: { '@type': 'Organization', name: 'Everyday Horoscope' },
        publisher: { '@type': 'Organization', name: 'Everyday Horoscope' },
      },
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Lo Shu Grid', url: `${SITE}/lo-shu-grid` },
        { name: `Personal Year ${data.number}`, url: `${SITE}/lo-shu-grid/personal-year/${data.number}` },
      ]),
      buildFaqSchema((data.faq || []).map((item) => ({ question: item.question || item.q, answer: item.answer || item.a }))),
    ],
  };
}

export default function LoShuPersonalYearPage() {
  const { n = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    let active = true;

    async function loadPage() {
      setLoading(true);
      setNotFound(false);

      try {
        const response = await axios.get(`${API}/lo-shu/personal-year/${n}`);
        if (active) {
          setData(response.data);
        }
      } catch {
        if (active) {
          setData(null);
          setNotFound(true);
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
  }, [n]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <SEO title="Loading Personal Year Page" description="Loading Lo Shu personal year page." noindex />
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
        <SEO title="Personal Year Page Not Found" description="The requested Lo Shu personal year page could not be found." noindex />
        <main className="mx-auto flex min-h-[70vh] max-w-4xl flex-col items-center justify-center px-4 text-center">
          <h1 className="font-playfair text-4xl font-semibold">Personal year page not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-muted-foreground">
            This Lo Shu personal year page is not available right now. You can still explore the hub or calculate your chart.
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
        url={`${SITE}/lo-shu-grid/personal-year/${data.number}`}
        schema={buildSchema(data)}
      />

      <main className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <nav className="text-sm text-muted-foreground">
          <Link to="/lo-shu-grid" className="transition hover:text-gold">Lo Shu Grid</Link>
          <span className="mx-2">/</span>
          <span>Personal Year {data.number}</span>
        </nav>

        <section className="mt-5 rounded-[2rem] border border-gold/20 bg-card/80 p-8 shadow-sm">
          <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Current cycle · {data.current_year}</p>
              <h1 className="mt-4 font-playfair text-4xl font-semibold leading-tight sm:text-5xl">
                Lo Shu Personal Year {data.number}
              </h1>
              <p className="mt-4 max-w-3xl text-base leading-8 text-muted-foreground">{data.intro}</p>
            </div>
            <div className="rounded-[1.5rem] border border-gold/20 bg-gold/[0.04] px-5 py-4">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Year theme</p>
              <p className="mt-3 text-sm leading-7 text-muted-foreground">{data.year_theme}</p>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-2">
          <article className="rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">Opportunities</h2>
            <div className="mt-5 flex flex-wrap gap-3">
              {(data.opportunities || []).map((item) => (
                <span key={item} className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-medium text-gold">
                  {item}
                </span>
              ))}
            </div>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">Cautions</h2>
            <div className="mt-5 grid gap-3">
              {(data.cautions || []).map((item) => (
                <div key={item} className="rounded-2xl border border-gold/15 bg-background/60 p-4 text-sm leading-7 text-muted-foreground">
                  {item}
                </div>
              ))}
            </div>
          </article>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Monthly flow</h2>
          <p className="mt-4 text-sm leading-7 text-muted-foreground">{data.monthly_note}</p>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Remedies and amplifiers</h2>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            {(data.remedies || []).map((item) => (
              <div key={item} className="rounded-2xl border border-gold/15 bg-background/60 p-4 text-sm leading-7 text-muted-foreground">
                {item}
              </div>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">How to calculate whether you are in Personal Year {data.number}</h2>
          <p className="mt-4 text-sm leading-7 text-muted-foreground">{data.who_is_in_this_year_now}</p>
          <div className="mt-5 rounded-2xl border border-gold/15 bg-gold/[0.04] p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Formula</p>
            <p className="mt-3 text-sm leading-7 text-muted-foreground">{data.calculation_method?.formula}</p>
          </div>
          <div className="mt-5 grid gap-3 md:grid-cols-2">
            {(data.calculation_method?.steps || []).map((item) => (
              <div key={item} className="rounded-2xl border border-gold/15 bg-background/60 p-4 text-sm leading-7 text-muted-foreground">
                {item}
              </div>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-8 text-center shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Calculate your Lo Shu Grid to see your full personal year analysis</h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-muted-foreground">
            Your Personal Year sits inside a bigger grid story. Use the full calculator to check missing numbers, active arrows, and the wider chart pattern behind this cycle.
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
