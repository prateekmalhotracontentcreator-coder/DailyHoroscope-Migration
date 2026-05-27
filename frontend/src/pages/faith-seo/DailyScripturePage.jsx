import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useParams } from 'react-router-dom';
import { ArrowLeft, ArrowRight, LoaderCircle, SunMoon } from 'lucide-react';
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
        about: {
          '@type': 'Thing',
          name: `Daily spiritual practice for ${data.sign_name} energy in ${data.month_name}`,
        },
      }),
      buildFaqSchema(data.faq),
      buildBreadcrumbSchema([
        { name: 'Home', url: SITE },
        { name: 'Faith Hubs', url: `${SITE}/faith` },
        { name: 'Daily', url: `${SITE}/faith/daily` },
        { name: data.sign_name, url: `${SITE}/faith/daily/${data.sign_slug}` },
        { name: data.month_name, url: `${SITE}${data.route}` },
      ]),
    ],
  };
}

export function DailyScripturePage() {
  const { sign = '', month = '' } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchPage() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/daily/${sign}/${month}`);
        if (!ignore) setData(response.data);
      } catch (err) {
        if (!ignore) {
          setData(null);
          setError(err?.response?.status === 404 ? 'Daily scripture page not found.' : 'Unable to load this daily guide right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPage();
    return () => {
      ignore = true;
    };
  }, [month, sign]);

  const schema = useMemo(() => buildSchema(data), [data]);
  const fallbackTitle = `${titleCaseSlug(sign)} Spiritual Guide - ${titleCaseSlug(month)}`;

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,rgba(144,202,249,0.16),transparent_28%),linear-gradient(180deg,#0f1116_0%,#151b22_42%,#1d2530_100%)] text-stone-100">
      <SEO
        title={data?.meta_title || fallbackTitle}
        description={data?.meta_description || 'Daily scripture guide by sign and month.'}
        url={data ? `${SITE}${data.route}` : `${SITE}/faith/daily/${sign}/${month}`}
        schema={schema}
        noindex={!loading && !!error && !data}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mb-6 flex items-center gap-2 text-sm text-stone-400">
          <Link to="/faith" className="transition hover:text-sky-300">Faith Hubs</Link>
          <span>/</span>
          <Link to="/faith/daily" className="transition hover:text-sky-300">Daily</Link>
          <span>/</span>
          <Link to={`/faith/daily/${sign}`} className="transition hover:text-sky-300">{data?.sign_name || titleCaseSlug(sign)}</Link>
          <span>/</span>
          <span className="text-stone-200">{data?.month_name || titleCaseSlug(month)}</span>
        </div>

        <Link to={`/faith/daily/${sign}`} className="mb-6 inline-flex items-center text-sm font-medium text-stone-400 transition hover:text-sky-300">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to sign guide
        </Link>

        {loading ? (
          <div className="flex items-center justify-center rounded-[2rem] border border-sky-300/20 bg-white/[0.05] p-12 text-stone-300">
            <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-sky-200" />
            Loading daily scripture guide...
          </div>
        ) : error ? (
          <div className="rounded-[2rem] border border-red-400/25 bg-red-500/10 p-6 text-sm text-red-200">{error}</div>
        ) : data ? (
          <>
            <section className="rounded-[2rem] border border-sky-300/20 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.28)] backdrop-blur">
              <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                <div className="max-w-3xl">
                  <div className="inline-flex items-center gap-2 rounded-full border border-sky-300/25 bg-sky-400/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">
                    <SunMoon className="h-3.5 w-3.5" />
                    {data.sign_name} • {data.month_name}
                  </div>
                  <h1 className="mt-4 font-cinzel text-4xl font-semibold leading-tight text-stone-50 sm:text-5xl">{data.title}</h1>
                  <p className="mt-4 text-base leading-8 text-stone-300">{data.summary}</p>
                </div>
                <div className="rounded-[1.5rem] border border-sky-300/18 bg-sky-400/10 px-5 py-4 text-sm">
                  <p className="text-xs font-semibold uppercase tracking-[0.18em] text-sky-200">Transit companion</p>
                  <Link to={data.links.transit_href} className="mt-2 block font-semibold text-stone-50 underline underline-offset-4">
                    Open related transit guide
                  </Link>
                </div>
              </div>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-sky-300/18 bg-white/[0.05] p-7">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">Sign and month energy</p>
              <p className="mt-4 text-sm leading-8 text-stone-300">{data.energy_intro}</p>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-2">
              <article className="rounded-[1.8rem] border border-sky-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">Gita verse for this month</p>
                <p className="mt-4 text-sm font-semibold text-stone-50">{data.gita_reference}</p>
                <p className="mt-3 font-playfair text-xl text-stone-100">{data.gita_text}</p>
                <p className="mt-4 text-sm leading-7 text-stone-300">{data.gita_application}</p>
              </article>

              <article className="rounded-[1.8rem] border border-sky-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">Bible promise for this month</p>
                <p className="mt-4 text-sm font-semibold text-stone-50">{data.bible_reference}</p>
                <p className="mt-3 font-playfair text-xl text-stone-100">{data.bible_text}</p>
                <p className="mt-4 text-sm leading-7 text-stone-300">{data.bible_application}</p>
              </article>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
              <article className="rounded-[1.8rem] border border-sky-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">{data.daily_practice_title}</p>
                <ul className="mt-5 space-y-3 text-sm text-stone-300">
                  {(data.daily_practices || []).map((item) => (
                    <li key={item} className="rounded-[1.1rem] border border-sky-300/16 bg-white/[0.04] px-4 py-3 leading-7">
                      {item}
                    </li>
                  ))}
                </ul>
              </article>

              <article className="rounded-[1.8rem] border border-sky-300/18 bg-white/[0.05] p-7">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">FAQ</p>
                <Accordion type="single" collapsible className="mt-4 space-y-3">
                  {(data.faq || []).map((item, index) => (
                    <AccordionItem key={item.q} value={`faq-${index}`} className="rounded-[1.1rem] border border-sky-300/16 bg-white/[0.04] px-4">
                      <AccordionTrigger className="text-left text-sm font-semibold text-stone-100">{item.q}</AccordionTrigger>
                      <AccordionContent className="text-sm leading-7 text-stone-300">{item.a}</AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              </article>
            </section>

            <section className="mt-8 rounded-[1.8rem] border border-sky-300/18 bg-white/[0.05] p-7">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.24em] text-sky-200">Premium next step</p>
                  <h2 className="mt-2 font-playfair text-2xl font-semibold text-stone-50">Turn the guide into a personalized 21-day path.</h2>
                  <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-300">{data.cta.label}</p>
                </div>
                <Link to={data.cta.href} className="inline-flex items-center rounded-full bg-sky-300 px-5 py-3 text-sm font-semibold text-slate-950 transition hover:opacity-90">
                  Match it to your birth chart
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </div>
            </section>

            <FaithPathwayLinks
              theme="sky"
              title="Need a concern-first route beyond this monthly guide?"
              body="When the monthly rhythm is helpful but not specific enough, use a guided pathway to jump into matched Gita, Bible, and transit pages around the same pressure."
            />

            <FaithGrowthPanel
              theme="sky"
              sourceTag={`faith-daily-${sign}`}
              title="Want this daily layer turned into a devotional sequence?"
              body="Join the Faith updates list if you want sign-based monthly devotionals, guided reading plans, and follow-up scripture emails built from pages like this one."
            />
          </>
        ) : null}
      </main>

      <Footer />
    </div>
  );
}
