import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { ChevronLeft, Check, CalendarDays, Sunrise, Sunset, MoonStar } from 'lucide-react';
import { SEO } from '../../components/SEO';
import { Footer } from '../../components/Footer';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '../../components/ui/accordion';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';
const LOCATION_SLUG = 'new-delhi-india';

const FESTIVAL_DATA = {
  holi: {
    name: 'Holi',
    hindi: 'होली',
    tagline: 'The Festival of Colours',
    description: 'Holi is the ancient Hindu festival of colours, celebrated on Purnima (full moon) of Phalguna month. It marks the victory of good over evil and the arrival of spring.',
    significance: 'Holi celebrates the divine love of Radha and Krishna, the triumph of devotee Prahlad over the demon Holika, and the joyous arrival of spring.',
    rituals: [
      'Holika Dahan - bonfire lit on the eve of Holi (Choti Holi)',
      'Playing with colours - gulal, abir and water on the main day',
      'Thandai - traditional spiced milk drink',
      'Visiting family and exchanging sweets',
      'Puja of Lord Vishnu and Prahlad',
    ],
    panchang_slug: 'holi',
    colour: 'from-pink-500/20 to-orange-500/10',
    icon: '🎨',
    title: (year) => `Holi ${year} - Date, Puja Muhurat & Rituals`,
    descriptionMeta: (year) => `Holi ${year} date, Holika Dahan time, puja muhurat and complete festival guide. Discover the significance and rituals of Holi according to Vedic Panchang.`,
  },
  diwali: {
    name: 'Diwali',
    hindi: 'दिवाली',
    tagline: 'The Festival of Lights',
    description: 'Diwali is the most celebrated Hindu festival, marking Lord Ram\'s return to Ayodhya and the victory of light over darkness, on Amavasya of Kartik month.',
    significance: 'Diwali honours the return of Lord Ram after 14 years of exile, the worship of Goddess Lakshmi for wealth and prosperity, and the New Year for many Indian communities.',
    rituals: [
      'Lakshmi Puja on the main night (Amavasya)',
      'Lighting diyas (oil lamps) and candles throughout the home',
      'Rangoli - decorative patterns at the entrance',
      'Fireworks and celebrations',
      'Exchanging sweets and gifts',
      'Dhanteras - buying gold/silver on the day before Diwali',
    ],
    panchang_slug: 'diwali',
    colour: 'from-yellow-500/20 to-orange-500/10',
    icon: '🪔',
    title: (year) => `Diwali ${year} - Date, Lakshmi Puja Muhurat & Rituals`,
    descriptionMeta: (year) => `Diwali ${year} date, Lakshmi Puja muhurat, and complete festival guide. Get auspicious timing for your Diwali puja according to Vedic Panchang.`,
  },
  'karwa-chauth': {
    name: 'Karwa Chauth',
    hindi: 'करवा चौथ',
    tagline: 'The Festival of Marital Love',
    description: 'Karwa Chauth is observed by married Hindu women who fast from sunrise to moonrise, praying for the long life and wellbeing of their husbands.',
    significance: 'The festival celebrates the bond of marriage and is observed on the Chaturthi (4th day) of Krishna Paksha in the month of Kartik.',
    rituals: [
      'Nirjala fast (no food or water) from sunrise to moonrise',
      'Dressed in bridal attire and jewellery',
      'Karwa Chauth Puja in a group of married women in the evening',
      'Sargi - pre-dawn meal eaten before sunrise (given by mother-in-law)',
      'Breaking fast after sighting the moon through a sieve',
    ],
    panchang_slug: 'karwa-chauth',
    colour: 'from-red-500/20 to-pink-500/10',
    icon: '🌕',
    title: (year) => `Karwa Chauth ${year} - Date, Moonrise Time & Puja Muhurat`,
    descriptionMeta: (year) => `Karwa Chauth ${year} date, moonrise time, and puja muhurat. Complete guide to Karwa Chauth rituals, significance, and Sargi timing.`,
  },
};

function formatLongDate(isoDate) {
  return new Date(`${isoDate}T12:00:00`).toLocaleDateString('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
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

function buildSchema(festival, year, dateValue, faqItems) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Event',
        name: `${festival.name} ${year}`,
        startDate: dateValue,
        location: { '@type': 'Place', name: 'India' },
        description: festival.description,
        organizer: { '@type': 'Organization', name: 'EverydayHoroscope' },
        url: `${SITE}/festivals/${festival.panchang_slug}`,
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

export function FestivalPage({ slug }) {
  const festival = FESTIVAL_DATA[slug];
  const year = new Date().getFullYear();
  const [festivalItem, setFestivalItem] = useState(null);
  const [panchangData, setPanchangData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let ignore = false;

    async function fetchFestivalPageData() {
      if (!festival) return;
      try {
        setLoading(true);
        setError('');
        const festivalResponse = await axios.get(`${API}/festivals`, {
          params: {
            year,
            location_slug: LOCATION_SLUG,
          },
        });
        const matchedFestival = festivalResponse.data?.items?.find((item) => item.slug === festival.panchang_slug);
        if (!matchedFestival) {
          throw new Error('Festival date not found');
        }

        const dailyResponse = await axios.get(`${API}/daily`, {
          params: {
            date: matchedFestival.date,
            location_slug: LOCATION_SLUG,
          },
        });

        if (!ignore) {
          setFestivalItem(matchedFestival);
          setPanchangData(dailyResponse.data);
        }
      } catch {
        if (!ignore) setError('Unable to load festival details right now.');
      } finally {
        if (!ignore) setLoading(false);
      }
    }

    fetchFestivalPageData();
    return () => {
      ignore = true;
    };
  }, [festival, year]);

  const brahmaMuhurta = findWindow(panchangData?.day_quality_windows, 'Brahma Muhurta');
  const abhijitMuhurta = findWindow(panchangData?.day_quality_windows, 'Abhijit Muhurta');
  const faqItems = useMemo(() => {
    if (!festival) return [];

    const dateAnswer = festivalItem
      ? `${festival.name} ${year} is on ${formatLongDate(festivalItem.date)}.`
      : `${festival.name} ${year} falls according to the Vedic Panchang calendar for that year.`;

    const muhuratParts = [];
    if (brahmaMuhurta) muhuratParts.push(`Brahma Muhurta is ${formatClock(brahmaMuhurta.start)} to ${formatClock(brahmaMuhurta.end)}`);
    if (abhijitMuhurta) muhuratParts.push(`Abhijit Muhurta is ${formatClock(abhijitMuhurta.start)} to ${formatClock(abhijitMuhurta.end)}`);
    if (slug === 'karwa-chauth' && panchangData?.summary?.moonrise) muhuratParts.push(`moonrise is at ${panchangData.summary.moonrise}`);

    return [
      {
        question: `When is ${festival.name} in ${year}?`,
        answer: dateAnswer,
      },
      {
        question: `What is the significance of ${festival.name}?`,
        answer: festival.significance,
      },
      {
        question: `What are the rituals of ${festival.name}?`,
        answer: festival.rituals.join('; ') + '.',
      },
      {
        question: `What is the Muhurat for ${festival.name} Puja in ${year}?`,
        answer: muhuratParts.length
          ? `${festival.name} Puja muhurat for ${year} includes ${muhuratParts.join(', ')} according to the Panchang for the festival day.`
          : `Check the Panchang for the festival day to confirm the puja muhurat for ${festival.name} ${year}.`,
      },
    ];
  }, [abhijitMuhurta, brahmaMuhurta, festival, festivalItem, panchangData?.summary?.moonrise, slug, year]);

  if (!festival) return null;

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <SEO
        title={festival.title(year)}
        description={festival.descriptionMeta(year)}
        url={`${SITE}/festivals/${slug}`}
        schema={buildSchema(festival, year, festivalItem?.date || `${year}-01-01`, faqItems)}
      />

      <main className="flex-1 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-6 flex items-center gap-2 text-sm text-muted-foreground">
          <Link to="/" className="hover:text-gold transition">Home</Link>
          <span>/</span>
          <Link to="/festivals" className="hover:text-gold transition">Festivals</Link>
          <span>/</span>
          <span className="text-foreground">{festival.name}</span>
        </div>

        <section className={`rounded-3xl border border-gold/20 bg-gradient-to-br ${festival.colour} p-8 shadow-sm`}>
          <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-5">
              <div className="flex h-20 w-20 items-center justify-center rounded-full border border-gold/20 bg-background/70 text-4xl shadow-sm">
                {festival.icon}
              </div>
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.2em] text-gold">Festival Guide</p>
                <h1 className="mt-2 text-3xl font-playfair font-bold text-foreground sm:text-4xl">
                  {festival.name}
                </h1>
                <p className="mt-1 text-lg text-muted-foreground">{festival.hindi}</p>
                <p className="mt-3 text-sm text-foreground/80">{festival.tagline}</p>
              </div>
            </div>

            <div className="rounded-2xl border border-gold/20 bg-background/70 px-5 py-4 text-sm shadow-sm">
              {loading ? (
                <p className="text-muted-foreground">Loading {year} date...</p>
              ) : error ? (
                <p className="text-muted-foreground">Date unavailable</p>
              ) : (
                <>
                  <p className="font-semibold text-foreground">{year} Date</p>
                  <p className="mt-1 text-muted-foreground">
                    {formatLongDate(festivalItem.date)} - {panchangData?.panchang?.tithi?.name}
                  </p>
                </>
              )}
            </div>
          </div>
        </section>

        {error && <p className="py-12 text-center text-muted-foreground">{error}</p>}

        {!error && (
          <>
            <section className="mt-8 grid gap-6 lg:grid-cols-[1.3fr_1fr]">
              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Why {festival.name} is celebrated</h2>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{festival.description}</p>
                <p className="mt-4 text-sm leading-7 text-muted-foreground">{festival.significance}</p>
              </div>

              <div className="rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
                <h2 className="text-xl font-semibold text-foreground">Festival day Panchang</h2>
                {loading ? (
                  <p className="mt-4 text-sm text-muted-foreground">Loading Panchang...</p>
                ) : (
                  <div className="mt-4 space-y-4 text-sm">
                    <div className="grid gap-3 sm:grid-cols-2">
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Tithi</p>
                        <p className="mt-2 font-semibold text-foreground">{panchangData?.panchang?.tithi?.name}</p>
                      </div>
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Nakshatra</p>
                        <p className="mt-2 font-semibold text-foreground">{panchangData?.panchang?.nakshatra?.name}</p>
                      </div>
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Yoga</p>
                        <p className="mt-2 font-semibold text-foreground">{panchangData?.panchang?.yoga?.name}</p>
                      </div>
                      <div className="rounded-xl border border-gold/10 bg-background/70 p-4">
                        <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Karana</p>
                        <p className="mt-2 font-semibold text-foreground">{panchangData?.panchang?.karana?.name}</p>
                      </div>
                    </div>

                    <div className="grid gap-3 sm:grid-cols-2">
                      <div className="flex items-center gap-3 rounded-xl border border-gold/10 bg-background/70 p-4">
                        <Sunrise className="h-4 w-4 text-gold" />
                        <div>
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Sunrise</p>
                          <p className="font-semibold text-foreground">{panchangData?.summary?.sunrise}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-3 rounded-xl border border-gold/10 bg-background/70 p-4">
                        <Sunset className="h-4 w-4 text-gold" />
                        <div>
                          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Sunset</p>
                          <p className="font-semibold text-foreground">{panchangData?.summary?.sunset}</p>
                        </div>
                      </div>
                      {slug === 'karwa-chauth' && (
                        <div className="flex items-center gap-3 rounded-xl border border-gold/10 bg-background/70 p-4 sm:col-span-2">
                          <MoonStar className="h-4 w-4 text-gold" />
                          <div>
                            <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Moonrise</p>
                            <p className="font-semibold text-foreground">{panchangData?.summary?.moonrise || '--'}</p>
                          </div>
                        </div>
                      )}
                    </div>

                    <div className="grid gap-3 sm:grid-cols-2">
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
                    </div>

                    {festivalItem?.date && (
                      <Link to={`/panchang/date/${festivalItem.date}`} className="inline-flex items-center gap-2 text-gold transition hover:underline">
                        <CalendarDays className="h-4 w-4" />
                        Full Panchang for this day
                      </Link>
                    )}
                  </div>
                )}
              </div>
            </section>

            <section className="mt-8 rounded-xl border border-gold/20 bg-gold/[0.04] p-6 shadow-sm">
              <h2 className="text-xl font-semibold text-foreground">Key rituals</h2>
              <ul className="mt-4 space-y-3">
                {festival.rituals.map((item) => (
                  <li key={item} className="flex items-start gap-3 text-sm leading-7 text-muted-foreground">
                    <Check className="mt-1 h-4 w-4 flex-shrink-0 text-gold" />
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
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
              <h2 className="text-xl font-semibold text-foreground">Get auspicious timing for your {festival.name} Puja</h2>
              <p className="mt-3 max-w-3xl text-sm leading-6 text-muted-foreground">
                Use your birth chart to go beyond the public Panchang and find timing that is personalised to your own planetary placements.
              </p>
              <Link to="/birth-chart" className="mt-5 inline-flex rounded-full bg-gold px-5 py-3 text-sm font-semibold text-background transition hover:opacity-90">
                Unlock your birth chart
              </Link>
            </section>

            <div className="mt-8">
              <Link to="/festivals" className="inline-flex items-center gap-2 text-sm font-semibold text-gold transition hover:underline">
                <ChevronLeft className="h-4 w-4" />
                View all festivals
              </Link>
            </div>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}
