import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { Link, useLocation, useParams } from 'react-router-dom';
import { Clock3, MapPin, Sparkles } from 'lucide-react';
import { Footer } from '../../components/Footer';
import { SEO } from '../../components/SEO';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://www.everydayhoroscope.in';
const PERIOD_CONFIG = {
  today: { label: 'Today Day', dayOffset: 0, table: 'day', canonical: 'today' },
  tonight: { label: 'Today Night', dayOffset: 0, table: 'night', canonical: 'tonight' },
  tomorrow: { label: 'Tomorrow Day', dayOffset: 1, table: 'day', canonical: 'tomorrow' },
  'tomorrow-night': { label: 'Tomorrow Night', dayOffset: 1, table: 'night', canonical: 'tomorrow-night' },
};

function formatDateLabel(value, timezone) {
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

function formatDateForParam(baseDate, offset) {
  const nextDate = new Date(`${baseDate}T00:00:00Z`);
  nextDate.setUTCDate(nextDate.getUTCDate() + offset);
  return nextDate.toISOString().slice(0, 10);
}

function formatTimeValue(value, timezone) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat('en-IN', {
    timeZone: timezone || 'Asia/Kolkata',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date);
}

function buildSchema(locationLabel, canonicalUrl, periodLabel) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: `What is Choghadiya in ${locationLabel}?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Choghadiya divides the day and night into eight equal segments from sunrise and sunset for ${locationLabel}. Each segment carries a traditional quality such as Amrit, Shubh, Labh, Char, Rog, Kaal, or Udveg.`,
        },
      },
      {
        '@type': 'Question',
        name: `How do I use the ${periodLabel} Choghadiya table?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Use the ${periodLabel.toLowerCase()} table to identify stronger and weaker windows for starting travel, rituals, business, or important tasks. City sunrise and sunset determine the exact slot timings.`,
        },
      },
      {
        '@type': 'Question',
        name: 'Why is city-specific Choghadiya different?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'The slot boundaries change with sunrise and sunset, so different cities produce different Choghadiya timings even on the same calendar day.',
        },
      },
    ],
    url: canonicalUrl,
  };
}

export function ChoghadiyaPage() {
  const { citySlug = '', period = '' } = useParams();
  const location = useLocation();
  const config = PERIOD_CONFIG[period];
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!config) {
      setError('Invalid Choghadiya route.');
      setLoading(false);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError('');

    async function loadChoghadiya() {
      try {
        let requestDate;
        if (config.dayOffset > 0) {
          const dailyResponse = await axios.get(`${API}/daily`, { params: { location_slug: citySlug } });
          const resolvedDaily = dailyResponse.data;
          if (resolvedDaily?.location?.slug !== citySlug) {
            setError('This city Choghadiya page is not available.');
            setData(null);
            return;
          }
          requestDate = formatDateForParam(resolvedDaily.date, config.dayOffset);
        }

        const response = await axios.get(`${API}/choghadiya`, {
          params: requestDate ? { location_slug: citySlug, date: requestDate } : { location_slug: citySlug },
        });
        if (cancelled) return;
        const nextData = response.data;
        if (nextData?.location?.slug !== citySlug) {
          setError('This city Choghadiya page is not available.');
          setData(null);
          return;
        }
        setData(nextData);
      } catch (err) {
        if (cancelled) return;
        setError(err?.response?.data?.detail || 'Unable to load Choghadiya right now.');
        setData(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    void loadChoghadiya();

    return () => {
      cancelled = true;
    };
  }, [citySlug, config]);

  const timezone = data?.location?.timezone || 'Asia/Kolkata';
  const selectedSlots = useMemo(() => {
    if (!data || !config) return [];
    return config.table === 'day' ? data.day_choghadiya : data.night_choghadiya;
  }, [data, config]);
  const now = Date.now();
  const canonicalUrl = `${SITE}${location.pathname}`;
  const title = data
    ? `${data.location.label} Choghadiya ${config.label} - Best Auspicious Hours`
    : 'City Choghadiya - Auspicious Hours';
  const description = data
    ? `Check ${config.label.toLowerCase()} Choghadiya timings in ${data.location.label}. Find the best Amrit and Shubh hours for starting new activities.`
    : 'City-specific Choghadiya timings with auspicious and caution windows.';
  const schema = data && config ? buildSchema(data.location.label, canonicalUrl, config.label) : null;

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
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-gold">Regional Choghadiya</p>
          <div className="mt-4 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="font-cinzel text-4xl font-semibold tracking-tight text-stone-900 sm:text-5xl">
                {data ? data.location.label : citySlug}
              </h1>
              <p className="mt-3 text-lg font-playfair italic text-stone-700">
                {config?.label || 'Selected period'}
              </p>
              <p className="mt-3 max-w-2xl text-sm leading-7 text-stone-600">
                Full eight-slot Choghadiya timing table calculated from city-specific sunrise and sunset, with auspicious quality labels and a live "Now" indicator when a slot is active.
              </p>
            </div>
            {data && (
              <div className="rounded-[1.5rem] border border-gold/20 bg-gold/5 px-5 py-4">
                <div className="flex items-center gap-2 text-sm font-semibold text-gold">
                  <MapPin className="h-4 w-4" />
                  {formatDateLabel(data.date, timezone)}
                </div>
                <p className="mt-2 text-sm text-stone-600">{data.location.timezone}</p>
              </div>
            )}
          </div>
        </section>

        <section className="mt-8 flex flex-wrap gap-3">
          {Object.entries(PERIOD_CONFIG).map(([key, item]) => (
            <Link
              key={key}
              to={`/choghadiya/${citySlug}/${key}`}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                key === period
                  ? 'bg-gold text-stone-950'
                  : 'border border-gold/20 bg-gold/10 text-gold hover:bg-gold hover:text-stone-950'
              }`}
            >
              {item.label}
            </Link>
          ))}
        </section>

        {loading && (
          <section className="mt-8 rounded-[1.75rem] border border-gold/15 bg-white/80 p-8 text-sm text-stone-600 shadow-sm">
            Loading Choghadiya...
          </section>
        )}

        {!loading && error && (
          <section className="mt-8 rounded-[1.75rem] border border-red-200 bg-white/85 p-8 text-sm text-red-600 shadow-sm">
            {error}
          </section>
        )}

        {!loading && data && (
          <>
            <section className="mt-8 grid gap-5 md:grid-cols-3">
              <article className="rounded-[1.5rem] border border-gold/15 bg-white/80 p-5 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Sunrise</p>
                <p className="mt-2 font-playfair text-2xl font-semibold text-stone-900">{formatTimeValue(data.sunrise, timezone)}</p>
              </article>
              <article className="rounded-[1.5rem] border border-gold/15 bg-white/80 p-5 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Sunset</p>
                <p className="mt-2 font-playfair text-2xl font-semibold text-stone-900">{formatTimeValue(data.sunset, timezone)}</p>
              </article>
              <article className="rounded-[1.5rem] border border-gold/15 bg-white/80 p-5 shadow-sm">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-gold">Next Sunrise</p>
                <p className="mt-2 font-playfair text-2xl font-semibold text-stone-900">{formatTimeValue(data.next_sunrise, timezone)}</p>
              </article>
            </section>

            <section className="mt-8 rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.24em] text-gold">
                <Clock3 className="h-4 w-4" />
                {config.label} slots
              </div>
              <div className="mt-5 overflow-hidden rounded-2xl border border-gold/10">
                <div className="grid grid-cols-[0.65fr_1.1fr_0.8fr_1fr] bg-gold/10 px-4 py-3 text-xs font-semibold uppercase tracking-[0.18em] text-stone-700">
                  <span>Slot</span>
                  <span>Timing</span>
                  <span>Quality</span>
                  <span>Planetary ruler</span>
                </div>
                {selectedSlots.map((slot) => {
                  const isNow = now >= new Date(slot.start).getTime() && now < new Date(slot.end).getTime();
                  return (
                    <div key={`${slot.index}-${slot.start}`} className={`grid grid-cols-[0.65fr_1.1fr_0.8fr_1fr] gap-3 border-t border-gold/10 px-4 py-4 text-sm ${isNow ? 'bg-gold/8' : 'bg-white/80'}`}>
                      <div className="flex items-center gap-2 font-semibold text-stone-900">
                        <span>{slot.name}</span>
                        {isNow && (
                          <span className="rounded-full bg-gold px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.14em] text-stone-950">
                            Now
                          </span>
                        )}
                      </div>
                      <span className="text-stone-600">
                        {formatTimeValue(slot.start, timezone)} - {formatTimeValue(slot.end, timezone)}
                      </span>
                      <span className={`font-semibold ${
                        slot.quality === 'good'
                          ? 'text-emerald-700'
                          : slot.quality === 'caution'
                            ? 'text-red-700'
                            : 'text-sky-700'
                      }`}>
                        {slot.quality}
                      </span>
                      <span className="text-stone-600">{slot.ruler}</span>
                    </div>
                  );
                })}
              </div>
            </section>

            <section className="mt-8 grid gap-5 lg:grid-cols-[1.1fr_0.9fr]">
              <article className="rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold text-stone-900">How to read the table</h2>
                <ul className="mt-4 space-y-3 text-sm leading-7 text-stone-600">
                  <li>- Amrit, Shubh, and Labh are generally treated as stronger windows for fresh starts and constructive actions.</li>
                  <li>- Char is more neutral and often used for movement, travel, or routine tasks.</li>
                  <li>- Rog, Kaal, and Udveg are cautionary windows where many practitioners avoid major beginnings.</li>
                  <li>- The exact slot timings depend on local sunrise and sunset, which is why each city gets its own calculation.</li>
                </ul>
              </article>

              <article className="rounded-[1.75rem] border border-gold/15 bg-white/82 p-6 shadow-sm">
                <h2 className="font-playfair text-2xl font-semibold text-stone-900">Related tools</h2>
                <div className="mt-4 flex flex-col gap-3">
                  <Link
                    to={`/panchang/${citySlug}/${data.date}`}
                    className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                  >
                    Open full Panchang for this city
                  </Link>
                  <Link
                    to="/hora"
                    className="rounded-full border border-gold/20 bg-gold/10 px-4 py-2 text-sm font-semibold text-gold transition hover:bg-gold hover:text-stone-950"
                  >
                    View Hora Today
                  </Link>
                </div>
              </article>
            </section>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default ChoghadiyaPage;
