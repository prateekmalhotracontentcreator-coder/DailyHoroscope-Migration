import React, { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../components/ui/accordion";
import { Footer } from "../../components/Footer";
import { SEO } from "../../components/SEO";
import { fetchAngelNumber } from "./angelNumbersApi";

const SITE = "https://www.everydayhoroscope.in";

function buildSchema(item) {
  if (!item) return null;
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Article",
        headline: item.headline,
        description: item.meta_description,
        url: `${SITE}/angel-numbers/${item.number}`,
        author: { "@type": "Organization", name: "Everyday Horoscope" },
        publisher: { "@type": "Organization", name: "Everyday Horoscope" },
      },
      {
        "@type": "FAQPage",
        mainEntity: item.faq.map((faq) => ({
          "@type": "Question",
          name: faq.q,
          acceptedAnswer: { "@type": "Answer", text: faq.a },
        })),
      },
    ],
  };
}

export function AngelNumberPage() {
  const { number = "" } = useParams();
  const [item, setItem] = useState(null);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    setNotFound(false);
    setItem(null);
    fetchAngelNumber(number, controller.signal)
      .then(setItem)
      .catch((error) => {
        if (error.status === 404) setNotFound(true);
      });
    return () => controller.abort();
  }, [number]);

  const schema = useMemo(() => buildSchema(item), [item]);

  if (notFound) {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#fcfaf5_0%,#f5efe3_55%,#efe7d6_100%)] text-stone-900">
        <SEO title="Angel Number Not Found" description="Browse the angel numbers hub to explore published numbers." url={`${SITE}/angel-numbers`} noindex />
        <main className="mx-auto flex min-h-[70vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Angel Numbers</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-900">Number not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-600">
            This number is outside the current 1,000-number module scope. You can still explore the main hub below.
          </p>
          <Link to="/angel-numbers" className="mt-6 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950">
            View angel numbers hub
          </Link>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.18),transparent_28%),linear-gradient(180deg,#fffaf0_0%,#f6eddc_52%,#efe3cd_100%)] text-stone-900">
      <SEO
        title={item?.meta_title || "Angel Number Meaning"}
        description={item?.meta_description || "Discover the meaning of this angel number."}
        url={`${SITE}/angel-numbers/${number}`}
        schema={schema}
        noindex={notFound}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <nav className="text-sm text-stone-500">
          <Link to="/angel-numbers" className="transition hover:text-gold">
            Angel Numbers
          </Link>
          <span className="mx-2">/</span>
          <span>{item?.number || number}</span>
        </nav>

        <section className="mt-5 rounded-[2rem] border border-gold/20 bg-white/75 p-8 shadow-sm backdrop-blur sm:p-10">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Angel Number Meaning</p>
              <h1 className="mt-4 font-cinzel text-5xl font-semibold leading-none text-stone-900 sm:text-7xl">
                {item?.number || "..."}
              </h1>
              <p className="mt-4 max-w-2xl font-playfair text-2xl italic text-stone-700">
                {item?.tagline || "Loading the message..."}
              </p>
            </div>
            <div className="rounded-[1.5rem] border border-gold/20 bg-gradient-to-br from-white/90 to-gold/10 px-6 py-5 text-right">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Numerology Root</p>
              <p className="mt-2 font-cinzel text-4xl text-stone-900">{item?.numerology_base || "-"}</p>
              <p className="mt-3 max-w-xs text-sm leading-7 text-stone-600">{item?.vibration || ""}</p>
            </div>
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[1.15fr_0.85fr]">
          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold text-stone-900">Seeing it means</h2>
            <p className="mt-4 text-sm leading-8 text-stone-600">{item?.seeing_it_means}</p>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold text-stone-900">Key themes</h2>
            <div className="mt-5 flex flex-wrap gap-3">
              {(item?.key_themes || []).map((theme) => (
                <span key={theme} className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-stone-800">
                  {theme}
                </span>
              ))}
            </div>
          </article>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">
            What to do when you see {item?.number || number}
          </h2>
          <ul className="mt-5 grid gap-4 md:grid-cols-3">
            {(item?.what_to_do || []).map((step) => (
              <li key={step} className="rounded-[1.5rem] border border-gold/15 bg-gold/5 p-4 text-sm leading-7 text-stone-700">
                {step}
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">Explore all 9 intent meanings</h2>
              <p className="mt-2 text-sm text-stone-600">
                These internal links are the main journey deeper into each number.
              </p>
            </div>
            <Link to="/birth-chart" className="text-sm font-semibold text-gold transition hover:opacity-80">
              Discover your personal numbers
            </Link>
          </div>
          <div className="mt-5 grid gap-4 lg:grid-cols-3">
            {(item?.intent_summaries || []).map((intent) => (
              <Link
                key={intent.intent}
                to={`/angel-numbers/${item.number}/${intent.intent}`}
                className="rounded-[1.5rem] border border-gold/15 bg-gradient-to-br from-white to-gold/10 p-4 shadow-sm transition hover:-translate-y-0.5"
              >
                <p className="text-sm font-semibold text-stone-900">{intent.display_name}</p>
                <p className="mt-2 text-sm leading-7 text-stone-600">{intent.teaser}</p>
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Affirmation</p>
            <blockquote className="mt-4 font-playfair text-2xl italic leading-10 text-stone-800">
              {item?.affirmation}
            </blockquote>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <div className="flex items-end justify-between gap-4">
              <div>
                <h2 className="font-playfair text-2xl font-semibold text-stone-900">Related numbers</h2>
                <p className="mt-2 text-sm text-stone-600">Follow the neighboring signals around this message.</p>
              </div>
              <Link to="/angel-numbers" className="text-sm font-semibold text-gold transition hover:opacity-80">
                View hub
              </Link>
            </div>
            <div className="mt-5 flex flex-wrap gap-3">
              {(item?.related_numbers || []).map((related) => (
                <Link
                  key={related}
                  to={`/angel-numbers/${related}`}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                >
                  {related}
                </Link>
              ))}
            </div>
          </article>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">Frequently asked questions</h2>
          <Accordion type="single" collapsible className="mt-4">
            {(item?.faq || []).map((faq) => (
              <AccordionItem key={faq.q} value={faq.q}>
                <AccordionTrigger className="text-left text-base font-semibold text-stone-900">{faq.q}</AccordionTrigger>
                <AccordionContent className="text-sm leading-7 text-stone-600">{faq.a}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default AngelNumberPage;
