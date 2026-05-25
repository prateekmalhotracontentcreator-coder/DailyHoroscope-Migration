import React, { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../components/ui/accordion";
import { Footer } from "../../components/Footer";
import { SEO } from "../../components/SEO";
import { fetchAngelIntent } from "./angelNumbersApi";

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
        url: `${SITE}/angel-numbers/${item.number}/${item.intent}`,
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

export function AngelNumberIntentPage() {
  const { number = "", intent = "" } = useParams();
  const [item, setItem] = useState(null);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    setItem(null);
    setNotFound(false);
    fetchAngelIntent(number, intent, controller.signal)
      .then(setItem)
      .catch((error) => {
        if (error.status === 404) setNotFound(true);
      });
    return () => controller.abort();
  }, [number, intent]);

  const schema = useMemo(() => buildSchema(item), [item]);

  if (notFound) {
    return (
      <div className="min-h-screen bg-[linear-gradient(180deg,#fcfaf5_0%,#f5efe3_55%,#efe7d6_100%)] text-stone-900">
        <SEO title="Angel Number Intent Not Found" description="Browse the angel numbers hub to explore published meanings." url={`${SITE}/angel-numbers`} noindex />
        <main className="mx-auto flex min-h-[70vh] max-w-3xl flex-col items-center justify-center px-4 text-center">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Angel Numbers</p>
          <h1 className="mt-4 font-cinzel text-4xl font-semibold text-stone-900">Intent page not found</h1>
          <p className="mt-4 max-w-xl text-sm leading-7 text-stone-600">
            That number or intent is outside the current module scope. Use the hub to continue exploring.
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
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.16),transparent_28%),linear-gradient(180deg,#fffaf0_0%,#f6eddc_52%,#efe3cd_100%)] text-stone-900">
      <SEO
        title={item?.meta_title || "Angel Number Intent Meaning"}
        description={item?.meta_description || "Read the intent-specific meaning of this angel number."}
        url={`${SITE}/angel-numbers/${number}/${intent}`}
        schema={schema}
        noindex={notFound}
      />

      <main className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
        <nav className="text-sm text-stone-500">
          <Link to="/angel-numbers" className="transition hover:text-gold">
            Angel Numbers
          </Link>
          <span className="mx-2">/</span>
          <Link to={`/angel-numbers/${item?.number || number}`} className="transition hover:text-gold">
            {item?.number || number}
          </Link>
          <span className="mx-2">/</span>
          <span>{item?.display_name || intent}</span>
        </nav>

        <section className="mt-5 rounded-[2rem] border border-gold/20 bg-white/75 p-8 shadow-sm backdrop-blur sm:p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Intent Meaning</p>
          <h1 className="mt-4 font-playfair text-4xl font-semibold leading-tight text-stone-900 sm:text-5xl">
            {item?.headline || "Loading..."}
          </h1>
          <p className="mt-5 max-w-3xl text-base leading-8 text-stone-700">{item?.opening}</p>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <h2 className="font-playfair text-2xl font-semibold text-stone-900">The angel's message</h2>
            <p className="mt-4 text-sm leading-8 text-stone-600">{item?.message}</p>
          </article>

          <article className="rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-gold">Affirmation</p>
            <blockquote className="mt-4 font-playfair text-2xl italic leading-10 text-stone-800">
              {item?.affirmation}
            </blockquote>
          </article>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <h2 className="font-playfair text-2xl font-semibold text-stone-900">Action steps</h2>
          <ul className="mt-5 grid gap-4 md:grid-cols-3">
            {(item?.action_steps || []).map((step) => (
              <li key={step} className="rounded-[1.5rem] border border-gold/15 bg-gold/5 p-4 text-sm leading-7 text-stone-700">
                {step}
              </li>
            ))}
          </ul>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">All 9 intents for {item?.number || number}</h2>
              <p className="mt-2 text-sm text-stone-600">The current intent stays highlighted while the other eight remain one tap away.</p>
            </div>
            <Link to={`/angel-numbers/${item?.number || number}`} className="text-sm font-semibold text-gold transition hover:opacity-80">
              Back to core meaning
            </Link>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            {(item?.all_intents || []).map((entry) => {
              const active = entry.slug === item?.intent;
              return (
                <Link
                  key={entry.slug}
                  to={`/angel-numbers/${item?.number || number}/${entry.slug}`}
                  className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                    active
                      ? "border border-gold bg-gold text-stone-950"
                      : "border border-gold/20 bg-gold/10 text-gold hover:bg-gold hover:text-stone-950"
                  }`}
                >
                  {entry.display_name}
                </Link>
              );
            })}
          </div>
        </section>

        <section className="mt-8 rounded-[1.75rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <div className="flex items-end justify-between gap-4">
            <div>
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">Related numbers for this intent</h2>
              <p className="mt-2 text-sm text-stone-600">These sequences often echo or extend the same lesson.</p>
            </div>
            <Link to="/birth-chart" className="text-sm font-semibold text-gold transition hover:opacity-80">
              Get your personal angel number reading
            </Link>
          </div>
          <div className="mt-5 flex flex-wrap gap-3">
            {(item?.related_numbers || []).map((related) => (
              <Link
                key={related}
                to={`/angel-numbers/${related}/${item.intent}`}
                className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
              >
                {related}
              </Link>
            ))}
          </div>
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

export default AngelNumberIntentPage;
