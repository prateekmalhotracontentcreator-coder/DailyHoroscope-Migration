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
        url: `${SITE}/lo-shu-grid/for/${data.slug}`,
        author: { '@type': 'Organization', name: 'Everyday Horoscope' },
        publisher: { '@type': 'Organization', name: 'Everyday Horoscope' },
      },
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Lo Shu Grid', url: `${SITE}/lo-shu-grid` },
        { name: data.problem_name, url: `${SITE}/lo-shu-grid/for/${data.slug}` },
      ]),
      buildFaqSchema((data.faq || []).map((item) => ({ question: item.question || item.q, answer: item.answer || item.a }))),
    ],
  };
}

export default function LoShuProblemPage() {
  const { problem = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    let active = true;

    async function loadPage() {
      setLoading(true);
      setNotFound(false);

      try {
        const response = await axios.get(`${API}/lo-shu/problem/${problem}`);
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
  }, [problem]);

  if (loading) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <SEO title="Loading Lo Shu Problem Page" description="Loading Lo Shu problem-area page." noindex />
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
        <SEO title="Lo Shu Problem Page Not Found" description="The requested Lo Shu problem page could not be found." noindex />
        <main className="mx-auto flex min-h-[70vh] max-w-4xl flex-col items-center justify-center px-4 text-center">
          <h1 className="font-playfair text-4xl font-semibold">Problem page not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-muted-foreground">
            This Lo Shu remedy page is not available right now. You can still explore the hub or calculate your chart.
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
        url={`${SITE}/lo-shu-grid/for/${data.slug}`}
        schema={buildSchema(data)}
      />

      <main className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <nav className="text-sm text-muted-foreground">
          <Link to="/lo-shu-grid" className="transition hover:text-gold">Lo Shu Grid</Link>
          <span className="mx-2">/</span>
          <span>{data.problem_name}</span>
        </nav>

        <section className="mt-5 rounded-[2rem] border border-gold/20 bg-card/80 p-8 shadow-sm">
          <h1 className="font-playfair text-4xl font-semibold leading-tight sm:text-5xl">
            Lo Shu Grid for {data.problem_name}
          </h1>
          <p className="mt-4 max-w-3xl text-base leading-8 text-muted-foreground">{data.intro}</p>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-2">
          <article className="rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">Grid diagnostic</h2>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">{data.grid_diagnostic}</p>
            <div className="mt-5">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Missing numbers to inspect</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {(data.diagnostic_missing_numbers || []).map((value) => (
                  <Link
                    key={value}
                    to={`/lo-shu-grid/missing-${value}`}
                    className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-primary-foreground"
                  >
                    Missing {value}
                  </Link>
                ))}
              </div>
            </div>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold">Overrepresented numbers</h2>
            <p className="mt-4 text-sm leading-7 text-muted-foreground">
              These are the numbers most likely to intensify the pattern when they become excessive or poorly balanced.
            </p>
            <div className="mt-5 flex flex-wrap gap-2">
              {(data.diagnostic_overrepresented_numbers || []).map((value) => (
                <span key={value} className="rounded-full border border-border bg-background/70 px-4 py-2 text-sm font-semibold text-muted-foreground">
                  Number {value}
                </span>
              ))}
            </div>
          </article>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-gradient-to-br from-gold/10 to-card/80 p-8 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Start here</p>
          <h2 className="mt-3 font-playfair text-3xl font-semibold">Address missing number {data.primary_fix_number} first</h2>
          <p className="mt-4 max-w-3xl text-sm leading-7 text-muted-foreground">{data.missing_number_fix}</p>
          <Link
            to={data.primary_fix_page?.href || `/lo-shu-grid/missing-${data.primary_fix_number}`}
            className="mt-6 inline-flex items-center gap-2 rounded-full border border-gold/20 bg-card/80 px-5 py-3 text-sm font-semibold text-gold transition hover:border-gold/40"
          >
            Read Missing {data.primary_fix_number}
            <ArrowRight className="h-4 w-4" />
          </Link>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Arrow patterns to watch</h2>
          <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {(data.arrow_patterns || []).map((item) => (
              <Link
                key={item.slug}
                to={item.href}
                className="rounded-[1.5rem] border border-gold/15 bg-gold/[0.04] p-5 transition hover:-translate-y-0.5 hover:border-gold/30 hover:shadow-sm"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{item.theme}</p>
                <h3 className="mt-3 font-playfair text-xl font-semibold">{item.name}</h3>
                <p className="mt-3 text-sm text-muted-foreground">{(item.numbers || []).join(' - ')}</p>
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Remedies</h2>
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            {(data.remedies || []).map((item) => (
              <div key={item} className="rounded-2xl border border-gold/15 bg-background/60 p-4 text-sm leading-7 text-muted-foreground">
                {item}
              </div>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-8 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Affirmation</p>
          <blockquote className="mt-4 font-playfair text-2xl italic leading-relaxed text-foreground">
            "{data.affirmation}"
          </blockquote>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-card/75 p-8 text-center shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold">Want to check whether this pattern shows up in your own chart?</h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-7 text-muted-foreground">
            Use the calculator to see your missing numbers, active arrows, and the combinations that shape this life area.
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
