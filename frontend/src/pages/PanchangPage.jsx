import React, { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { SEO } from '../components/SEO';
import { Card } from '../components/ui/card';
import { Calendar, Sun, Moon, Star, Sparkles, ChevronLeft, ChevronRight, Zap, MapPin, Globe, ChevronDown } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api/panchang`;
const SITE = 'https://everydayhoroscope.in';
const OG_IMAGE = `${SITE}/og-image.png`;
const LOC_STORAGE_KEY = 'panchang_location_slug';
const DEFAULT_SLUG = 'new-delhi-india';

const QUALITY_STYLES = {
  good:    { badge: 'bg-green-100 text-green-800' },
  neutral: { badge: 'bg-amber-100 text-amber-800' },
  caution: { badge: 'bg-red-100 text-red-800' },
};

const TYPE_META = {
  daily:      { title: "Today's Panchang",      icon: Sun,      desc: 'Complete Vedic almanac — Tithi, Nakshatra, Yoga, Karana, Sunrise & Sunset' },
  tomorrow:   { title: "Tomorrow's Panchang",   icon: Sun,      desc: 'Complete Vedic almanac for tomorrow — Tithi, Nakshatra, Yoga, Karana' },
  tithi:      { title: 'Tithi — Lunar Day',      icon: Moon,     desc: "Today's Tithi (lunar day) with Paksha phase and timing" },
  choghadiya: { title: 'Choghadiya',             icon: Zap,      desc: 'Auspicious and inauspicious time periods of the day' },
  calendar:   { title: 'Panchang Calendar',      icon: Calendar, desc: 'Monthly Hindu calendar with Tithi and observances' },
  festivals:  { title: 'Festivals & Vrats',      icon: Sparkles, desc: 'Upcoming Hindu festivals and vrat dates' },
};

const ALIAS = {
  today:      'daily',
  tomorrow:   'tomorrow',
  tithi:      'tithi',
  choghadiya: 'choghadiya',
  muhurat:    'daily',
  nakshatra:  'daily',
  rahukaal:   'daily',
};

// ─── Time formatting — respects location timezone ─────────────────────────
function makeFormatTime(tz) {
  return function formatTime(iso) {
    if (!iso) return '--';
    try {
      return new Date(iso).toLocaleTimeString('en-IN', {
        hour: '2-digit', minute: '2-digit', hour12: true,
        timeZone: tz || 'Asia/Kolkata',
      });
    } catch { return iso.slice(11, 16); }
  };
}

function formatDate(iso, tz) {
  if (!iso) return '';
  try {
    return new Date(iso).toLocaleDateString('en-IN', {
      weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
      timeZone: tz || 'Asia/Kolkata',
    });
  } catch { return iso; }
}

function getTodayInTZ(tz) {
  try {
    const now = new Date();
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(now);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    // IST fallback
    const ist = new Date(new Date().getTime() + 5.5 * 60 * 60 * 1000);
    return ist.toISOString().slice(0, 10);
  }
}

function getTomorrowInTZ(tz) {
  try {
    const tomorrow = new Date(new Date().getTime() + 86400000);
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(tomorrow);
    const map = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${map.year}-${map.month}-${map.day}`;
  } catch {
    const ist = new Date(new Date().getTime() + 5.5 * 60 * 60 * 1000);
    ist.setDate(ist.getDate() + 1);
    return ist.toISOString().slice(0, 10);
  }
}

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];

function humanDate(isoDate, tz) {
  if (!isoDate) return '';
  const [y, m, d] = isoDate.split('-');
  try {
    const weekday = new Date(`${isoDate}T12:00:00Z`).toLocaleDateString('en-IN', { weekday: 'long', timeZone: tz || 'Asia/Kolkata' });
    return `${weekday}, ${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
  } catch {
    return `${parseInt(d)} ${MONTH_NAMES[parseInt(m) - 1]} ${y}`;
  }
}

// ─── Location picker component ─────────────────────────────────────────────
function LocationPicker({ selectedSlug, onSelect }) {
  const [locations, setLocations] = useState([]);
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const ref = useRef(null);

  useEffect(() => {
    axios.get(`${API}/locations`)
      .then(r => setLocations(r.data))
      .catch(() => {});
  }, []);

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, []);

  const selected = locations.find(l => l.slug === selectedSlug);
  const countries = [...new Set(locations.map(l => l.country))];

  const filtered = search.trim()
    ? locations.filter(l =>
        l.label.toLowerCase().includes(search.toLowerCase()) ||
        l.country.toLowerCase().includes(search.toLowerCase())
      )
    : locations;

  const grouped = countries.reduce((acc, c) => {
    const locs = filtered.filter(l => l.country === c);
    if (locs.length) acc[c] = locs;
    return acc;
  }, {});

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gold/30 bg-gold/5 text-xs font-semibold text-gold hover:bg-gold/10 transition-colors"
      >
        <MapPin className="h-3 w-3" />
        <span>{selected ? `${selected.label}, ${selected.country}` : 'Select location'}</span>
        <ChevronDown className={`h-3 w-3 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-72 max-h-80 overflow-hidden rounded-xl border border-border bg-background shadow-xl z-50 flex flex-col">
          {/* Search */}
          <div className="p-2 border-b border-border">
            <input
              autoFocus
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search city or country…"
              className="w-full px-3 py-1.5 text-xs rounded-lg border border-border bg-muted/30 focus:outline-none focus:border-gold/50"
            />
          </div>
          {/* List */}
          <div className="overflow-y-auto flex-1">
            {Object.entries(grouped).map(([country, locs]) => (
              <div key={country}>
                <div className="flex items-center gap-1.5 px-3 py-1.5 bg-muted/30">
                  <Globe className="h-3 w-3 text-muted-foreground" />
                  <p className="text-[10px] font-bold uppercase tracking-widest text-muted-foreground">{country}</p>
                </div>
                {locs.map(loc => (
                  <button
                    key={loc.slug}
                    onClick={() => { onSelect(loc.slug); setOpen(false); setSearch(''); }}
                    className={`w-full text-left px-4 py-2 text-xs hover:bg-gold/10 transition-colors flex items-center justify-between ${
                      loc.slug === selectedSlug ? 'text-gold font-semibold bg-gold/5' : 'text-foreground'
                    }`}
                  >
                    <span>{loc.label}</span>
                    {loc.slug === selectedSlug && <span className="text-gold">✓</span>}
                  </button>
                ))}
              </div>
            ))}
            {Object.keys(grouped).length === 0 && (
              <p className="text-xs text-muted-foreground text-center py-6">No locations found</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── SEO helpers ───────────────────────────────────────────────────────────
function webPageSchema({ name, description, url, datePublished }) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name, description, url,
    inLanguage: 'en-IN',
    ...(datePublished ? { datePublished } : {}),
    isPartOf: { '@type': 'WebSite', name: 'Everyday Horoscope', url: SITE },
    provider: { '@type': 'Organization', name: 'Everyday Horoscope', url: SITE },
  };
}

function buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }) {
  const tz = locationTZ || 'Asia/Kolkata';
  const todayISO    = getTodayInTZ(tz);
  const tomorrowISO = getTomorrowInTZ(tz);
  switch (view) {
    case 'daily': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Today's Panchang — ${humanToday}`;
      const description = `Free daily Panchang for ${humanToday}. Get today's Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Gulika Kaal, Abhijit Muhurta, Sunrise & Sunset — powered by Vedic astronomy.`;
      const url = `${SITE}/panchang/today`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'tomorrow': {
      const humanTomorrow = humanDate(tomorrowISO, tz);
      const title = `Tomorrow's Panchang — ${humanTomorrow}`;
      const description = `Panchang for ${humanTomorrow}. Plan your day with tomorrow's Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Gulika Kaal, Abhijit Muhurta, and Sunrise & Sunset.`;
      const url = `${SITE}/panchang/tomorrow`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: tomorrowISO }) };
    }
    case 'tithi': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Today's Tithi (Lunar Day) — ${humanToday}`;
      const description = `What is today's Tithi? Find the current Tithi (lunar day), Paksha phase, Nakshatra, and Moon sign for ${humanToday} — accurate Vedic Panchang data.`;
      const url = `${SITE}/panchang/tithi`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'choghadiya': {
      const humanToday = humanDate(todayISO, tz);
      const title = `Choghadiya Today — ${humanToday}`;
      const description = `Today's Choghadiya table for ${humanToday}. Find auspicious and inauspicious time slots for starting new work, travel, and muhurat planning.`;
      const url = `${SITE}/panchang/choghadiya`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: todayISO }) };
    }
    case 'festivals': {
      const year = new Date().getFullYear();
      const title = `Hindu Festivals & Vrats ${year} — Complete Calendar`;
      const description = `Full list of Hindu festivals, vrats, and religious observances for ${year}. Includes Ekadashi, Purnima, Amavasya, and major festivals with exact dates.`;
      const url = `${SITE}/panchang/festivals`;
      let schema;
      if (festivalData?.items?.length) {
        schema = { '@context': 'https://schema.org', '@type': 'ItemList', name: title, description, url, numberOfItems: festivalData.items.length,
          itemListElement: festivalData.items.slice(0, 20).map((item, idx) => ({ '@type': 'ListItem', position: idx + 1, name: item.name, description: item.summary || item.name, url: `${SITE}/panchang/date/${item.date}` })) };
      } else {
        schema = webPageSchema({ name: title, description, url });
      }
      return { title, description, url, schema };
    }
    case 'calendar': {
      const y = calYear || new Date().getFullYear();
      const mo = calMonth || (new Date().getMonth() + 1);
      const monthLabel = `${MONTH_NAMES[mo - 1]} ${y}`;
      const title = `Panchang Calendar — ${monthLabel}`;
      const description = `Hindu Panchang calendar for ${monthLabel}. View daily Tithi, Nakshatra, festivals, and Vedic observances for every day of ${monthLabel}.`;
      const url = `${SITE}/panchang/calendar/${y}/${mo}`;
      return { title, description, url, schema: webPageSchema({ name: title, description, url, datePublished: `${y}-${String(mo).padStart(2,'0')}-01` }) };
    }
    case 'date': {
      if (!dateValue) return null;
      const humanDay = humanDate(dateValue, tz);
      let title, description;
      if (panchangData?.panchang) {
        const { tithi, nakshatra, yoga } = panchangData.panchang;
        title = `Panchang ${humanDay} — ${tithi.name}, ${nakshatra.name} Nakshatra`;
        description = `Panchang for ${humanDay}: Tithi — ${tithi.name} (${panchangData.panchang.paksha} Paksha), Nakshatra — ${nakshatra.name}, Yoga — ${yoga.name}.`;
      } else {
        title = `Panchang — ${humanDay}`;
        description = `Complete Vedic Panchang for ${humanDay}. Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, Gulika Kaal, Abhijit Muhurta, Sunrise & Sunset.`;
      }
      const url = `${SITE}/panchang/date/${dateValue}`;
      const [y, mo] = dateValue.split('-');
      const breadcrumb = { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Panchang', item: `${SITE}/panchang/today` },
        { '@type': 'ListItem', position: 2, name: `${MONTH_NAMES[parseInt(mo)-1]} ${y}`, item: `${SITE}/panchang/calendar/${y}/${parseInt(mo)}` },
        { '@type': 'ListItem', position: 3, name: humanDay, item: url },
      ]};
      return { title, description, url, schema: [breadcrumb, webPageSchema({ name: title, description, url, datePublished: dateValue })] };
    }
    default: return null;
  }
}

function PanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }) {
  const seo = useMemo(
    () => buildPanchangSEO({ view, calYear, calMonth, dateValue, festivalData, panchangData, locationTZ }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [view, calYear, calMonth, dateValue, festivalData?.items?.length, panchangData?.panchang?.tithi?.name, locationTZ]
  );
  if (!seo) return null;
  const schemas = Array.isArray(seo.schema) ? seo.schema : seo.schema ? [seo.schema] : [];
  return <SEO title={seo.title} description={seo.description} url={seo.url} image={OG_IMAGE} type="website" schema={schemas.length === 1 ? schemas[0] : schemas.length > 1 ? schemas : null} />;
}

// ─── SEO body-copy blocks ──────────────────────────────────────────────────
function PanchangDailySEOContent() {
  return (
    <div className="mt-12 space-y-8 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Panchang?</h2>
        <p>Panchang (also written as Panchangam or Panchāṅga) is the traditional Hindu almanac used across India for over 1,800 years. The word means "five limbs" — referring to Tithi (lunar day), Vara (weekday), Nakshatra (lunar mansion), Yoga, and Karana. Together these five elements describe the quality and character of each day according to Vedic astronomy.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Rahu Kaal?</h2>
        <p>Rahu Kaal is an inauspicious period each day governed by Rahu, the shadow planet. The traditional Vedic system divides daylight into 8 equal Kaals. Rahu Kaal occupies one of these slots, with the exact slot shifting each day of the week. Important activities like travel, business deals, or ceremonies are generally avoided during this window.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">What is Abhijit Muhurta?</h2>
        <p>Abhijit Muhurta is the most auspicious 48-minute window of the day, centred on solar noon. It is considered so powerful in Vedic tradition that it overrides most negative planetary influences. Starting any new work, signing agreements, or making important decisions during Abhijit Muhurta is highly recommended — except on Wednesdays.</p>
      </div>
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Tithi, Nakshatra, Yoga and Karana explained</h2>
        <p><strong className="text-foreground">Tithi</strong> is the lunar day — calculated from the angular distance between the Sun and Moon. <strong className="text-foreground">Nakshatra</strong> is the lunar mansion — the Moon's position among the 27 asterisms of the zodiac. <strong className="text-foreground">Yoga</strong> is computed from the sum of Sun and Moon longitudes. <strong className="text-foreground">Karana</strong> is half a Tithi and changes twice daily.</p>
      </div>
    </div>
  );
}

function PanchangTithiSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Understanding Tithi — the Vedic Lunar Day</h2><p>A Tithi is not a solar calendar day — it is a lunar day defined by the Moon moving 12° away from the Sun. There are 30 Tithis in a complete lunar cycle, numbered 1 (Pratipada) through 15 (Purnima or Amavasya).</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Shukla Paksha and Krishna Paksha</h2><p>Shukla Paksha is the bright fortnight from Amavasya to Purnima — associated with growth and auspicious beginnings. Krishna Paksha is the dark fortnight from Purnima to Amavasya — associated with completion and ancestral rites.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Important Tithis and their significance</h2><p>Ekadashi (11th Tithi) is observed as a fast day dedicated to Lord Vishnu. Purnima (full moon) is ideal for spiritual practices. Amavasya (new moon) is observed for ancestral rites. Pradosh (13th Tithi) is sacred to Lord Shiva.</p></div>
    </div>
  );
}

function PanchangChoghadiyaSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">What is Choghadiya?</h2><p>Choghadiya is a Vedic time-keeping system that divides the day and night into eight equal segments. Each is classified by its ruling planet, giving it one of seven qualities: Amrit (excellent), Shubh (auspicious), Labh (profitable), Char (good for travel), Udveg, Kaal, or Rog (inauspicious).</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">How to use Choghadiya for muhurat planning</h2><p>For starting a new business, signing a contract, or travelling, look for an Amrit or Shubh Choghadiya window. Udveg, Kaal, and Rog periods are traditionally avoided for new beginnings.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Choghadiya vs Rahu Kaal — what's the difference?</h2><p>Rahu Kaal is a single inauspicious window each day, whereas Choghadiya provides a full table of all time segments with their qualities — a more granular picture for muhurat planning.</p></div>
    </div>
  );
}

function PanchangFestivalsSEOContent() {
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Hindu Festivals and the Vedic Calendar</h2><p>Hindu festivals are not fixed to the Gregorian calendar — they are computed from Tithi, Nakshatra, and planetary positions each year. Our festival dates are calculated directly from Vedic astronomy using the Swiss Ephemeris for maximum accuracy.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">Major Hindu festivals and their Panchang basis</h2><p><strong className="text-foreground">Diwali</strong> falls on Amavasya of Kartika. <strong className="text-foreground">Holi</strong> is on Purnima of Phalguna. <strong className="text-foreground">Janmashtami</strong> is on Ashtami Krishna Paksha of Shravana. <strong className="text-foreground">Rama Navami</strong> is on Navami Shukla Paksha of Chaitra.</p></div>
    </div>
  );
}

function PanchangCalendarSEOContent({ calYear, calMonth }) {
  const monthName = MONTH_NAMES[(calMonth || 1) - 1];
  const year = calYear || new Date().getFullYear();
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div><h2 className="text-base font-semibold text-foreground mb-2">Hindu Panchang Calendar — {monthName} {year}</h2><p>This month view shows the Tithi for every day of {monthName} {year}, along with festivals and Vedic observances. Tap any date to access its complete Panchang details.</p></div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">How to read the Panchang Calendar</h2><p>Each cell shows the Tithi name for that day (calculated at sunrise). A gold dot indicates a festival or Vrat observance. The calendar follows the Amanta lunar month system.</p></div>
    </div>
  );
}

function PanchangDateSEOContent({ panchangData }) {
  if (!panchangData?.panchang) return null;
  const { tithi, nakshatra, yoga, karana, paksha, lunar_month, sun_sign, moon_sign } = panchangData.panchang;
  const { sunrise, sunset } = panchangData.summary || {};
  return (
    <div className="mt-12 space-y-6 text-sm text-muted-foreground border-t border-border pt-8">
      <div>
        <h2 className="text-base font-semibold text-foreground mb-2">Full Panchang Details</h2>
        <p>Tithi: <strong className="text-foreground">{tithi.name}</strong> in <strong className="text-foreground">{paksha} Paksha</strong> of <strong className="text-foreground">{lunar_month}</strong>. Moon in <strong className="text-foreground">{nakshatra.name}</strong> Nakshatra ({moon_sign} Rashi). Sun in <strong className="text-foreground">{sun_sign}</strong>. Yoga: <strong className="text-foreground">{yoga.name}</strong>. Karana: <strong className="text-foreground">{karana.name}</strong>.</p>
        {sunrise && sunset && <p className="mt-2">Sunrise: <strong className="text-foreground">{sunrise}</strong> · Sunset: <strong className="text-foreground">{sunset}</strong> (local time).</p>}
      </div>
      <div><h2 className="text-base font-semibold text-foreground mb-2">About {nakshatra.name} Nakshatra</h2><p>The Moon in {nakshatra.name} shapes the emotional quality of this day. Each of the 27 Nakshatras carries a distinct deity, symbol, and set of qualities that influence the nature of any activity begun under them.</p></div>
    </div>
  );
}

// ─── Views ──────────────────────────────────────────────────────────────────

function PanchangDailyView({ dayOffset = 0, locationSlug, locationTZ, onDataLoad }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const formatTime = useMemo(() => makeFormatTime(locationTZ), [locationTZ]);

  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    const tz = locationTZ || 'Asia/Kolkata';
    const dateStr = dayOffset === 1 ? getTomorrowInTZ(tz) : getTodayInTZ(tz);
    const params = { location_slug: locationSlug, date: dateStr };
    axios.get(`${API}/daily`, { params })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setError('Failed to load Panchang data. Please try again.'))
      .finally(() => setLoading(false));
  }, [dayOffset, locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) return <div className="space-y-4">{[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error) return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data) return null;

  const { summary, panchang, day_quality_windows, observances } = data;
  const locTZ = data.location?.timezone || locationTZ || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00', locTZ)}</span>
        </div>
        <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
      </div>
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi',      value: panchang.tithi.name,     sub: panchang.paksha + ' Paksha' + (panchang.tithi.end ? ' · until ' + fmtTime(panchang.tithi.end) : '') },
            { label: 'Nakshatra',  value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign + (panchang.nakshatra.end ? ' · until ' + fmtTime(panchang.nakshatra.end) : '') },
            { label: 'Yoga',       value: panchang.yoga.name,      sub: panchang.yoga.end ? 'Until ' + fmtTime(panchang.yoga.end) : '' },
            { label: 'Karana',     value: panchang.karana.name,    sub: panchang.karana.end ? 'Until ' + fmtTime(panchang.karana.end) : '' },
            { label: 'Vara (Day)', value: summary.weekday,          sub: panchang.samvat },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[200px]">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>
      <div className="grid grid-cols-2 gap-3">
        <Card className="p-4 border border-gold/20 text-center">
          <Sun className="h-5 w-5 text-amber-500 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunrise</p>
          <p className="font-semibold text-lg">{summary.sunrise}</p>
          <p className="text-xs text-muted-foreground mt-1">Sun in {panchang.sun_sign}</p>
        </Card>
        <Card className="p-4 border border-gold/20 text-center">
          <Moon className="h-5 w-5 text-blue-400 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunset</p>
          <p className="font-semibold text-lg">{summary.sunset}</p>
          <p className="text-xs text-muted-foreground mt-1">Moon in {panchang.moon_sign}</p>
        </Card>
      </div>
      {day_quality_windows?.length > 0 && (
        <Card className="border border-gold/20 overflow-hidden">
          <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Timing Windows</p>
          </div>
          <div className="divide-y divide-border">
            {day_quality_windows.map(w => (
              <div key={w.label} className="flex items-center justify-between px-5 py-3">
                <div className="flex items-center gap-3">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${(QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral).badge}`}>{w.quality}</span>
                  <span className="text-sm font-medium">{w.label}</span>
                </div>
                <span className="text-xs text-muted-foreground">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
      {observances?.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Today's Observances</p>
          <div className="space-y-2">
            {observances.map(o => (
              <div key={o.slug} className="flex items-start gap-3">
                <Star className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{o.name}</p>
                  <p className="text-xs text-muted-foreground">{o.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      <div className="flex gap-3">
        <Link to={`/panchang/calendar/${new Date().getFullYear()}/${new Date().getMonth() + 1}`}
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Calendar className="h-4 w-4" /> Monthly Calendar
        </Link>
        <Link to="/panchang/festivals"
          className="flex-1 flex items-center justify-center gap-2 py-3 border border-gold/30 rounded-xl text-sm font-medium text-gold hover:bg-gold/5 transition-colors">
          <Sparkles className="h-4 w-4" /> Festivals &amp; Vrats
        </Link>
      </div>
      <PanchangDailySEOContent />
    </div>
  );
}

function PanchangTithiView({ locationSlug }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]);
  if (loading) return <div className="space-y-4">{[...Array(3)].map((_, i) => <div key={i} className="h-20 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data) return <p className="text-center text-muted-foreground py-12">Failed to load Tithi data</p>;
  const { panchang, summary } = data;
  const fmtTime = makeFormatTime(data.location?.timezone);
  return (
    <div className="space-y-6">
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Today's Tithi</p>
        </div>
        <div className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-3xl font-playfair font-bold">{panchang.tithi.name}</p>
              <p className="text-muted-foreground">{panchang.paksha} Paksha</p>
            </div>
            <Moon className="h-10 w-10 text-gold/60" />
          </div>
          {panchang.tithi.end && (
            <p className="text-sm text-muted-foreground border-t border-border pt-3">
              Ends at <span className="font-semibold text-foreground">{fmtTime(panchang.tithi.end)}</span>
            </p>
          )}
        </div>
      </Card>
      <Card className="border border-gold/20 p-5">
        <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Moon Position</p>
        <div className="grid grid-cols-2 gap-4">
          <div><p className="text-xs text-muted-foreground">Moon Sign</p><p className="font-semibold">{panchang.moon_sign}</p></div>
          <div><p className="text-xs text-muted-foreground">Nakshatra</p><p className="font-semibold">{panchang.nakshatra.name}</p></div>
          <div><p className="text-xs text-muted-foreground">Weekday</p><p className="font-semibold">{summary.weekday}</p></div>
          <div><p className="text-xs text-muted-foreground">Samvat</p><p className="font-semibold text-xs">{panchang.samvat}</p></div>
        </div>
      </Card>
      <PanchangTithiSEOContent />
    </div>
  );
}

function PanchangChoghadiyaView({ locationSlug }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    axios.get(`${API}/daily`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [locationSlug]);
  if (loading) return <div className="space-y-3">{[...Array(8)].map((_, i) => <div key={i} className="h-12 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data) return <p className="text-center text-muted-foreground py-12">Failed to load Choghadiya data</p>;
  const windows = data.day_quality_windows || [];
  const now = new Date();
  const fmtTime = makeFormatTime(data.location?.timezone);
  return (
    <div className="space-y-4">
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Today's Choghadiya</p>
        </div>
        {windows.length === 0
          ? <p className="text-center text-muted-foreground py-8">No timing data available for today</p>
          : <div className="divide-y divide-border">
              {windows.map((w, i) => {
                const isCurrent = now >= new Date(w.start) && now <= new Date(w.end);
                return (
                  <div key={i} className={`flex items-center justify-between px-5 py-3 ${isCurrent ? 'bg-gold/5' : ''}`}>
                    <div className="flex items-center gap-3">
                      {isCurrent && <span className="w-2 h-2 rounded-full bg-green-500 flex-shrink-0" />}
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${(QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral).badge}`}>{w.quality}</span>
                      <span className="text-sm font-medium">{w.label}</span>
                      {isCurrent && <span className="text-xs text-green-600 font-semibold">Current</span>}
                    </div>
                    <span className="text-xs text-muted-foreground">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
                  </div>
                );
              })}
            </div>
        }
      </Card>
      <p className="text-xs text-muted-foreground text-center">Times shown in local time for {data.location?.label}</p>
      <PanchangChoghadiyaSEOContent />
    </div>
  );
}

function PanchangCalendarView({ year, month, locationSlug }) {
  const navigate = useNavigate();
  const today = new Date();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    setLoading(true); setData(null);
    axios.get(`${API}/calendar/${year}/${month}`, { params: { location_slug: locationSlug } })
      .then(r => setData(r.data)).catch(() => setData(null)).finally(() => setLoading(false));
  }, [year, month, locationSlug]);
  const prevMonth = month === 1 ? { y: year - 1, m: 12 } : { y: year, m: month - 1 };
  const nextMonth = month === 12 ? { y: year + 1, m: 1 } : { y: year, m: month + 1 };
  const todayISO = today.toISOString().slice(0, 10);
  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <button onClick={() => navigate(`/panchang/calendar/${prevMonth.y}/${prevMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors"><ChevronLeft className="h-5 w-5 text-gold" /></button>
        <h2 className="font-playfair font-semibold text-xl">{data?.month_label || `${month}/${year}`}</h2>
        <button onClick={() => navigate(`/panchang/calendar/${nextMonth.y}/${nextMonth.m}`)} className="p-2 hover:bg-gold/10 rounded-lg transition-colors"><ChevronRight className="h-5 w-5 text-gold" /></button>
      </div>
      {loading ? (
        <div className="grid grid-cols-7 gap-1">{[...Array(35)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>
      ) : data ? (
        <div className="space-y-1">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].map(d => <div key={d} className="text-center text-xs font-semibold text-muted-foreground py-1">{d}</div>)}
          </div>
          {(() => {
            const firstDay = new Date(year, month - 1, 1).getDay();
            const cells = [...Array(firstDay).fill(null), ...data.days];
            const rows = [];
            for (let i = 0; i < cells.length; i += 7) rows.push(cells.slice(i, i + 7));
            return rows.map((row, ri) => (
              <div key={ri} className="grid grid-cols-7 gap-1">
                {row.map((day, ci) => {
                  if (!day) return <div key={ci} />;
                  const isToday = day.date === todayISO;
                  const hasFestival = day.observances?.length > 0;
                  return (
                    <button key={day.date} onClick={() => navigate(`/panchang/date/${day.date}`)}
                      className={`p-1.5 rounded-lg border text-center w-full transition-all hover:border-gold hover:bg-gold/10 hover:shadow-sm ${isToday ? 'border-gold bg-gold/10' : 'border-border'}`}>
                      <p className={`text-sm font-semibold ${isToday ? 'text-gold' : ''}`}>{day.day}</p>
                      <p className="text-[9px] text-muted-foreground leading-tight mt-0.5 truncate">{day.tithi.split(' ')[1] || day.tithi}</p>
                      {hasFestival && <div className="w-1 h-1 bg-gold rounded-full mx-auto mt-1" />}
                    </button>
                  );
                })}
              </div>
            ));
          })()}
        </div>
      ) : <p className="text-center text-muted-foreground py-12">Failed to load calendar</p>}
      <p className="text-xs text-center text-muted-foreground">Tap any date to view full Panchang details</p>
      <PanchangCalendarSEOContent calYear={year} calMonth={month} />
    </div>
  );
}

function PanchangFestivalsView({ locationSlug, onDataLoad }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const year = new Date().getFullYear();
  useEffect(() => {
    axios.get(`${API}/festivals`, { params: { year, location_slug: locationSlug } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-3">{[...Array(8)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (!data?.items?.length) return <p className="text-center text-muted-foreground py-12">No festivals found</p>;
  const grouped = data.items.reduce((acc, item) => { const m = item.date.slice(0,7); if (!acc[m]) acc[m]=[]; acc[m].push(item); return acc; }, {});
  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([m, items]) => (
        <div key={m}>
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">
            {new Date(m + '-01').toLocaleDateString('en-IN', { month: 'long', year: 'numeric' })}
          </p>
          <div className="space-y-2">
            {items.map(item => (
              <div key={item.slug + item.date} className="flex items-start gap-4 p-4 border border-gold/20 rounded-xl bg-gold/5">
                <div className="text-center min-w-[40px]">
                  <p className="text-xl font-playfair font-bold text-gold">{new Date(item.date + 'T00:00:00').getDate()}</p>
                  <p className="text-[10px] text-muted-foreground uppercase">{new Date(item.date + 'T00:00:00').toLocaleDateString('en-IN', { weekday: 'short' })}</p>
                </div>
                <div>
                  <span className={`text-[10px] font-semibold uppercase tracking-wide px-2 py-0.5 rounded-full ${item.observance_type === 'festival' ? 'bg-amber-100 text-amber-800' : item.observance_type === 'vrat' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>{item.observance_type}</span>
                  <p className="font-semibold text-sm mt-1">{item.name}</p>
                  <p className="text-xs text-muted-foreground">{item.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
      <PanchangFestivalsSEOContent />
    </div>
  );
}

function PanchangDateView({ dateStr, locationSlug, onDataLoad }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    setLoading(true); setError(null); setData(null);
    axios.get(`${API}/date/${dateStr}`, { params: { location_slug: locationSlug } })
      .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
      .catch(() => {
        axios.get(`${API}/daily`, { params: { date: dateStr, location_slug: locationSlug } })
          .then(r => { setData(r.data); if (onDataLoad) onDataLoad(r.data); })
          .catch(() => setError('Failed to load Panchang data.'))
          .finally(() => setLoading(false));
      })
      .finally(() => setLoading(false));
  }, [dateStr, locationSlug]); // eslint-disable-line react-hooks/exhaustive-deps
  if (loading) return <div className="space-y-4">{[...Array(5)].map((_, i) => <div key={i} className="h-16 bg-gold/5 rounded-lg animate-pulse" />)}</div>;
  if (error) return <p className="text-center text-muted-foreground py-12">{error}</p>;
  if (!data) return null;
  const { summary, panchang, day_quality_windows, observances } = data;
  const locTZ = data.location?.timezone || 'Asia/Kolkata';
  const fmtTime = makeFormatTime(locTZ);
  const [y, mo] = dateStr.split('-');
  return (
    <div className="space-y-6">
      <button onClick={() => navigate(`/panchang/calendar/${y}/${parseInt(mo)}`)} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-gold transition-colors">
        <ChevronLeft className="h-4 w-4" /> Back to Calendar
      </button>
      <div className="flex items-center justify-between px-6 py-4 bg-gold/5 border border-gold/20 rounded-xl">
        <div className="flex items-center gap-3">
          <Sun className="h-5 w-5 text-gold" />
          <span className="font-playfair font-semibold text-lg">{formatDate(data.date + 'T00:00:00', locTZ)}</span>
        </div>
        <span className="text-xs text-muted-foreground">{data.location?.label}, {data.location?.country}</span>
      </div>
      <Card className="border border-gold/20 overflow-hidden">
        <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold">Panch Anga — Five Limbs</p>
        </div>
        <div className="divide-y divide-border">
          {[
            { label: 'Tithi',      value: panchang.tithi.name,     sub: panchang.paksha + ' Paksha' },
            { label: 'Nakshatra',  value: panchang.nakshatra.name, sub: 'Moon in ' + panchang.moon_sign },
            { label: 'Yoga',       value: panchang.yoga.name,      sub: '' },
            { label: 'Karana',     value: panchang.karana.name,    sub: '' },
            { label: 'Vara (Day)', value: summary.weekday,          sub: panchang.samvat },
          ].map(item => (
            <div key={item.label} className="flex items-center justify-between px-5 py-4">
              <div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide mb-0.5">{item.label}</p>
                <p className="font-medium text-sm">{item.value}</p>
              </div>
              {item.sub && <p className="text-xs text-muted-foreground text-right max-w-[200px]">{item.sub}</p>}
            </div>
          ))}
        </div>
      </Card>
      <div className="grid grid-cols-2 gap-3">
        <Card className="p-4 border border-gold/20 text-center">
          <Sun className="h-5 w-5 text-amber-500 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunrise</p>
          <p className="font-semibold text-lg">{summary.sunrise}</p>
        </Card>
        <Card className="p-4 border border-gold/20 text-center">
          <Moon className="h-5 w-5 text-blue-400 mx-auto mb-2" />
          <p className="text-xs text-muted-foreground uppercase tracking-wide">Sunset</p>
          <p className="font-semibold text-lg">{summary.sunset}</p>
        </Card>
      </div>
      {day_quality_windows?.length > 0 && (
        <Card className="border border-gold/20 overflow-hidden">
          <div className="px-5 py-3 bg-gold/5 border-b border-gold/20">
            <p className="text-xs font-semibold uppercase tracking-widest text-gold">Timing Windows</p>
          </div>
          <div className="divide-y divide-border">
            {day_quality_windows.map(w => (
              <div key={w.label} className="flex items-center justify-between px-5 py-3">
                <div className="flex items-center gap-3">
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${(QUALITY_STYLES[w.quality] || QUALITY_STYLES.neutral).badge}`}>{w.quality}</span>
                  <span className="text-sm font-medium">{w.label}</span>
                </div>
                <span className="text-xs text-muted-foreground">{fmtTime(w.start)} — {fmtTime(w.end)}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
      {observances?.length > 0 && (
        <Card className="border border-gold/20 p-5">
          <p className="text-xs font-semibold uppercase tracking-widest text-gold mb-3">Observances</p>
          <div className="space-y-2">
            {observances.map(o => (
              <div key={o.slug} className="flex items-start gap-3">
                <Star className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" />
                <div>
                  <p className="text-sm font-medium">{o.name}</p>
                  <p className="text-xs text-muted-foreground">{o.summary}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}
      <PanchangDateSEOContent panchangData={data} />
    </div>
  );
}

// ─── Main page ─────────────────────────────────────────────────────────────
export const PanchangPage = () => {
  const { type: rawType = 'daily', year: yearParam, month: monthParam, dateValue } = useParams();
  const resolvedType = ALIAS[rawType] || rawType;
  const isCalendar = resolvedType === 'calendar' || (yearParam && monthParam && !dateValue);
  const isDateView = !!dateValue;
  const activeView = isDateView ? 'date' : isCalendar ? 'calendar' : (resolvedType || 'daily');
  const today = new Date();
  const calYear  = parseInt(yearParam)  || today.getFullYear();
  const calMonth = parseInt(monthParam) || (today.getMonth() + 1);

  // Location state — persisted in localStorage
  const [locationSlug, setLocationSlug] = useState(
    () => localStorage.getItem(LOC_STORAGE_KEY) || DEFAULT_SLUG
  );
  const [locationTZ, setLocationTZ] = useState('Asia/Kolkata');

  const handleLocationSelect = useCallback((slug) => {
    setLocationSlug(slug);
    localStorage.setItem(LOC_STORAGE_KEY, slug);
  }, []);

  // Fetch location TZ whenever slug changes (so SEO dates are correct)
  useEffect(() => {
    axios.get(`${API}/locations`)
      .then(r => {
        const loc = r.data.find(l => l.slug === locationSlug);
        if (loc?.timezone) setLocationTZ(loc.timezone);
      })
      .catch(() => {});
  }, [locationSlug]);

  const [festivalData, setFestivalData] = useState(null);
  const [panchangData, setPanchangData] = useState(null);

  useEffect(() => {
    setFestivalData(null);
    setPanchangData(null);
  }, [activeView, dateValue, calYear, calMonth, locationSlug]);

  const config = isDateView
    ? { title: 'Panchang Details', icon: Calendar, desc: 'Complete Vedic almanac for the selected date' }
    : (TYPE_META[activeView] || TYPE_META.daily);

  const subNavItems = [
    { key: 'daily',       label: 'Today',      icon: Sun,      path: '/panchang/today' },
    { key: 'tomorrow',    label: 'Tomorrow',   icon: Sun,      path: '/panchang/tomorrow' },
    { key: 'tithi',       label: 'Tithi',      icon: Moon,     path: '/panchang/tithi' },
    { key: 'choghadiya',  label: 'Choghadiya', icon: Zap,      path: '/panchang/choghadiya' },
    { key: 'calendar',    label: 'Calendar',   icon: Calendar, path: `/panchang/calendar/${today.getFullYear()}/${today.getMonth() + 1}` },
    { key: 'festivals',   label: 'Festivals',  icon: Sparkles, path: '/panchang/festivals' },
  ];

  const subNavActive = activeView === 'date' ? 'calendar' : activeView;

  return (
    <div className="max-w-3xl mx-auto px-4 py-10 pb-24 lg:pb-10">
      <PanchangSEO
        view={activeView}
        calYear={calYear}
        calMonth={calMonth}
        dateValue={dateValue}
        festivalData={festivalData}
        panchangData={panchangData}
        locationTZ={locationTZ}
      />
      <div className="text-center mb-6">
        <div className="inline-flex items-center gap-2 border border-gold/30 bg-gold/5 text-gold text-xs font-semibold uppercase tracking-widest px-4 py-1.5 rounded-full mb-4">
          <Calendar className="h-3 w-3" /> Vedic Panchang
        </div>
        <h1 className="text-3xl font-playfair font-semibold mb-2">{config.title}</h1>
        <p className="text-muted-foreground">{config.desc}</p>
      </div>

      {/* Location picker */}
      <div className="flex justify-end mb-4">
        <LocationPicker selectedSlug={locationSlug} onSelect={handleLocationSelect} />
      </div>

      {/* Sub-nav */}
      <div className="flex flex-wrap gap-2 mb-8 border-b border-border pb-4">
        {subNavItems.map(({ key, label, icon: Icon, path }) => (
          <Link key={key} to={path} className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition-colors ${subNavActive === key ? 'bg-gold text-white' : 'border border-border text-muted-foreground hover:border-gold/50 hover:text-gold'}`}>
            <Icon className="h-3 w-3" />{label}
          </Link>
        ))}
      </div>

      {isDateView                                 && <PanchangDateView     dateStr={dateValue}           locationSlug={locationSlug} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'daily'      && <PanchangDailyView    dayOffset={0}                 locationSlug={locationSlug} locationTZ={locationTZ} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'tomorrow'   && <PanchangDailyView    dayOffset={1}                 locationSlug={locationSlug} locationTZ={locationTZ} onDataLoad={setPanchangData} />}
      {!isDateView && activeView === 'tithi'      && <PanchangTithiView                                  locationSlug={locationSlug} />}
      {!isDateView && activeView === 'choghadiya' && <PanchangChoghadiyaView                             locationSlug={locationSlug} />}
      {!isDateView && activeView === 'calendar'   && <PanchangCalendarView year={calYear} month={calMonth} locationSlug={locationSlug} />}
      {!isDateView && activeView === 'festivals'  && <PanchangFestivalsView                              locationSlug={locationSlug} onDataLoad={setFestivalData} />}
    </div>
  );
};
