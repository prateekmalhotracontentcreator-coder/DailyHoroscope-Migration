import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, LoaderCircle, Orbit } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { API, SITE, buildArticleSchema, buildBreadcrumbSchema, buildFaqSchema, titleCaseSlug } from './faithShared';
import { FaithGrowthPanel } from './FaithGrowthPanel';
import { FaithPathwayLinks } from './FaithPathwayLinks';

function buildSchema(data) {
  if (!data) return null;
  return {
    '@context': 'https://schema.org',
    '@graph': [
      buildArticleSchema({
        headline: data.title,
        description: data.meta_description,
        url: `${SITE}${data.route}`,
        about: [
          { '@type': 'Book', name: 'Bhagavad Gita' },
          { '@type': 'Book', name: 'The Bible' },
        ],
      }),
      buildFaqSchema(data.faq),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Transit', url: `${SITE}/faith/transit` },
        { name: data.transit_label, url: `${SITE}${data.route}` },
      ]),
    ],
  };
}

export function TransitScripturePage() {
  const { transitSlug = '', tradition = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/transit/${transitSlug}/${tradition}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Transit scripture page not found.' : 'Unable to load this transit page right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPage();
    return () => {
      ignore = true;
    };
  }, [transitSlug, tradition]);

  const schema = useMemo(() => buildSchema(data), [data]);
  const pageTitle = data?.title || `${titleCaseSlug(transitSlug)} guidance`;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(255,193,94,0.14),transparent_28%),linear-gradient(180deg,#0d1015_0%,#141a22_42%,#1f2731_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || pageTitle}
        description={data?.meta_description || 'Transit-based faith guidance.'}
        url={data ? `${SITE}${data.route}` : `${SITE}/faith/transit`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-[#f3d27a]">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/transit" className="transition hover:text-[#f3d27a]">Transit</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.transit_label || titleCaseSlug(transitSlug)}</span>
        </div>

        <Link to="/faith/transit" className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-[#f3d27a]">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to transit hub
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-[#f3d27a]" />
            Loading transit guidance...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-[#d4af37]/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-[#d4af37]/25 bg-[#d4af37]/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">
                    <Orbit className="h-3.5 w-3.5" />
                    {data.tradition_label}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.title}</h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">{data.summary}</p>
                </div>
                <div className="rounded-[1.5rem] border border-[#d4af37]/18 bg-[#d4af37]/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">Transit link</p>
                  <a href={data.links.transit_href} className="mt-2 block font-semibold text-stone-50 underline underline-offset-4">
                    {data.transit_label}
                  </a>
                </div>
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Transit energy</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.energy_intro}</p>
              </article>
              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">{data.practice_title}</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.practice_body}</p>
                <div className="mt-6 flex flex-wrap gap-3">
                  <a href={data.links.panchang_href} className="inline-flex rounded-full bg-[#d4af37] px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                    Check panchang timing
                  </a>
                  <a href={data.links.traits_href} className="inline-flex rounded-full border border-[#d4af37]/18 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-stone-100 transition hover:border-[#d4af37]/35 hover:bg-white/[0.07]">
                    Related traits page
                  </a>
                </div>
              </article>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Scripture anchors</p>
              <div className="mt-6 grid gap-5 lg:grid-cols-2">
                {(data.scripture_cards || []).map((item) => (
                  <article key={item.reference} className="rounded-[1.4rem] border border-[#d4af37]/16 bg-white/[0.04] p-5">
                    <p className="text-xs font-semibold uppercase tracking-[0.18em] text-[#f3d27a]">{item.reference}</p>
                    <p className="mt-3 font-playfair text-xl text-stone-50">{item.text}</p>
                    <p className="mt-4 text-sm leading-7 text-stone-300">{item.why_it_fits}</p>
                  </article>
                ))}
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">{data.prayer_title}</p>
                <p className="mt-4 text-sm leading-8 text-stone-300">{data.prayer_body}</p>
              </article>
              <article className="rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">FAQ</p>
                <Accordion type="single" collapsible className="mt-4 space-y-3">
                  {(data.faq || []).map((item, index) => (
                    <AccordionItem key={item.q} value={`faq-${index}`} className="rounded-[1.1rem] border border-[#d4af37]/16 bg-white/[0.04] px-4">
                      <AccordionTrigger className="text-left text-sm font-semibold text-stone-100">{item.q}</AccordionTrigger>
                      <AccordionContent className="text-sm leading-7 text-stone-300">{item.a}</AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </article>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-[#d4af37]/18 bg-white/[0.05] p-7">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[#f3d27a]">Next step</p>
                  <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Carry the transit into practice, not just interpretation.</h2>
                </div>
                <Link to="/faith/daily" className="inline-flex items-center rounded-full bg-[#d4af37] px-5 py-3 text-sm font-semibold text-stone-950 transition hover:opacity-90">
                  Explore daily scripture
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
            </section>

            <FaithPathwayLinks
              theme="gold"
              title="Use a guided pathway if this transit is part of a larger life issue"
              body="Transit pages are often strongest when paired with a concern-first pathway that also opens the right Gita, Bible, and daily support pages."
            />

            <FaithGrowthPanel
              theme="gold"
              sourceTag={`faith-transit-${transitSlug}`}
              title="Want more transit-based faith journeys?"
              body="Join the Faith updates list and choose the track you want more support around. This helps us build compare-tradition transit journeys and timed devotional follow-ups."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
