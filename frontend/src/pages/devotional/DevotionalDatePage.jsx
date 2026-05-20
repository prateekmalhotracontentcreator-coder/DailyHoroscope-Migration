import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { CalendarDays, Check, Sparkles, Sunrise, Sunset } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';
const DEFAULT_LOCATION_SLUG = 'new-delhi-india';

const DEVOTIONAL_DATA = {
  ekadashi: {
    name: 'Ekadashi',
    hindi: 'Ekadashi',
    tithi: 'Tithi 11 (Shukla) and Tithi 26 (Krishna)',
    deity: 'Lord Vishnu',
    icon: '🕉️',
    tagline: 'The Sacred Fasting Day of Lord Vishnu',
    description: 'Ekadashi falls on the 11th lunar day of both the waxing and waning moon. In Vaishnava practice it is one of the most respected fasting observances for purification, devotion, and mental discipline.',
    significance: 'Ekadashi is dedicated to Lord Vishnu. Fasting, japa, and scriptural remembrance on this day are believed to deepen sattva, reduce inner heaviness, and create spiritual merit.',
    fastingRules: [
      'Begin the fast at sunrise on Ekadashi and break it on Dwadashi the following morning.',
      'Avoid grains, lentils, and tamasic foods such as onion and garlic.',
      'Fruits, milk, nuts, potatoes, and vrat flours are commonly used for phalahar.',
      'Spend extra time in Vishnu Puja, mantra japa, Bhagavad Gita reading, or Vishnu Sahasranama.',
      'Wake early, bathe before sunrise when possible, and keep the day inward and disciplined.',
      'Donation of food or seva on Ekadashi is considered especially meritorious.',
    ],
    whatToEat: 'Sabudana, fruits, milk, curd, nuts, potatoes, sweet potato, kuttu atta, and other vrat-friendly sattvic foods.',
    whatToAvoid: 'Rice, wheat, barley, lentils, chickpeas, onion, garlic, alcohol, and non-vegetarian food.',
    colour: 'from-indigo-500/20 to-blue-500/10',
    metaTitle: (year) => `Ekadashi ${year} - Next Date, Fasting Rules and Significance`,
    metaDescription: (year) => `When is the next Ekadashi in ${year}? Get the exact date, Panchang details, fasting rules, and what to eat and avoid during Ekadashi vrat.`,
  },
  amavasya: {
    name: 'Amavasya',
    hindi: 'Amavasya',
    tithi: 'Tithi 30 (New Moon)',
    deity: 'Pitrs and Shiva traditions',
    icon: '🌑',
    tagline: 'The New Moon Day of Ancestral Offerings',
    description: 'Amavasya is the new moon day and the final tithi of the lunar month. It is widely observed for ancestor remembrance, introspection, and quiet ritual work.',
    significance: 'Amavasya is especially important for Pitru Tarpan, Shraddha-related remembrance, and simple offerings made in gratitude to ancestors. In many traditions it is also a powerful day for Shiva worship and inner cleansing.',
    fastingRules: [
      'A full fast is optional, but many devotees keep the day simple and sattvic.',
      'Pitru Tarpan with water and black sesame is one of the most important Amavasya observances.',
      'Lighting a diya in memory of ancestors is a common evening practice.',
      'Charity and food donation in the name of ancestors are considered auspicious.',
      'Avoid celebratory or highly auspicious new beginnings on Amavasya in many traditions.',
    ],
    whatToEat: 'Simple sattvic meals, fruit, milk, and light food if you are observing a partial fast.',
    whatToAvoid: 'Alcohol, non-vegetarian food, and in many households the launch of major new ventures or ceremonies.',
    colour: 'from-slate-500/20 to-gray-500/10',
    metaTitle: (year) => `Amavasya ${year} - Next Date, Rituals and Puja Muhurat`,
    metaDescription: (year) => `When is the next Amavasya in ${year}? Get the exact date, Pitru Tarpan muhurat, rituals and Panchang for Amavasya.`,
  },
  purnima: {
    name: 'Purnima',
    hindi: 'Purnima',
    tithi: 'Tithi 15 (Full Moon)',
    deity: 'Chandra, Vishnu, and Shiva by observance',
    icon: '🌕',
    tagline: 'The Full Moon Day of Illumination and Devotion',
    description: 'Purnima marks the full moon and the 15th tithi of the bright lunar fortnight. It is associated with fullness, clarity, devotion, and spiritually heightened lunar energy.',
    significance: 'Many of the most cherished devotional observances of the year fall on Purnima. The day is considered supportive for japa, Satyanarayana Puja, offerings to the moon, and practices of gratitude and abundance.',
    fastingRules: [
      'Many devotees observe a simple phalahar fast using fruits, milk, and light sattvic food.',
      'Offer arghya to the full moon in the evening when visible.',
      'Satyanarayana Puja is traditionally performed on Purnima in many households.',
      'Lighting a ghee lamp, mantra japa, and charity are widely recommended.',
      'Keep the day calm, devotional, and mentally clear rather than over-scheduled.',
    ],
    whatToEat: 'Fruits, milk, curd, nuts, sago, and other light sattvic preparations commonly used for vrat.',
    whatToAvoid: 'Alcohol, non-vegetarian food, and heavy tamasic meals if observing the vrat traditionally.',
    colour: 'from-amber-500/20 to-yellow-500/10',
    metaTitle: (year) => `Purnima ${year} - Next Full Moon Date, Fasting and Significance`,
    metaDescription: (year) => `When is the next Purnima (full moon) in ${year}? Get the date, Panchang, fasting rules and puja muhurat for Purnima.`,
  },
};

function formatIsoDate(dateValue) {
  const year = dateValue.getFullYear();
  const month = String(dateValue.getMonth() + 1).padStart(2, '0');
  const day = String(dateValue.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function formatLongDate(isoDate) {
  return new Date(`${isoDate}T12:00:00`).toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

function formatShortDate(isoDate) {
  return new Date(`${isoDate}T12:00:00`).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
}

function formatClock(value) {
  if (!value) return '--';
  if (/^\d{2}:\d{2}:\d{2}$/.test(value)) return value.slice(0, 5);
  return new Date(value).toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

function findWindow(windows, label) {
  return windows?.find((item) => item.label === label) || null;
}

function buildSchema(config, nextItem, faqItems) {
  if (!nextItem) return null;
  const monthLabel = new Date(`${nextItem.date}T12:00:00`).toLocaleDateString('en-IN', {
    month: 'long',
    year: 'numeric',
  });

  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Event',
        name: `${config.name} - ${monthLabel}`,
        startDate: nextItem.date,
        description: config.tagline,
        location: { '@type': 'Place', name: 'India' },
        url: `${SITE}/${nextItem.slug}`,
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqItems.map((item) => ({
          '@type': 'Question',
          name: item.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.answer,
          },
        })),
      },
    ],
  };
}

function buildFaqItems(config, nextItem) {
  const nextAnswer = nextItem
    ? `The next ${config.name} is on ${formatLongDate(nextItem.date)}.`
    : `The next ${config.name} date is determined from the live Panchang calendar.`;

  return [
    {
      question: `When is the next ${config.name}?`,
      answer: nextAnswer,
    },
    {
      question: `What to eat during ${config.name} fast?`,
      answer: config.whatToEat,
    },
    {
      question: `What rituals should be done on ${config.name}?`,
      answer: config.fastingRules.join(' '),
    },
    {
      question: `What should be avoided on ${config.name}?`,
      answer: config.whatToAvoid,
    },
  ];
}

export function DevotionalDatePage({ type }) {
  const config = DEVOTIONAL_DATA[type];
  const [upcomingDates, setUpcomingDates] = useState([]);
  const [nextPanchang, setNextPanchang] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!config) return undefined;

    let ignore = false;

    async function fetchPageData() {
      const todayIso = formatIsoDate(new Date());
      const currentYear = new Date().getFullYear();

      try {
        setLoading(true);
        setError('');

        const [currentYearResponse, nextYearResponse] = await Promise.all([
          axios.get(`${API}/festivals`, {
            params: {
              year: currentYear,
              location_slug: DEFAULT_LOCATION_SLUG,
            },
          }),
          axios.get(`${API}/festivals`, {
            params: {
              year: currentYear + 1,
              location_slug: DEFAULT_LOCATION_SLUG,
            },
          }),
        ]);

        const mergedItems = [...(currentYearResponse.data?.items || []), ...(nextYearResponse.data?.items || [])];
        const filteredItems = mergedItems
          .filter((item) => item.slug === type && item.date >= todayIso)
          .sort((left, right) => left.date.localeCompare(right.date))
          .filter((item, index, array) => index === 0 || item.date !== array[index - 1].date);

        if (!filteredItems.length) {
          throw new Error('No upcoming observances found');
        }

        const nextItem = filteredItems[0];
        const dailyResponse = await axios.get(`${API}/daily`, {
          params: {
            date: nextItem.date,
            location_slug: DEFAULT_LOCATION_SLUG,
          },
        });

        if (!ignore) {
          setUpcomingDates(filteredItems.slice(0, 6));
          setNextPanchang(dailyResponse.data);
        }
      } catch {
        if (!ignore) {
          setUpcomingDates([]);
          setNextPanchang(null);
          setError(`Unable to load ${config.name} details right now.`);
        }
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchPageData();
    return () => {
      ignore = true;
    };
  }, [config, type]);

  const nextItem = upcomingDates[0] || null;
  const faqItems = useMemo(() => buildFaqItems(config, nextItem), [config, nextItem]);
  const schema = useMemo(() => buildSchema(config, nextItem, faqItems), [config, faqItems, nextItem]);
  const brahmaMuhurta = findWindow(nextPanchang?.day_quality_windows, 'Brahma Muhurta');
  const abhijitMuhurta = findWindow(nextPanchang?.day_quality_windows, 'Abhijit Muhurta');
  const rahuKaal = findWindow(nextPanchang?.day_quality_windows, 'Rahu Kaal');
  const seoYear = nextItem ? new Date(`${nextItem.date}T12:00:00`).getFullYear() : new Date().getFullYear();

  if (!config) return null;

  const relatedLinks = Object.entries(DEVOTIONAL_DATA).filter(([key]) => key !== type);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={config.metaTitle(seoYear)}
        description={config.metaDescription(seoYear)}
        url={`${SITE}/${type}`}
        schema={schema}
      />

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className={`rounded-3xl border border-gold/20 bg-gradient-to-br ${config.colour} p-8 shadow-sm`}>
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-5">
              <div className="flex h-20 w-20 items-center justify-center rounded-full border border-gold/20 bg-background/70 text-4xl shadow-sm">
                {config.icon}
              </div>
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gold">Devotional Date Guide</p>
                <h1 className="mt-2 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                  {config.name} - {config.tagline}
                </h1>
                <p className="mt-2 text-sm text-muted-foreground">{config.hindi} · {config.deity}</p>
                <p className="mt-3 text-sm text-foreground/80">{config.tithi}</p>
              </div>
            </div>

            <div className="rounded-2xl border border-gold/20 bg-background/70 px-5 py-4 text-sm shadow-sm">
              {loading ? (
                <p className="text-muted-foreground">Loading next date...</p>
              ) : error ? (
                <p className="text-muted-foreground">Date unavailable</p>
              ) : (
                <>
                  <p className="font-semibold text-foreground">Next {config.name}</p>
                  <p className="mt-1 text-muted-foreground">{formatLongDate(nextItem.date)}</p>
                </>
              )}
            </div>
          </div>
        </section>

        {error && <p className="py-12 text-center text-muted-foreground">{error}</p>}

        {!error && (
          <>
            <section className="mt-8 rounded-2xl border border-gold/20 bg-gradient-to-br from-gold/15 to-gold/5 p-6 shadow-sm">
              {loading ? (
                <p className="text-sm text-muted-foreground">Loading next {config.name.toLowerCase()} details...</p>
              ) : (
                <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-gold">Next Date</p>
                    <h2 className="mt-2 text-2xl font-playfair font-bold text-foreground">
                      Next {config.name}: {formatLongDate(nextItem.date)}
                    </h2>
                    <p className="mt-3 text-sm text-muted-foreground">
                      {nextPanchang?.panchang?.tithi?.name} · {nextPanchang?.panchang?.paksha || 'Lunar Paksha'} · {nextPanchang?.panchang?.nakshatra?.name}
                    </p>
                  </div>

                  <Link to={`/panchang/date/${nextItem.date}`} className="inline-flex items-center gap-2 rounded-full border border-gold px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold/10">
                    <CalendarDays className="h-4 w-4" />
                    View full Panchang for this day
                  </Link>
                </div>
              )}
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[0.95fr_1.05fr]">
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Upcoming {config.name} dates</h2>
                {loading ? (
                  <p className="mt-4 text-sm text-muted-foreground">Loading upcoming dates...</p>
                ) : (
                  <div className="mt-5 space-y-4">
                    {upcomingDates.map((item) => (
                      <div key={item.date} className="flex items-start gap-4">
                        <div className="mt-1.5 h-3 w-3 rounded-full bg-gold" />
                        <div className="flex-1 rounded-xl border border-gold/10 bg-background/70 p-4">
                          <div className="flex flex-wrap items-start justify-between gap-3">
                            <div>
                              <p className="font-semibold text-foreground">{formatShortDate(item.date)}</p>
                              <p className="mt-1 text-xs text-muted-foreground">{item.name}</p>
                            </div>
                            <Link to={`/panchang/date/${item.date}`} className="text-sm text-gold transition hover:underline">
                              Panchang ->
                            </Link>
                          </div>
                          <p className="mt-3 text-sm leading-6 text-muted-foreground">{item.summary}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Panchang for the next date</h2>
                {loading ? (
                  <p className="mt-4 text-sm text-muted-foreground">Loading Panchang...</p>
                ) : (
                  <div className="mt-4 space-y-4 text-sm">
                    <div className="grid gap-3 sm:grid-cols-2">
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Tithi</p>
                        <p className="mt-2 font-semibold text-foreground">{nextPanchang?.panchang?.tithi?.name}</p>
                      </div>
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Nakshatra</p>
                        <p className="mt-2 font-semibold text-foreground">{nextPanchang?.panchang?.nakshatra?.name}</p>
                      </div>
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Yoga</p>
                        <p className="mt-2 font-semibold text-foreground">{nextPanchang?.panchang?.yoga?.name}</p>
                      </div>
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Karana</p>
                        <p className="mt-2 font-semibold text-foreground">{nextPanchang?.panchang?.karana?.name}</p>
                      </div>
                    </div>

                    <div className="grid gap-3 sm:grid-cols-2">
                      <div className="flex items-center gap-3 rounded-xl border border-gold/10 bg-background/70 p-4">
                        <Sunrise className="h-4 w-4 text-gold" />
                        <div>
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Sunrise</p>
                          <p className="font-semibold text-foreground">{nextPanchang?.summary?.sunrise}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3 rounded-xl border border-gold/10 bg-background/70 p-4">
                        <Sunset className="h-4 w-4 text-gold" />
                        <div>
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Sunset</p>
                          <p className="font-semibold text-foreground">{nextPanchang?.summary?.sunset}</p>
                        </div>
                      </div>
                    </div>

                    <div className="grid gap-3 sm:grid-cols-3">
                      {brahmaMuhurta && (
                        <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Brahma Muhurta</p>
                          <p className="mt-2 font-semibold text-foreground">{formatClock(brahmaMuhurta.start)} - {formatClock(brahmaMuhurta.end)}</p>
                        </div>
                      )}
                      {abhijitMuhurta && (
                        <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Abhijit Muhurta</p>
                          <p className="mt-2 font-semibold text-foreground">{formatClock(abhijitMuhurta.start)} - {formatClock(abhijitMuhurta.end)}</p>
                        </div>
                      )}
                      {rahuKaal && (
                        <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Rahu Kaal</p>
                          <p className="mt-2 font-semibold text-foreground">{formatClock(rahuKaal.start)} - {formatClock(rahuKaal.end)}</p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-[1fr_1fr]">
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Significance</h2>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{config.description}</p>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{config.significance}</p>
              </div>

              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Fasting rules and rituals</h2>
                <ul className="mt-4 space-y-3">
                  {config.fastingRules.map((item) => (
                    <li key={item} className="flex items-start gap-3 text-sm leading-7 text-muted-foreground">
                      <Check className="mt-1 h-4 w-4 flex-shrink-0 text-gold" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="mt-8 grid gap-6 lg:grid-cols-2">
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">What to eat</h2>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{config.whatToEat}</p>
              </div>

              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">What to avoid</h2>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{config.whatToAvoid}</p>
              </div>
            </section>

            <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">Frequently asked questions</h2>
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

            <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.05] p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">Get personalised Puja timing for your birth chart</h2>
              <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">
                Public Panchang timing is a strong starting point. A full birth chart helps you align fasting, mantra, and devotional windows more personally to your own planetary placements.
              </p>
              <Link to="/birth-chart" className="mt-5 inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90">
                Unlock your birth chart
              </Link>
            </section>

            <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-gold" />
                <h2 className="text-xl font-semibold text-foreground">Related devotional dates</h2>
              </div>
              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                {relatedLinks.map(([key, item]) => (
                  <Link key={key} to={`/${key}`} className="rounded-xl border border-border bg-background/70 p-4 text-sm text-foreground transition hover:border-gold/30 hover:text-gold">
                    {item.name} -> {item.tagline}
                  </Link>
                ))}
              </div>
            </section>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
