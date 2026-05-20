import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useSearchParams } from 'react-router-dom';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';
import { CalendarDays, HeartHandshake, LoaderCircle, MapPin, Sparkles, Star } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';
const CURRENT_YEAR = new Date().getFullYear();

function formatLongDate(isoDate) {
  return new Date(`${isoDate}T12:00:00`).toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

function buildFaqItems(year, count) {
  return [
    {
      question: `Which are the auspicious marriage dates in ${year}?`,
      answer: count
        ? `There are ${count} Panchang-screened marriage muhurat dates currently listed for ${year} on this page, calculated for New Delhi as the reference location.`
        : `The ${year} list is generated from the live Panchang engine. If no dates are visible, please try reloading or checking the next planning year.`,
    },
    {
      question: 'How are marriage muhurat dates calculated?',
      answer: 'The page filters the year through auspicious Shukla Paksha tithis, preferred marriage nakshatras, Kharmas exclusions, Holashtak, and the cooldown days following Ekadashi, using the existing Panchang engine only.',
    },
    {
      question: 'Which Nakshatra is best for marriage?',
      answer: 'Rohini, Uttara Phalguni, Hasta, Revati, Anuradha, and other classic marriage nakshatras are widely preferred, but the final choice should still be checked against both partners\' birth charts.',
    },
    {
      question: `Which months are inauspicious for marriage in ${year}?`,
      answer: 'Kharmas periods, Adhik Maas spans when present, Holashtak, and Pitru-related no-marriage windows are screened out before dates are shown here.',
    },
    {
      question: 'Can I get a personalised marriage muhurat for my birth chart?',
      answer: 'Yes. A personalised consultation should match the muhurat against both partners\' Lagna, Moon, dasha timing, and compatibility factors rather than relying only on a general calendar.',
    },
  ];
}

function buildSchema(year, count, faqItems) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        name: `Shubh Vivah Muhurat ${year}`,
        url: `${SITE}/muhurat/marriage${year === CURRENT_YEAR ? '' : `?year=${year}`}`,
        description: `Complete list of auspicious Hindu marriage dates for ${year}.`,
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqItems.map((item, index) => ({
          '@type': 'Question',
          name: index === 0 ? `Which are the auspicious marriage dates in ${year}?` : item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: index === 0
              ? `There are ${count} auspicious Vivah Muhurat dates listed for ${year}, calculated from the live Panchang engine for New Delhi.`
              : item.answer,
          },
        })),
      },
    ],
  };
}

function renderStars(score) {
  return Array.from({ length: 5 }, (_, index) => (
    <Star
      key={`star-${index}`}
      className={`h-4 w-4 ${index < score ? 'fill-current text-gold' : 'text-muted-foreground/30'}`}
    />
  ));
}

export function MarriageMuhuratPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const yearParam = searchParams.get('year');
  const parsedYear = yearParam ? Number(yearParam) : NaN;
  const year = Number.isInteger(parsedYear) && parsedYear >= 2000 && parsedYear <= 2100
    ? parsedYear
    : CURRENT_YEAR;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeMonth, setActiveMonth] = useState('all');

  useEffect(() => {
    setActiveMonth('all');
  }, [year]);

  useEffect(() => {
    let ignore = false;

    async function fetchMarriageMuhurat() {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get(`${API}/muhurat/marriage`, {
          params: { year },
        });
        if (!ignore) setData(response.data);
      } catch {
        if (!ignore) {
          setData(null);
          setError('Unable to load marriage muhurat dates right now.');
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchMarriageMuhurat();
    return () => {
      ignore = true;
    };
  }, [year]);

  const faqItems = useMemo(() => buildFaqItems(year, data?.count || 0), [data?.count, year]);
  const schema = useMemo(() => buildSchema(year, data?.count || 0, faqItems), [data?.count, faqItems, year]);
  const canonicalUrl = year === CURRENT_YEAR ? `${SITE}/muhurat/marriage` : `${SITE}/muhurat/marriage?year=${year}`;
  const monthTabs = useMemo(() => {
    const summary = data?.month_summary || [];
    return [
      { key: 'all', label: 'All Months', count: data?.count || 0 },
      ...summary.map((item) => ({
        key: item.month,
        label: item.label,
        count: item.count,
      })),
    ];
  }, [data?.count, data?.month_summary]);
  const visibleDates = useMemo(() => {
    const dates = data?.muhurat_dates || [];
    if (activeMonth === 'all') return dates;
    return dates.filter((item) => item.month === activeMonth);
  }, [activeMonth, data?.muhurat_dates]);

  function setYear(nextYear) {
    if (nextYear === CURRENT_YEAR) {
      setSearchParams({});
      return;
    }
    setSearchParams({ year: String(nextYear) });
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={`Shubh Vivah Muhurat ${year} - Auspicious Hindu Marriage Dates`}
        description={`Complete list of auspicious Hindu marriage dates for ${year}. Vedic Panchang-verified muhurat with Tithi, Nakshatra, and monthly breakdown for your wedding planning.`}
        url={canonicalUrl}
        schema={schema}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/" className="hover:text-gold transition">Home</Link>
          <span>/</span>
          <span className="text-foreground">Marriage Muhurat</span>
        </div>

        <section className="rounded-3xl border border-gold/20 bg-gradient-to-br from-gold/[0.08] via-background to-background p-8 shadow-sm">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 rounded-full border border-gold/20 bg-gold/[0.06] px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gold">
                <HeartHandshake className="h-3.5 w-3.5" />
                Vivah Muhurat
              </div>
              <h1 className="mt-4 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                Shubh Vivah Muhurat {year}
              </h1>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
                Panchang-screened Hindu marriage dates for {year}, with auspicious Tithi, Nakshatra,
                and direct links to the full daily Panchang for each shortlisted wedding date.
              </p>
              <div className="mt-5 flex flex-wrap gap-3 text-sm text-muted-foreground">
                <div className="inline-flex items-center gap-2 rounded-full border border-gold/15 bg-background/70 px-3 py-2">
                  <CalendarDays className="h-4 w-4 text-gold" />
                  <span>{data?.count ?? '--'} shortlisted dates</span>
                </div>
                <div className="inline-flex items-center gap-2 rounded-full border border-gold/15 bg-background/70 px-3 py-2">
                  <MapPin className="h-4 w-4 text-gold" />
                  <span>{data?.location?.label || 'New Delhi'} reference location</span>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border border-gold/20 bg-background/80 p-4 shadow-sm">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Planning Year</p>
              <div className="mt-3 flex items-center gap-3">
                <button
                  type="button"
                  onClick={() => setYear(year - 1)}
                  className="rounded-lg border border-gold/20 px-3 py-2 text-sm text-foreground transition hover:bg-gold/[0.06]"
                >
                  {year - 1}
                </button>
                <div className="rounded-lg bg-gold/[0.08] px-4 py-2 text-center">
                  <p className="text-xs text-muted-foreground">Selected</p>
                  <p className="text-lg font-semibold text-foreground">{year}</p>
                </div>
                <button
                  type="button"
                  onClick={() => setYear(year + 1)}
                  className="rounded-lg border border-gold/20 px-3 py-2 text-sm text-foreground transition hover:bg-gold/[0.06]"
                >
                  {year + 1}
                </button>
              </div>
            </div>
          </div>
        </section>

        <div className="mt-8 grid gap-8 lg:grid-cols-[1.15fr_0.85fr]">
          <section className="rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
            <div className="flex items-center gap-2 text-gold">
              <Sparkles className="h-4 w-4" />
              <h2 className="text-xl font-semibold text-foreground">What makes a date auspicious?</h2>
            </div>
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                <p className="text-sm font-semibold text-foreground">Marriage-friendly Tithis</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  Dwitiya, Tritiya, Panchami, Saptami, Dashami, Ekadashi, and Trayodashi in Shukla Paksha.
                </p>
              </div>
              <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                <p className="text-sm font-semibold text-foreground">Preferred Nakshatras</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  Rohini, Mrigashira, Uttara Phalguni, Hasta, Swati, Anuradha, Revati, and other classic Vivah nakshatras.
                </p>
              </div>
              <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                <p className="text-sm font-semibold text-foreground">Filtered out automatically</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  Kharmas, Adhik Maas spans when present, Holashtak, and the three days following Ekadashi.
                </p>
              </div>
              <div className="rounded-xl border border-gold/15 bg-gold/[0.04] p-4">
                <p className="text-sm font-semibold text-foreground">Reference note</p>
                <p className="mt-2 text-sm leading-6 text-muted-foreground">
                  {data?.advisory || 'Calculated for New Delhi as the standard reference. Muhurat timings may vary slightly by city.'}
                </p>
              </div>
            </div>
          </section>

          <section className="rounded-2xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-foreground">Personalised muhurat matters</h2>
            <p className="mt-3 text-sm leading-6 text-muted-foreground">
              A public muhurat calendar is the first filter. Final wedding timing should still be checked against both
              partners&apos; charts, doshas, dasha timing, and compatibility factors before you lock the ceremony window.
            </p>
            <div className="mt-5 rounded-xl border border-gold/20 bg-background/80 p-4">
              <p className="text-sm font-semibold text-foreground">Best next step for couples</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Use the general dates below for planning, then confirm the final muhurat with a personalised chart-based reading.
              </p>
              <div className="mt-4 flex flex-wrap gap-3">
                <Link
                  to="/kundali-milan"
                  className="inline-flex items-center justify-center rounded-lg bg-gold px-4 py-2 text-sm font-semibold text-primary-foreground transition hover:bg-gold/90"
                >
                  Check Kundali Milan
                </Link>
                <Link
                  to="/birth-chart"
                  className="inline-flex items-center justify-center rounded-lg border border-gold/30 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/[0.06]"
                >
                  Open Birth Chart
                </Link>
              </div>
            </div>
          </section>
        </div>

        <section className="mt-10">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-2xl font-playfair font-bold text-foreground">Auspicious wedding dates</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Browse by month or view the full {year} list.
              </p>
            </div>
            <p className="text-sm text-muted-foreground">
              {loading ? 'Loading live Panchang data...' : `${visibleDates.length} visible date${visibleDates.length === 1 ? '' : 's'}`}
            </p>
          </div>

          <div className="mt-5 overflow-x-auto border-b border-gold/15">
            <div className="flex min-w-max gap-2">
              {monthTabs.map((tab) => {
                const active = activeMonth === tab.key;
                return (
                  <button
                    key={String(tab.key)}
                    type="button"
                    onClick={() => setActiveMonth(tab.key)}
                    className={`border-b-2 px-4 py-3 text-sm font-medium transition ${
                      active
                        ? 'border-gold text-gold'
                        : 'border-transparent text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    {tab.label} ({tab.count})
                  </button>
                );
              })}
            </div>
          </div>

          {loading ? (
            <div className="mt-8 flex items-center justify-center rounded-2xl border border-gold/15 bg-background/80 p-10 text-muted-foreground">
              <LoaderCircle className="mr-3 h-5 w-5 animate-spin text-gold" />
              Loading marriage muhurat dates...
            </div>
          ) : error ? (
            <div className="mt-8 rounded-2xl border border-red-400/20 bg-red-500/10 p-6 text-sm text-red-200">
              {error}
            </div>
          ) : !visibleDates.length ? (
            <div className="mt-8 rounded-2xl border border-gold/15 bg-background/80 p-8 text-center">
              <p className="text-lg font-semibold text-foreground">No dates in this view</p>
              <p className="mt-2 text-sm text-muted-foreground">
                Try another month tab or move to the next planning year.
              </p>
            </div>
          ) : (
            <div className="mt-8 grid gap-4">
              {visibleDates.map((item) => {
                const highlight = item.quality === 'Highly Auspicious';
                return (
                  <article
                    key={item.date}
                    className={`rounded-2xl border border-gold/20 p-5 shadow-sm ${
                      highlight ? 'bg-gold/[0.08]' : 'bg-background/80'
                    }`}
                  >
                    <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                      <div className="space-y-3">
                        <div>
                          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">{item.month_label}</p>
                          <h3 className="mt-1 text-xl font-semibold text-foreground">{formatLongDate(item.date)}</h3>
                          <p className="mt-1 text-sm text-muted-foreground">{item.day_of_week} wedding window</p>
                        </div>

                        <div className="flex flex-wrap gap-2">
                          <span className="rounded-full border border-gold/30 bg-gold/15 px-3 py-1 text-xs font-medium text-gold">
                            {item.tithi}
                          </span>
                          <span className="rounded-full border border-indigo-400/30 bg-indigo-500/15 px-3 py-1 text-xs font-medium text-indigo-300">
                            {item.nakshatra}
                          </span>
                          <span className="rounded-full border border-border bg-background/70 px-3 py-1 text-xs font-medium text-muted-foreground">
                            Lunar month: {item.lunar_month}
                          </span>
                        </div>

                        <p className="text-sm leading-6 text-muted-foreground">{item.notes}</p>
                      </div>

                      <div className="min-w-[240px] rounded-xl border border-gold/15 bg-background/80 p-4 lg:max-w-xs">
                        <p className="text-sm font-semibold text-foreground">{item.quality}</p>
                        <div className="mt-2 flex items-center gap-1">
                          {renderStars(item.quality_score)}
                        </div>
                        <p className="mt-3 text-sm leading-6 text-muted-foreground">
                          Suitable for shortlisting. Final ceremony timing should still be matched against both partners&apos; charts.
                        </p>
                        <Link
                          to={item.panchang_path}
                          className="mt-4 inline-flex items-center text-sm font-semibold text-gold transition hover:text-gold/80"
                        >
                          View full Panchang
                        </Link>
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        <section className="mt-12 rounded-2xl border border-gold/20 bg-background/80 p-6 shadow-sm">
          <h2 className="text-2xl font-playfair font-bold text-foreground">Marriage Muhurat FAQ</h2>
          <Accordion type="single" collapsible className="mt-4">
            {faqItems.map((item, index) => (
              <AccordionItem key={item.question} value={`faq-${index}`}>
                <AccordionTrigger className="text-left text-sm font-medium text-foreground">
                  {item.question}
                </AccordionTrigger>
                <AccordionContent className="text-sm leading-6 text-muted-foreground">
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
