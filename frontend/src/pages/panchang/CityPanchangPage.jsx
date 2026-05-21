import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useLocation, useParams } from 'react-router-dom';
import { CalendarDays, MapPin, MoonStar, Sparkles, Sun, Sunrise } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';

const FAQ_ITEMS = [
  {
    question: 'What is Panchang?',
    answer: 'Panchang is the traditional Vedic calendar system that combines Tithi, Nakshatra, Yoga, Karana, and Vara with sunrise-based day timing.',
  },
  {
    question: 'How often does this Panchang update?',
    answer: 'The page is generated from the internal Panchang engine for the selected city and date, and the timing windows are recalculated from astronomical data for that location.',
  },
  {
    question: 'Why does city matter in Panchang?',
    answer: 'Sunrise, sunset, moonrise, and derived auspicious windows change by latitude, longitude, and timezone, so the city affects the exact daily timings.',
  },
];

function isIsoDate(value) {
  return /^\d{4}-\d{2}-\d{2}$/.test(value || '');
}

function formatDisplayDate(value, timezone) {
  try {
    return new Intl.DateTimeFormat('en-IN', {
      timeZone: timezone || 'Asia/Kolkata',
      weekday: 'long',
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    }).format(new Date(`${value}T00:00:00`));
  } catch {
    return value;
  }
}

function formatTimeValue(value, timezone) {
  if (!value) return '--';
  if (/^\d{2}:\d{2}(:\d{2})?$/.test(value)) {
    const [hourText, minuteText, secondText = '00'] = value.split(':');
    const hour = Number(hourText);
    const minute = Number(minuteText);
    const second = Number(secondText);
    if ([hour, minute, second].every((part) => Number.isFinite(part))) {
      const period = hour >= 12 ? 'PM' : 'AM';
      const normalizedHour = hour % 12 || 12;
      const secondSuffix = value.split(':').length > 2 ? `:${String(second).padStart(2, '0')}` : '';
      return `${normalizedHour}:${String(minute).padStart(2, '0')}${secondSuffix} ${period}`;
    }
  }
  const candidate = value.includes('T') ? value : `2000-01-01T${value}`;
  const date = new Date(candidate);
  if (Number.isNaN(date.getTime())) return value;
  try {
    return new Intl.DateTimeFormat('en-IN', {
      timeZone: timezone || 'Asia/Kolkata',
      hour: 'numeric',
      minute: '2-digit',
      second: value.includes(':') && value.split(':').length > 2 ? '2-digit' : undefined,
    }).format(date);
  } catch {
    return value;
  }
}

function buildSchema(data, canonicalUrl, faqItems) {
  return {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Dataset',
        name: `${data.location.label} Panchang ${data.date}`,
        description: `Accurate daily Panchang for ${data.location.label} on ${data.date}.`,
        url: canonicalUrl,
        spatialCoverage: {
          '@type': 'Place',
          name: data.location.label,
        },
        temporalCoverage: data.date,
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

export function CityPanchangPage() {
  const { citySlug = '', date = '' } = useParams();
  const location = useLocation();
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!citySlug || !isIsoDate(date)) {
      setError('Invalid Panchang route.');
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError('');

    axios.get(`${API}/daily`, { params: { location_slug: citySlug, date } })
      .then((response) => {
        if (cancelled) return;
        const nextData = response.data;
        if (nextData?.location?.slug !== citySlug) {
          setError('This city Panchang page is not available.');
          setData(null);
          return;
        }
        setData(nextData);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err?.response?.data?.detail || 'Unable to load Panchang right now.');
        setData(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [citySlug, date]);

  const timezone = data?.location?.timezone || 'Asia/Kolkata';
  const displayDate = data ? formatDisplayDate(data.date, timezone) : date;
  const canonicalUrl = `${SITE}${location.pathname}`;
  const faqItems = useMemo(() => {
    const label = data?.location?.label || citySlug;
    return FAQ_ITEMS.map((item) => ({
      ...item,
      answer: item.answer.replaceAll('the selected city', label),
    }));
  }, [data?.location?.label, citySlug]);
  const schema = data ? buildSchema(data, canonicalUrl, faqItems) : null;
  const title = data
    ? `${data.location.label} Panchang Today ${data.date} - Tithi, Rahu Kaal and Muhurta`
    : 'City Panchang - Daily Hindu Calendar';
  const description = data
    ? `Accurate daily Panchang for ${data.location.label} on ${data.date}. Includes Tithi, Nakshatra, Choghadiya, Rahu Kaal, and all auspicious windows.`
    : 'Daily city Panchang with Tithi, Nakshatra, Rahu Kaal, and Muhurta timings.';

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,rgba(201,150,31,0.16),transparent_24%),linear-gradient(180deg,#fcfaf5_0%,#f5efe3_58%,#ece2cf_100%)] text-stone-900">
      <SEO
        title={title}
        description={description}
        canonical={canonicalUrl}
        hreflang={[
          { lang: 'en-in', href: canonicalUrl },
          { lang: 'en-us', href: canonicalUrl },
        ]}
        jsonLd={schema}
        noindex={!data && !loading}
      />

      <main className="mx-auto max-w-6xl px-4 py-12 sm:px-6 lg:px-8">
        <section className="rounded-[2rem] border border-gold/20 bg-white/75 p-8 shadow-sm backdrop-blur sm:p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Daily City Panchang</p>
          <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="font-cinzel text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">
                {data ? data.location.label : citySlug}
              </h1>
              <p className="mt-3 text-lg font-playfair italic text-stone-700">
                {displayDate}
              </p>
              <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-600">
                City-specific Panchang timings generated from the internal Vedic engine, including Tithi, Nakshatra, Rahu Kaal, Choghadiya, Muhurta windows, and observances.
              </p>
            </div>
            {data && (
              <div className="rounded-[1.5rem] border border-gold/20 bg-gold/5 px-5 py-4">
                <div className="flex items-center gap-2 text-sm font-semibold text-gold">
                  <MapPin className="h-4 w-4" />
                  {data.location.country || 'Panchang location'}
                </div>
                <p className="mt-2 text-sm text-stone-600">{data.location.timezone}</p>
              </div>
            )}
          </div>
        </section>

        {loading && (
          <section className="mt-8 rounded-[1.75rem] border border-gold/15 bg-white/80 p-8 text-sm text-stone-600 shadow-sm">
            Loading Panchang...
          </section>
        )}

        {!loading && error && (
          <section className="mt-8 rounded-[1.75rem] border border-red-200 bg-white/85 p-8 text-sm text-red-600 shadow-sm">
            {error}
          </section>
        )}

        {!loading && data && (
          <>
            <section className="mt-8 grid gap-5 lg:grid-cols-4">
              {[
                ['Sunrise', data.summary.sunrise, Sunrise],
                ['Sunset', data.summary.sunset, Sun],
                ['Moonrise', data.summary.moonrise, MoonStar],
                ['Moonset', data.summary.moonset, Sparkles],
              ].map(([label, value, Icon]) => (
                <article key={label} className="rounded-[1.5rem] border border-gold/15 bg-white/80 p-5 shadow-sm">
                  <div className="flex items-center gap-2 text-sm font-semibold text-gold">
                    <Icon className="h-4 w-4" />
                    {label}
                  </div>
                  <p className="mt-3 font-playfair text-2xl font-semibold text-stone-900">
                    {formatTimeValue(value, timezone)}
                  </p>
                </article>
              ))}
            </section>

            <section className="mt-8 grid gap-5 lg:grid-cols-[1.2fr_0.8fr]">
              <article className="rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                  <CalendarDays className="h-4 w-4" />
                  Panchang details
                </div>
                <div className="mt-5 grid gap-4 md:grid-cols-2">
                  {[
                    ['Tithi', data.panchang.tithi.name, data.panchang.tithi.end],
                    ['Nakshatra', data.panchang.nakshatra.name, data.panchang.nakshatra.end],
                    ['Yoga', data.panchang.yoga.name, data.panchang.yoga.end],
                    ['Karana', data.panchang.karana.name, data.panchang.karana.end],
                    ['Paksha', data.panchang.paksha, null],
                    ['Vara', data.summary.weekday, null],
                    ['Moon Sign', data.panchang.moon_sign, null],
                    ['Sun Sign', data.panchang.sun_sign, null],
                    ['Lunar Month', data.panchang.lunar_month, null],
                    ['Samvat', data.panchang.samvat, null],
                  ].map(([label, value, secondary]) => (
                    <div key={label} className="rounded-2xl border border-gold/10 bg-gold/5 p-4">
                      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">{label}</p>
                      <p className="mt-2 font-playfair text-xl font-semibold text-stone-900">{value}</p>
                      {secondary && (
                        <p className="mt-2 text-xs text-stone-500">Ends {formatTimeValue(secondary, timezone)}</p>
                      )}
                    </div>
                  ))}
                </div>
              </article>

              <article className="rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-gold">Special yogas and observances</p>
                <div className="mt-5 space-y-4">
                  <div className="rounded-2xl border border-gold/10 bg-gold/5 p-4">
                    <h2 className="font-playfair text-xl font-semibold text-stone-900">Special Yogas</h2>
                    {data.special_yogas?.length ? (
                      <ul className="mt-3 space-y-2 text-sm leading-7 text-stone-600">
                        {data.special_yogas.map((item) => <li key={item}>- {item}</li>)}
                      </ul>
                    ) : (
                      <p className="mt-3 text-sm leading-7 text-stone-600">No named special yoga is highlighted for this city-date combination.</p>
                    )}
                  </div>

                  <div className="rounded-2xl border border-gold/10 bg-gold/5 p-4">
                    <h2 className="font-playfair text-xl font-semibold text-stone-900">Observances</h2>
                    {data.observances?.length ? (
                      <ul className="mt-3 space-y-3 text-sm leading-7 text-stone-600">
                        {data.observances.map((item) => (
                          <li key={`${item.slug}-${item.date}`}>
                            <p className="font-semibold text-stone-800">{item.name}</p>
                            <p>{item.summary}</p>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="mt-3 text-sm leading-7 text-stone-600">No festival or vrat observance is surfaced for this date.</p>
                    )}
                  </div>
                </div>
              </article>
            </section>

            <section className="mt-8 rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">Auspicious and caution windows</h2>
              <div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                {data.day_quality_windows.map((window) => (
                  <article key={`${window.label}-${window.start}`} className="rounded-2xl border border-gold/10 bg-white/70 p-4">
                    <div className="flex items-center justify-between gap-3">
                      <p className="font-semibold text-stone-900">{window.label}</p>
                      <span className={`rounded-full px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.16em] ${
                        window.quality === 'good'
                          ? 'bg-emerald-500/15 text-emerald-700'
                          : window.quality === 'caution'
                            ? 'bg-red-500/12 text-red-700'
                            : 'bg-sky-500/12 text-sky-700'
                      }`}>
                        {window.quality}
                      </span>
                    </div>
                    <p className="mt-3 text-sm text-stone-600">
                      {formatTimeValue(window.start, timezone)} - {formatTimeValue(window.end, timezone)}
                    </p>
                  </article>
                ))}
              </div>
            </section>

            <section className="mt-8 rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                  <h2 className="font-playfair text-2xl font-semibold text-stone-900">Move through nearby dates</h2>
                  <p className="mt-2 text-sm text-stone-600">Use the next and previous city-date links to browse the Panchang sequence.</p>
                </div>
                <Link
                  to={`/choghadiya/${citySlug}/today`}
                  className="text-sm font-semibold text-gold transition hover:opacity-80"
                >
                  Open Choghadiya view
                </Link>
              </div>
              <div className="mt-5 flex flex-wrap gap-3">
                <Link
                  to={`/panchang/${citySlug}/${new Date(new Date(data.date).getTime() - 86400000).toISOString().slice(0, 10)}`}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                >
                  Previous day
                </Link>
                <Link
                  to={`/panchang/${citySlug}/${new Date(new Date(data.date).getTime() + 86400000).toISOString().slice(0, 10)}`}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                >
                  Next day
                </Link>
                <Link
                  to={`/calendar/${new Date(data.date).getFullYear()}/${new Date(data.date).getMonth() + 1}`}
                  className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                >
                  Monthly calendar
                </Link>
              </div>
            </section>

            <section className="mt-8 rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
              <h2 className="font-playfair text-2xl font-semibold text-stone-900">Panchang FAQs</h2>
              <div className="mt-5 space-y-4">
                {faqItems.map((item) => (
                  <article key={item.question} className="rounded-2xl border border-gold/10 bg-gold/5 p-4">
                    <h3 className="font-semibold text-stone-900">{item.question}</h3>
                    <p className="mt-2 text-sm leading-7 text-stone-600">{item.answer}</p>
                  </article>
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

export default CityPanchangPage;
