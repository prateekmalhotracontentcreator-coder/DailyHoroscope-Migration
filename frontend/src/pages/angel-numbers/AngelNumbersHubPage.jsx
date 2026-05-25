import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../../components/ui/accordion";
import { Footer } from "../../components/Footer";
import { SEO } from "../../components/SEO";
import { fetchAngelHub, normaliseAngelSearchInput } from "./angelNumbersApi";

const SITE = "https://www.everydayhoroscope.in";

function buildSchema(data) {
  if (!data) return null;
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Home", item: SITE },
          { "@type": "ListItem", position: 2, name: "Angel Numbers", item: `${SITE}/angel-numbers` },
        ],
      },
      {
        "@type": "FAQPage",
        mainEntity: data.faq.map((item) => ({
          "@type": "Question",
          name: item.q,
          acceptedAnswer: { "@type": "Answer", text: item.a },
        })),
      },
    ],
  };
}

export function AngelNumbersHubPage() {
  const navigate = useNavigate();
  const [hub, setHub] = useState(null);
  const [searchValue, setSearchValue] = useState("");
  const [searchError, setSearchError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    fetchAngelHub(controller.signal)
      .then(setHub)
      .catch(() => {});
    return () => controller.abort();
  }, []);

  const schema = useMemo(() => buildSchema(hub), [hub]);

  const onSearch = (event) => {
    event.preventDefault();
    const number = normaliseAngelSearchInput(searchValue);
    if (!number) {
      setSearchError("Enter a valid angel number from 1 to 10000.");
      return;
    }
    setSearchError("");
    navigate(`/angel-numbers/${number}`);
  };

  const families = hub?.numerology_families || [];
  const intentCards = hub?.intent_categories || [];

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(197,160,89,0.18),transparent_28%),linear-gradient(180deg,#fffaf0_0%,#f6eddc_52%,#efe3cd_100%)] text-stone-900">
      <SEO
        title="Angel Numbers - All 1,000 Meanings, Sequences & Messages | EverydayHoroscope"
        description="Discover the meaning of every angel number from 1 to 9999. Explore messages for love, career, twin flame, manifestation, and spiritual growth."
        url={`${SITE}/angel-numbers`}
        schema={schema}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="overflow-hidden rounded-[2rem] border border-gold/20 bg-white/75 p-8 shadow-sm backdrop-blur sm:p-10">
          <div className="grid gap-8 lg:grid-cols-[1.15fr_0.85fr]">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Angel Numbers SEO Hub</p>
              <h1 className="mt-4 font-cinzel text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">
                Angel Numbers - Meanings, Messages & What They Mean for You
              </h1>
              <p className="mt-5 max-w-3xl text-sm leading-8 text-stone-600">
                {hub?.intro ||
                  "Angel numbers are repeating number sequences many people notice during turning points, decisions, and seasons of growth. This hub helps you move from curiosity into clarity with practical interpretations, numerology families, and intent-specific guidance."}
              </p>
            </div>

            <form onSubmit={onSearch} className="rounded-[1.75rem] border border-gold/20 bg-gradient-to-br from-white/90 to-gold/10 p-6 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Find Your Number</p>
              <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">Search any angel number</h2>
              <p className="mt-3 text-sm leading-7 text-stone-600">
                Type the number you keep seeing and jump straight into its meaning page.
              </p>
              <label className="mt-5 block text-xs font-semibold uppercase tracking-[0.2em] text-stone-500">
                Number (1-10000)
              </label>
              <input
                value={searchValue}
                onChange={(event) => setSearchValue(event.target.value)}
                placeholder="111, 1212, 4444"
                className="mt-2 w-full rounded-2xl border border-gold/20 bg-white/80 px-4 py-3 text-lg font-semibold text-stone-900 outline-none transition focus:border-gold"
              />
              {searchError ? <p className="mt-3 text-sm text-red-600">{searchError}</p> : null}
              <button
                type="submit"
                className="mt-5 inline-flex rounded-full bg-gold px-6 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90"
              >
                Explore number meaning
              </button>
            </form>
          </div>
        </section>

        <section className="mt-8">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Popular Sequences</p>
              <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">Most-searched angel numbers</h2>
            </div>
            <p className="hidden text-sm text-stone-500 sm:block">20 high-interest entry points into the module.</p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-5">
            {(hub?.popular_numbers || []).map((item) => (
              <Link
                key={`${item.display}-${item.number}`}
                to={`/angel-numbers/${item.number}`}
                className="rounded-[1.6rem] border border-gold/20 bg-white/80 p-5 shadow-sm transition hover:-translate-y-0.5 hover:bg-white"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Angel number</p>
                <p className="mt-4 font-cinzel text-5xl font-semibold text-stone-900">{item.display}</p>
                <p className="mt-3 text-sm font-semibold text-stone-800">{item.theme}</p>
              </Link>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">By Intent</p>
          <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">Follow the life area you care about most</h2>
          <div className="mt-5 flex flex-wrap gap-3">
            {intentCards.map((item) => (
              <div key={item.slug} className="rounded-full border border-gold/20 bg-gold/10 px-4 py-3">
                <p className="text-sm font-semibold text-stone-900">{item.display_name}</p>
                <p className="mt-1 text-xs text-stone-600">
                  Try {item.strong_numbers.slice(0, 3).join(", ")}
                </p>
              </div>
            ))}
          </div>
        </section>

        <section className="mt-8 rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Numerology Families</p>
          <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">Numbers grouped by their root vibration</h2>
          <Accordion type="single" collapsible className="mt-4">
            {families.map((family) => (
              <AccordionItem key={family.root} value={`family-${family.root}`}>
                <AccordionTrigger className="text-left">
                  <div>
                    <p className="font-semibold text-stone-900">{family.label}</p>
                    <p className="text-sm text-stone-600">{family.theme}</p>
                  </div>
                </AccordionTrigger>
                <AccordionContent>
                  <div className="flex flex-wrap gap-2">
                    {family.preview.map((number) => (
                      <Link
                        key={number}
                        to={`/angel-numbers/${number}`}
                        className="rounded-full border border-gold/20 bg-gold/5 px-3 py-2 text-sm font-medium text-stone-700 transition hover:bg-gold hover:text-stone-950"
                      >
                        {number}
                      </Link>
                    ))}
                  </div>
                  <p className="mt-4 text-sm text-stone-500">
                    {family.numbers.length} numbers in this family. Temple Team can expand the preview or paginate this list if needed after integration.
                  </p>
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>

        <section className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <article className="rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">How To Use The Signs</p>
            <h2 className="mt-3 font-playfair text-2xl font-semibold text-stone-900">How to work with angel numbers</h2>
            <ol className="mt-5 grid gap-4">
              {(hub?.how_to_work_with_angel_numbers || []).map((step, index) => (
                <li key={step} className="flex gap-4 rounded-[1.5rem] border border-gold/15 bg-gold/5 p-4">
                  <span className="flex h-9 w-9 items-center justify-center rounded-full bg-gold font-semibold text-stone-950">
                    {index + 1}
                  </span>
                  <p className="text-sm leading-7 text-stone-700">{step}</p>
                </li>
              ))}
            </ol>
          </article>

          <article className="rounded-[2rem] border border-gold/20 bg-white/80 p-6 shadow-sm">
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Frequently Asked Questions</p>
            <Accordion type="single" collapsible className="mt-4">
              {(hub?.faq || []).map((item) => (
                <AccordionItem key={item.q} value={item.q}>
                  <AccordionTrigger className="text-left text-base font-semibold text-stone-900">
                    {item.q}
                  </AccordionTrigger>
                  <AccordionContent className="text-sm leading-7 text-stone-600">{item.a}</AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          </article>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default AngelNumbersHubPage;
